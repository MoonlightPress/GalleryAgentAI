import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

BUCKET_PATH = "memory/exclusive_strategy_buckets.json"
DEPLOY_PATH = "deploy_data/compact_opportunities.json"
SNAPSHOT_PATH = "memory/daily_digest_snapshot.json"
REPORT_PATH = "reports/daily_digest.md"

MONTH_MAP = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

UNKNOWN_DEADLINE_TOKENS = {
    "unknown", "check source", "check current schedule",
    "n/a", "tbd", "varies",
}


def load_json(path, fallback=None):
    p = Path(path)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return fallback if fallback is not None else {}


def parse_deadline(text):
    """Extract the earliest concrete date from a deadline string. Returns date or None."""
    if not text:
        return None
    stripped = text.strip().lower()
    # Skip exact placeholder values with no parseable date content
    if stripped in UNKNOWN_DEADLINE_TOKENS:
        return None

    today = date.today()
    candidates = []

    # ISO: 2026-06-30
    for m in re.finditer(r"(20\d{2})-(\d{2})-(\d{2})", text):
        try:
            candidates.append(date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        except ValueError:
            pass

    # "June 30, 2026" or "Jun 30 2026"
    for m in re.finditer(
        r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\.?\s+(\d{1,2}),?\s+(20\d{2})",
        text, re.I,
    ):
        try:
            candidates.append(date(int(m.group(3)), MONTH_MAP[m.group(1).lower()[:3]], int(m.group(2))))
        except (ValueError, KeyError):
            pass

    # "June 27" (no year — assume current or next year)
    for m in re.finditer(
        r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\.?\s+(\d{1,2})\b(?!\s*,?\s*20\d{2})",
        text, re.I,
    ):
        try:
            month = MONTH_MAP[m.group(1).lower()[:3]]
            day = int(m.group(2))
            d = date(today.year, month, day)
            if d < today:
                d = date(today.year + 1, month, day)
            candidates.append(d)
        except (ValueError, KeyError):
            pass

    # "July 8" inside a longer string like "July 8, 2026 — 11:59 PM Pacific"
    for m in re.finditer(r"(20\d{2})", text):
        year = int(m.group(1))
        # Already handled above with full patterns, but pick up bare years
        pass

    if not candidates:
        return None
    # Return the soonest upcoming date, or the most recent past date if all are past
    future = [d for d in candidates if d >= today]
    return min(future) if future else max(candidates)


def days_label(delta):
    if delta is None:
        return None
    if delta < 0:
        return f"PAST ({abs(delta)}d ago)"
    if delta == 0:
        return "TODAY"
    if delta <= 7:
        return f"{delta}d — this week"
    return f"{delta}d"


def urgency_prefix(delta):
    if delta is None:
        return ""
    if delta < 0:
        return "~~"
    if delta <= 7:
        return "**"
    if delta <= 14:
        return "*"
    return ""


def main():
    today = date.today()
    buckets = load_json(BUCKET_PATH, {})
    deploy = load_json(DEPLOY_PATH, [])
    snapshot = load_json(SNAPSHOT_PATH, None)

    # Build name → record lookup from deploy_data
    deploy_by_name = {}
    for o in deploy:
        name = (o.get("name") or o.get("title") or "").strip()
        if name:
            deploy_by_name[name.lower()] = o

    ibm = buckets.get("immediate_best_moves", [])
    stretch = buckets.get("stretch_targets", [])
    research = buckets.get("research_needed", [])

    # Enrich IBM entries with deadline/fee/link from deploy_data
    ibm_enriched = []
    for entry in ibm:
        name = entry.get("title") or entry.get("name") or ""
        detail = deploy_by_name.get(name.lower(), {})
        deadline_raw = detail.get("deadline") or ""
        event_date_raw = detail.get("event_date") or ""
        fees_raw = detail.get("fees") or ""
        # Prefer submission_page over source_url for the action link
        link = detail.get("submission_page") or detail.get("source_url") or entry.get("source") or ""
        deadline_date = parse_deadline(deadline_raw)
        delta = (deadline_date - today).days if deadline_date else None
        ibm_enriched.append({
            "name": name,
            "score": entry.get("score"),
            "deadline_raw": deadline_raw,
            "event_date_raw": event_date_raw,
            "deadline_date": deadline_date,
            "delta": delta,
            "fees": fees_raw,
            "link": link,
            "action_type": entry.get("action_type", "apply"),
            "why": (entry.get("why") or "")[:140],
        })

    # Sort: soonest deadline first, then no-deadline entries by score
    def sort_key(e):
        if e["delta"] is not None:
            return (0, e["delta"])
        return (1, -(e["score"] or 0))

    ibm_enriched.sort(key=sort_key)

    # Watch list: items outside IBM with deadlines in the next 90 days
    watch_items = []
    for bucket_name, entries in [("stretch_targets", stretch), ("research_needed", research)]:
        for entry in entries:
            name = entry.get("title") or entry.get("name") or ""
            detail = deploy_by_name.get(name.lower(), {})
            deadline_raw = detail.get("deadline") or ""
            deadline_date = parse_deadline(deadline_raw)
            if deadline_date is None:
                continue
            delta = (deadline_date - today).days
            if 0 <= delta <= 90:
                watch_items.append({
                    "name": name,
                    "deadline_raw": deadline_raw,
                    "deadline_date": deadline_date,
                    "delta": delta,
                    "bucket": bucket_name,
                })
    watch_items.sort(key=lambda x: x["delta"])

    # Diff against previous snapshot
    curr_ibm_names = [e["name"] for e in ibm_enriched]
    curr_ibm_scores = {e["name"]: e["score"] for e in ibm_enriched}
    curr_opp_count = len(deploy)

    if snapshot:
        prev_ibm_names = snapshot.get("ibm_names", [])
        prev_ibm_scores = snapshot.get("ibm_scores", {})
        prev_opp_count = snapshot.get("opportunity_count", 0)
        prev_date = snapshot.get("date", "unknown")

        added = [n for n in curr_ibm_names if n not in prev_ibm_names]
        removed = [n for n in prev_ibm_names if n not in curr_ibm_names]
        score_changes = [
            (n, prev_ibm_scores[n], curr_ibm_scores[n])
            for n in curr_ibm_names
            if n in prev_ibm_scores and prev_ibm_scores[n] != curr_ibm_scores[n]
        ]
        opp_delta = curr_opp_count - prev_opp_count
    else:
        added = removed = score_changes = []
        prev_date = None
        opp_delta = 0

    # ── Build report ──────────────────────────────────────────────────────────
    lines = [f"# Daily Digest — {today.strftime('%B %d, %Y')}", ""]

    # What changed
    lines += ["## What Changed Since Last Run", ""]
    if not snapshot:
        lines.append("_First run — baseline established. Comparison will appear on the next run._")
    else:
        lines.append(f"_Previous run: {prev_date}_")
        lines.append("")
        if not added and not removed and not score_changes and opp_delta == 0:
            lines.append("No changes detected.")
        else:
            for n in added:
                lines.append(f"- **Added to Immediate Best Moves:** {n}")
            for n in removed:
                lines.append(f"- **Removed from Immediate Best Moves:** {n}")
            for n, prev_s, curr_s in score_changes:
                direction = "↑" if curr_s > prev_s else "↓"
                lines.append(f"- **Score change:** {n} {prev_s} → {curr_s} {direction}")
            if opp_delta != 0:
                sign = "+" if opp_delta > 0 else ""
                lines.append(f"- **Opportunity count:** {prev_opp_count} → {curr_opp_count} ({sign}{opp_delta})")
    lines.append("")

    # Immediate Best Moves
    lines += [f"## Immediate Best Moves ({len(ibm_enriched)})", ""]
    for e in ibm_enriched:
        delta = e["delta"]
        prefix = urgency_prefix(delta)
        suffix = prefix  # closing mark if prefix is ** or *

        name_display = f"{prefix}{e['name']}{suffix}" if prefix else e["name"]
        lines.append(f"### {name_display}")

        if delta is not None:
            label = days_label(delta)
            lines.append(f"- **Apply by:** {e['deadline_raw']} — _{label}_")
        elif e["deadline_raw"]:
            lines.append(f"- **Apply by:** {e['deadline_raw']}")
        else:
            lines.append(f"- **Apply by:** — _(contact / propose)_")
        if e.get("event_date_raw"):
            lines.append(f"- **Event date:** {e['event_date_raw']}")

        if e["fees"]:
            lines.append(f"- **Fee:** {e['fees']}")
        if e["link"]:
            lines.append(f"- **Link:** {e['link']}")
        if e["why"]:
            lines.append(f"- _{e['why']}_")
        lines.append("")

    # Watch list
    lines += ["## Watch List — Deadlines Within 90 Days", ""]
    if watch_items:
        for w in watch_items:
            delta = w["delta"]
            bucket_label = "Stretch" if w["bucket"] == "stretch_targets" else "Research"
            lines.append(
                f"- **{w['name']}** — {w['deadline_raw']} "
                f"({delta}d) [{bucket_label}]"
            )
    else:
        lines.append("_No items outside IBM with confirmed deadlines in the next 90 days._")
    lines.append("")

    # Write outputs
    Path("reports").mkdir(exist_ok=True)
    Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {REPORT_PATH}")

    new_snapshot = {
        "date": today.isoformat(),
        "ibm_names": curr_ibm_names,
        "ibm_scores": curr_ibm_scores,
        "opportunity_count": curr_opp_count,
    }
    Path(SNAPSHOT_PATH).write_text(
        json.dumps(new_snapshot, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Wrote {SNAPSHOT_PATH}")

    # Stdout summary
    print(f"\nIBM: {len(ibm_enriched)} entries")
    for e in ibm_enriched:
        dl = f"{e['delta']}d" if e["delta"] is not None else "no deadline"
        print(f"  {e['name']}: {dl}")
    if watch_items:
        print(f"\nWatch list: {len(watch_items)} item(s) with deadlines ≤90d")
    if snapshot and (added or removed):
        print(f"Changes: +{len(added)} added, -{len(removed)} removed from IBM")


if __name__ == "__main__":
    main()
