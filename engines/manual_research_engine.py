"""Manual research ingestion — an offline, zero-Tavily fact source.

Why this exists
---------------
rumor_mill_engine.py resolves deadline/fee/contact_email/submission_url for
opportunities sitting in the needs_research bucket, using 2-4 Tavily searches
per item. On 2026-07-27 it exhausted the monthly Tavily quota at item 558/577,
and rumor_mill_expansion_runner returned data_found=0 for all 80 of its batch —
leaving 135 of that run's 148 new opportunities unresearched.

This engine fills the same slot from a hand-authored source file,
memory/manual_research.json, whose facts are read off each opportunity's real
page. It spends nothing.

The Data Patch Rule (CLAUDE.md)
-------------------------------
deploy_data/compact_opportunities.json is pipeline-generated, so it must never
be hand-edited. memory/manual_research.json is a SOURCE file (hand-maintained,
like artist_master_profile.json) and this engine is the rule that applies it
deterministically on every fresh run. Delete every generated JSON file, re-run
the pipeline, and these facts still land — which is the property the patch rule
is protecting.

Safety
------
Records are hand-authored, so validate_record() is the boundary that keeps
garbage out. It refuses anything that is unprovenanced, malformed, or carries a
model's "I don't know" dressed up as a fact. apply_records() additionally
refuses to overwrite data the pipeline already found unless a record explicitly
opts in via "override": true.
"""

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent))

from engines.deadline_normaliser import parse_deadline_date

# The only fields a manual record may write. A typo'd key is a silent no-op,
# so unknown names are rejected loudly rather than ignored.
ALLOWED_FIELDS = ("deadline", "fee", "contact_email", "submission_url", "eligibility")

# Split-field pairs (audit 2026-07-06): different-era engines write different
# spellings of one concept, and readers prefer different sides — _fees_value
# in api.py prefers "fees" even when it holds a placeholder. Records speak the
# canonical name; the engine reads and writes every spelling the entry carries.
FIELD_ALIASES = {"fee": ("fee", "fees")}


def _aliases(key: str):
    return FIELD_ALIASES.get(key, (key,))


def _is_placeholder(value) -> bool:
    return str(value or "").strip().lower() in PLACEHOLDERS

# How a model says "I don't know". None of these may reach a card as a fact.
PLACEHOLDERS = {"", "unknown", "n/a", "na", "tbd", "none", "null", "-", "--", "?", "tba"}


def _is_http_url(value) -> bool:
    try:
        parsed = urlparse(str(value))
    except (ValueError, AttributeError):
        return False
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def validate_record(rec: dict):
    """Return (ok, reason). Reason is human-readable and names the offending key."""
    if not isinstance(rec, dict):
        return False, "record is not an object"

    if not rec.get("title"):
        return False, "missing title"

    source = rec.get("source_url")
    if not source:
        return False, "missing source_url (provenance is mandatory)"
    if not _is_http_url(source):
        return False, f"source_url is not an http(s) URL: {source!r}"

    if not rec.get("verified_at"):
        return False, "missing verified_at"

    found = rec.get("found") or {}
    retract = rec.get("retract") or {}
    if not isinstance(found, dict) or not isinstance(retract, dict):
        return False, "'found'/'retract' must be objects"
    if not found and not retract:
        return False, "no facts in 'found' and nothing in 'retract'"

    for key, value in found.items():
        if key not in ALLOWED_FIELDS:
            return False, f"unknown field {key!r} (allowed: {', '.join(ALLOWED_FIELDS)})"

        if str(value).strip().lower() in PLACEHOLDERS:
            return False, f"{key} is a placeholder, not a fact: {value!r}"

        if key == "deadline" and parse_deadline_date(str(value)) is None:
            return False, f"deadline does not parse to a real date: {value!r}"

        if key == "submission_url" and not _is_http_url(value):
            return False, f"submission_url is not an http(s) URL: {value!r}"

    if retract:
        # Retraction withdraws misinformation, so it carries a higher burden:
        # it must name the exact bad value it removes and say why.
        for key, value in retract.items():
            if key not in ALLOWED_FIELDS:
                return False, f"unknown retract field {key!r} (allowed: {', '.join(ALLOWED_FIELDS)})"
            if not str(value).strip():
                return False, f"retract.{key} must name the exact wrong value being removed"
        if not str(rec.get("reason") or "").strip():
            return False, "retraction requires a reason"

    return True, "ok"


def _title_of(opp: dict) -> str:
    return str(opp.get("name") or opp.get("title") or "").strip()


def apply_records(opps: list, records: list):
    """Apply validated records onto matching opportunities, in place.

    Fill-only by default: an existing non-empty value is never clobbered unless
    the record sets "override": true. Returns (applied, skipped) where each
    entry is (title, reason)."""
    applied, skipped = [], []
    by_title = {}
    for opp in opps:
        by_title.setdefault(_title_of(opp), opp)

    for rec in records:
        title = str(rec.get("title", "")).strip()

        ok, reason = validate_record(rec)
        if not ok:
            skipped.append((title, f"invalid: {reason}"))
            continue

        opp = by_title.get(title)
        if opp is None:
            skipped.append((title, "no opportunity with this exact title"))
            continue

        override = bool(rec.get("override"))
        wrote = []
        stale = []

        # Retractions first, so a record that retracts AND asserts the same
        # field ends with the asserted value. A retraction only fires when the
        # stored value still equals the named bad value — if the pipeline has
        # since found something different, the stale retraction must not
        # delete it.
        for key, bad_value in (rec.get("retract") or {}).items():
            matched = any(str(opp.get(a) or "").strip() == str(bad_value).strip()
                          for a in _aliases(key))
            if matched:
                # Clear the matched spelling AND any placeholder siblings —
                # "fees": "Unknown" must not keep feeding the serving accessor
                # junk after the misinformation next to it is withdrawn.
                for a in _aliases(key):
                    cur = str(opp.get(a) or "").strip()
                    if cur == str(bad_value).strip() or _is_placeholder(opp.get(a)):
                        opp[a] = ""
                wrote.append(f"retracted {key}")
            elif any(str(opp.get(a) or "").strip() for a in _aliases(key)):
                stale.append(key)

        for key, value in (rec.get("found") or {}).items():
            existing = any(not _is_placeholder(opp.get(a)) and str(opp.get(a) or "").strip()
                           for a in _aliases(key))
            if existing and not override:
                continue
            for a in _aliases(key):
                opp[a] = value
            wrote.append(key)

        if not wrote:
            if stale:
                skipped.append((title, f"stored value no longer matches retraction "
                                       f"({', '.join(stale)}) — not deleting"))
            elif rec.get("retract") and not rec.get("found"):
                skipped.append((title, "already retracted — nothing to do"))
            else:
                skipped.append((title, "all fields already populated (no override)"))
            continue

        opp["manual_research_source"] = rec["source_url"]
        opp["manual_research_at"] = rec["verified_at"]
        applied.append((title, ", ".join(wrote)))

    return applied, skipped


RESEARCH_PATH = Path("memory/manual_research.json")
COMPACT_PATH = Path("deploy_data/compact_opportunities.json")


def run(research_path: Path = RESEARCH_PATH, compact_path: Path = COMPACT_PATH):
    """Apply the source file to the opportunity list. Returns (applied, skipped).

    Every failure mode degrades to a no-op: this runs as one step of a ~101-step
    pipeline and must never abort the run."""
    if not Path(research_path).exists():
        print(f"No {research_path} — nothing to apply.")
        return [], []

    try:
        raw = json.loads(Path(research_path).read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(f"WARNING: {research_path} is not valid JSON ({exc}) — skipping.")
        return [], []

    records = raw.get("records", []) if isinstance(raw, dict) else raw
    if not isinstance(records, list):
        print(f"WARNING: {research_path} has no 'records' list — skipping.")
        return [], []

    if not Path(compact_path).exists():
        print(f"ERROR: {compact_path} not found — nothing to apply to.")
        return [], []

    opps = json.loads(Path(compact_path).read_text(encoding="utf-8"))
    if not isinstance(opps, list):
        print(f"ERROR: {compact_path} is not a list.")
        return [], []

    applied, skipped = apply_records(opps, records)

    if applied:
        Path(compact_path).write_text(
            json.dumps(opps, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    print(f"Manual research: {len(applied)} applied, {len(skipped)} skipped "
          f"(of {len(records)} records)")
    for title, fields in applied:
        print(f"  + {title[:60]} -> {fields}")
    for title, reason in skipped:
        print(f"  - {title[:60]}: {reason}")

    return applied, skipped


if __name__ == "__main__":
    run()
