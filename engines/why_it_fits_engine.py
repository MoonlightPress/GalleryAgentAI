"""
why_it_fits_engine.py

Permanent pipeline step: rewrites weak why_this_fits_short fields in
compact_opportunities.json using Claude Haiku. Skips entries that already
have a strong, venue-specific why. Idempotent — safe to run on every
pipeline pass.

Targets entries in visible buckets where the why field is:
- identical to one_sentence
- contains template/placeholder language
- contains typos/garbled text
- empty or too short
- carries no clause that could only have been written about HER
  (the "her-specific hook" rule — see below)

The hook rule (2026-09-04). The three Today's Focus cards are the first
thing she reads, and their why-line was the opportunity's own catalog
summary said back to her: "a painting competition suitable for watercolor
and illustration artists" describes the contest, not the painter. Every
why-line must now contain at least one concrete anchor to HER — her
watercolor practice, the daily diary, Colour Diary, her exhibition record,
Tokyo/Beijing, her languages, her audience, her subjects. If the model
cannot produce that clause from real profile facts, that is itself the
signal the pick is weak; the serve-time guard in api.py then keeps the
line off the card face rather than shipping boilerplate.

Facts come from memory/artist_master_profile.json and
memory/career_strategy_report.json at run time — never hardcoded, so the
copy tracks her real record instead of drifting behind it.

Flags:
  --only SUBSTR   restrict to entries whose id/name/title contains SUBSTR
                  (repeatable) — for targeted regeneration of a few cards
  --limit N       stop after N rewrites
  --dry-run       print what would be rewritten, call nothing, write nothing
  --force         with --only, rewrite the matches even if they already pass
                  (for when the prompt itself has changed)
"""
import sys
import json
import os
import re
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

from engines.profile_sync import follower_count_str
from engines.why_hook import has_personal_hook, why_line_problem

ROOT     = Path(__file__).parent.parent
OPP_PATH = ROOT / "deploy_data" / "compact_opportunities.json"
PROFILE_PATH = ROOT / "memory" / "artist_master_profile.json"
CAREER_PATH  = ROOT / "memory" / "career_strategy_report.json"

# Buckets whose cards reach her card face (Today's Focus + the browse
# sections). competitions_awards and publication_editorial were missing:
# today's High Impact slot is drawn from competitions_awards, and 273 of its
# 282 entries carried the summary back as the "why".
TARGET_BUCKETS = {
    "immediate_best_moves",
    "publication_targets",
    "japan_book_ecosystem",
    "stretch_targets",
    "relationship_builders",
    "competitions_awards",
    "publication_editorial",
}

# research_needed holds 575 entries — far too many to rewrite every run, and
# most of them never reach a card. But Today's Focus falls back into this
# bucket when a slot's own pool is thin (api.py get_today), so its strongest
# few DO surface. Rewrite that head of the list and leave the tail alone.
BUCKET_HEAD_ONLY = {"research_needed": 40}


def _score(opp: dict) -> float:
    for key in ("truth_aligned_score", "overall_score", "score_base"):
        try:
            return float(opp.get(key))
        except (TypeError, ValueError):
            continue
    return 0.0

# Language-fields the translation engine derives FROM why_this_fits_short.
# Rewriting the English without clearing these would leave her Chinese page
# reading the old sentence forever (needs_translation() only checks whether
# the target exists, not whether its source has moved).
DERIVED_TRANSLATIONS = ("why_it_fits_zh", "why_it_fits_ja")

# The card face renders ~100 characters of the localized line and cuts the rest.
# Chinese carries roughly twice the meaning per character, so an English source
# of about this length arrives as a sentence that fits her card whole.
MAX_WHY_CHARS = 220


def _follower_count() -> str:
    """Read her real follower count from the profile (never hardcode a literal).

    Falls back to the profile_sync default if the profile is missing/unreadable.
    """
    try:
        master = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    except Exception:
        master = {}
    return follower_count_str(master)


def _load(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def artist_facts() -> str:
    """The block of real, current facts the model is allowed to draw on.

    Read from her profile and the computed career report every run, so the
    copy tracks her actual record. Never hardcode a stage or a credit here —
    the old constant this replaced still said "early Tier 2" and named her
    Feb 2023 group show as the latest news, years after both stopped being
    true.
    """
    master  = _load(PROFILE_PATH)
    vp      = master.get("visual_profile", {}) or {}
    hist    = master.get("career_history", {}) or {}
    report  = _load(CAREER_PATH)
    ev      = report.get("career_evidence", {}) or {}

    daily   = (hist.get("daily_practice") or {})
    pubs    = [p for p in (hist.get("publications") or []) if p.get("title")]
    exhibs  = hist.get("exhibitions") or []
    # "exhibition (group/solo not specified on source)" is not a solo show —
    # match the type only where it LEADS with solo, or three become four.
    solos = [e for e in exhibs if (e.get("type") or "").lower().startswith("solo")]

    def _dates(e):
        # Source dates carry research caveats: "August 25, 2026 – approx.
        # September 6, 2026 (end date unconfirmed; believed to run through…)".
        return (e.get("dates") or "").split("(")[0].strip().rstrip(";,")

    solo_str = "; ".join(
        f"{e.get('title', '')} ({e.get('venue', '')}, {e.get('city', '')}, {_dates(e)})"
        for e in solos[-3:]
    )

    subjects = ", ".join((vp.get("dominant_subjects") or [])[:5])
    book     = pubs[0].get("title") if pubs else ""
    missing  = [label for key, label in (
        ("has_representation", "gallery representation"),
        ("has_residency", "a residency"),
        ("has_grant", "a grant"),
    ) if not ev.get(key)]

    lines = [
        f"- Chinese, age {vp.get('age', 26)}, from {vp.get('hometown', 'Changsha, China')}; "
        f"based {vp.get('current_city', 'between Tokyo and Beijing')}.",
        f"- Reads and writes Chinese first; Japanese at {vp.get('japanese_proficiency', 'JLPT N2')} "
        "— she can handle a Japanese-language application herself.",
        f"- Medium: {vp.get('medium', 'watercolor (primary), occasional ink')} — on paper. "
        "Trained in illustration and design, so zines, artist books and illustration "
        "publishing are her home ground; fine-art galleries are the second ecosystem.",
    ]
    if daily.get("started"):
        lines.append(
            f"- Daily watercolor \"{daily.get('name', 'diary')}\" since {daily['started']}, "
            f"posted to {_follower_count()} Instagram followers."
        )
    if book:
        lines.append(f"- Her one book so far: {book} — it grew out of the daily diary.")
    if subjects:
        lines.append(f"- What she paints: {subjects}.")
    if ev:
        lines.append(
            f"- Record: {ev.get('confirmed_group_shows', 0)} confirmed group shows, "
            f"{ev.get('solo_shows', 0)} solo shows, museum group shows, a showing in London, "
            f"{ev.get('publications_confirmed', 0)} publications."
        )
    if solo_str:
        lines.append(f"- Her solo shows: {solo_str}.")
    if master.get("is_student"):
        lines.append("- She is still a student — student-eligible calls genuinely apply to her.")
    if missing:
        lines.append(
            "- Doors still ahead of her (open doors, never write about them as things she lacks): "
            + ", ".join(missing) + "."
        )
    return "\n".join(lines)


def is_weak(opp: dict) -> tuple:
    """Return (is_weak, reason). Good entries return (False, '')."""
    why = opp.get("why_this_fits_short", "") or ""
    one_sent = opp.get("one_sentence", "") or ""

    if not why.strip():
        return True, "empty"
    if why.strip() == one_sent.strip():
        return True, "identical to one_sentence"
    if len(why.strip()) < 40:
        return True, "too short"
    # The card face renders ~100 characters. A 400-character line is not a
    # fuller answer there — it is the first 100 characters plus an ellipsis,
    # which is how a why-line ends up cut off mid-word on the page she reads.
    if len(why.strip()) > MAX_WHY_CHARS + 80:
        return True, "too long for the card"
    if "potential fit because it belongs to a structured opportunity category" in why.lower():
        return True, "template language"
    if "needs verification before recommendation" in why.lower():
        return True, "placeholder text"
    if "watercolor artistly" in why.lower():
        return True, "typo/garbled text"
    if "artist book / watercolor sequence" in why.lower():
        return True, "garbled medium label"
    why_words = set(why.lower().split())
    sent_words = set(one_sent.lower().split())
    if len(why_words) > 5 and len(sent_words) > 5:
        overlap = len(why_words & sent_words) / max(len(why_words), len(sent_words))
        if overlap > 0.85:
            return True, "near-duplicate of one_sentence"
    # The her-specific hook rule. Checked in English (the source) and in the
    # Chinese she actually reads — a hook that survived only in the English
    # is a hook that never reaches her page.
    problem = why_line_problem(why)
    if problem:
        return True, problem
    zh = opp.get("why_it_fits_zh") or ""
    if zh and not has_personal_hook(zh):
        return True, "no her-specific clause (zh)"
    return False, ""


_TIER_TAG_RE = re.compile(r"tier\s*\d", re.I)


def _today_str() -> str:
    from datetime import date
    return date.today().isoformat()


def _trim_to_sentence(text: str, limit: int) -> str:
    """Last resort after the retry: keep whole sentences, never a half one.

    A line the model refuses to shorten is better cut at a full stop here than
    cut mid-word by the card at render time — but only if a real sentence
    survives; otherwise the long line is left intact for the detail panel and
    the serve-time guard decides what reaches the card face.
    """
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    cut = max(text.rfind(stop, 0, limit + 1) for stop in (". ", "。", "！", "？", "? "))
    if cut > 60:
        return text[:cut + 1].strip()  # keep the stop itself
    return text


def build_prompt(opp: dict) -> str:
    title    = opp.get("title") or opp.get("name") or "Unknown"
    one_sent = opp.get("one_sentence") or ""
    category = opp.get("category") or opp.get("category_label") or ""
    city     = opp.get("city") or ""
    tags     = opp.get("tags") or []
    deadline = opp.get("deadline") or ""
    fees     = opp.get("fees") or opp.get("fee") or ""
    why_old  = opp.get("why") or opp.get("why_this_fits_short") or ""
    # Internal taxonomy is kept OUT of the prompt entirely. The bucket name and
    # the "Tier1" tag are how "a concrete Tier-1 route" reached her card face:
    # a model handed the vocabulary will eventually use it.
    tags_str = ", ".join(str(t) for t in tags if t and not _TIER_TAG_RE.search(str(t)))

    return f"""You are writing the one sentence GEGYjiji reads underneath an opportunity on her own
app — the line that tells her why THIS one is worth her attention. She reads it in Chinese; it is
written in English first and translated faithfully, so whatever you write must survive translation.

WHO SHE IS (draw on these facts; invent nothing beyond them):
{artist_facts()}

Today's date: {_today_str()}
Venue/Opportunity: {title}
What it is: {one_sent}
Category: {category}
City: {city}
Deadline (as recorded, may be stale): {deadline or '(unknown)'}
Fee: {fees or '(unknown)'}
Tags: {tags_str}
Previous why note: {why_old[:200] if why_old else '(none)'}

=== NEVER SEND HER AT A DATE THAT HAS ALREADY PASSED ===
Compare any date you are about to write against today's date above. If the recorded deadline is in
the past, or is a repeating annual round, do NOT tell her to act "before" it — the venue is either
rolling or on its next cycle, so give her the step without the date ("email them a small zine
dummy") instead of a deadline she has already missed. Cite a date only when it is still ahead.

Write ONE to TWO sentences telling her, in plain practical terms, why this venue/opportunity is
worth her attention RIGHT NOW. This is advice, not a description — it must help her decide whether
to act, not just summarize what the place is.

=== HARD RULE: {MAX_WHY_CHARS} CHARACTERS, TWO SENTENCES AT THE ABSOLUTE MOST ===
Her card shows the first ~100 characters and cuts the rest off mid-word. A long answer is not a
fuller answer; it is the same answer with the ending thrown away. Put the clause that is about HER
in the FIRST sentence. Count your characters before you answer.

=== HARD RULE: ONE CLAUSE THAT COULD ONLY BE ABOUT HER (this is the point of the line) ===
The sentence must contain at least one clause that would be false, or meaningless, if it were
handed to any other artist. Anchor it in something real from the facts above:
  - her medium and how she works (watercolor on paper, the daily diary since 2020)
  - her book, Colour Diary, and the diary pages it came from
  - her record (the solo shows, the group shows, the museum shows, the London showing)
  - her languages (Chinese first, Japanese at N2 — she can file a Japanese application unaided)
  - her situation (Chinese national living between Tokyo and Beijing; still a student)
  - her audience (the Instagram following the daily diary built)
  - what she actually paints (Tokyo streets, quiet architecture, interiors and interior light, cats)
FORBIDDEN, because they are true of every artist alive: "a Tokyo gallery showing emerging artists",
"suitable for watercolor and illustration artists", "open to international visual artists",
"a good fit for emerging artists". A category word on its own ("watercolor", "Tokyo", "painting")
is NOT the hook — the hook is the clause that ties it to HER work, HER record or HER situation.
If nothing in the facts above genuinely connects her to this opportunity, say so plainly in one
short sentence rather than inventing a connection. A flat honest line is better than a false one.

=== NEVER INVENT A CREDENTIAL ===
Use only the record given above. Do not promote her ("an established painter", "an award-winning
artist"), do not add shows, prizes, representation, residencies or grants she does not have, and do
not describe a door she has not walked through as though she had.

=== HARD RULE: NEVER ASSERT AESTHETIC OR TASTE FIT (this overrides everything else) ===
The system has NOT seen this venue's actual work and does NOT know her personal taste. You therefore
may NOT claim, imply, or rank aesthetic/taste compatibility. Specifically FORBIDDEN:
- Any verdict of fit derived from vibe/tags: "perfect fit", "highest/best aesthetic match",
  "matches your aesthetic", "aligns with your quiet register/sensibility", "your kind of space",
  "they'll love your work", "this is so you", "right up your alley".
- Predicting what she or the venue will like, or how well her work will be received.
- Treating tag/category overlap as proof of taste alignment.
Her taste is genuinely unknown to the system (she likes a wide range, including rough/outsider work),
so any aesthetic verdict here would be a fabricated certainty — exactly the failure we are preventing.
If the only thing connecting her to this venue is vibe/aesthetic, do NOT assert it: hedge instead,
e.g. "contemporary/outsider-leaning — worth a look if you want to judge the fit yourself," and let
HER make the taste call.

=== GROUND EVERY REASON IN VERIFIABLE FACTS ===
Build the reason ONLY from facts in the data above (or facts plainly entailed by them):
the medium the venue shows, whether it accepts un-represented / emerging artists, audience or
subject-matter overlap, fee (or free), deadline, location/city, format (open call, consignment,
grant, fair, zine/bookstore). Lead with one such checkable fact. If you genuinely lack a fact that
would justify recommending it, hedge openly ("worth a look — judge the fit yourself") rather than
inventing enthusiasm.

=== ADVISE, DON'T DESCRIBE ===
- START with a concrete, checkable fact about the opportunity (what it shows, whether it takes
  un-repped artists, the fee, the deadline, the location) — not with a description of its vibe.
- END with a concrete next action she could take (e.g. "submit 6–8 diary works before the May
  deadline", "email the organizer to confirm they take un-repped painters", "consign a small set of
  prints"). Make the action specific to this opportunity.
- Do NOT write filler like "visit their site to get a feel" / "stop by to soak up the atmosphere" /
  "check it out to see if it resonates" — that is not advice.

=== PRESERVE THESE EXISTING RULES ===
- Address her directly in the SECOND PERSON ("you", "your work", "your daily diary"). Never write
  about her in the third person — never use "she", "her work" as if describing someone else, and
  never use her name "GEGYjiji" in the sentence.
- Be specific to this venue — mention what they actually do and why it connects to your work
- Reference watercolor, urban/architectural focus, or your daily practice where relevant
- Do NOT be generic ("a good fit for emerging artists")
- Do NOT repeat the one_sentence description word-for-word
- Do NOT start with "This" — start with the venue name or a specific, checkable aspect of the opportunity
- Do NOT use garbled phrases — use "watercolor" or "works on paper"
- NEVER mention internal taxonomy or system terms ("Tier 1", "Tier 2", "bucket", "immediate best
  moves", "stretch target", "score") — this copy is for her, not for the system.
- NEVER reference a store, shop, sales pipeline, or the system selling/recommending anything to her.
- NEVER include meta-instructions, caveats to a reviewer, or verification notes (e.g.
  "建议在推荐前进行核实" / "verify before recommending" / "needs verification"). Output only the
  finished, her-facing sentence.
- If it's a grant: lead with the eligibility/criteria fact and the deadline, then the next step — do
  NOT claim the work itself is a taste match.
- If it's a bookstore/zine: lead with whether your printed/daily work fits their format (zine,
  consignment, works on paper), then the next step — do NOT assert their curatorial taste matches yours.
- If it's an art fair: state the strategic fit or limitation honestly (cost, reach, audience), then the next step.
- Keep it to 1-2 sentences maximum

=== SAY WHAT IT IS, NOT WHAT IT ISN'T ===
Never end on what her work is not or where it would not go ("not for original paintings",
"rather than framed work", "而非原作绘画"). A trailing negative is both the least useful half of the
sentence and the half she reads last. State the positive route and stop.

Output the 1-2 sentences only, nothing else. Under {MAX_WHY_CHARS} characters."""


def main(only=(), limit=0, dry_run=False, force=False):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        try:
            from dotenv import load_dotenv
            load_dotenv(ROOT / ".env")
            api_key = os.environ.get("ANTHROPIC_API_KEY")
        except ImportError:
            pass
    if not api_key:
        env_path = ROOT / ".env"
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("ANTHROPIC_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not api_key and not dry_run:
        print("ERROR: ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    opps = json.loads(OPP_PATH.read_text(encoding="utf-8"))

    # Heads of the head-only buckets, by score — the entries that can actually
    # reach a card face.
    head_ids = set()
    for bucket_name, top_n in BUCKET_HEAD_ONLY.items():
        ranked = sorted(
            (i for i, o in enumerate(opps)
             if o.get("exclusive_primary_bucket") == bucket_name
             and o.get("recommendation_visibility") != "hidden"),
            key=lambda i: _score(opps[i]), reverse=True,
        )
        head_ids.update(ranked[:top_n])

    targets = []
    for i, opp in enumerate(opps):
        bucket     = opp.get("exclusive_primary_bucket", "")
        visibility = opp.get("recommendation_visibility", "show")
        if bucket not in TARGET_BUCKETS and i not in head_ids:
            continue
        if visibility == "hidden":
            continue
        if only and not _matches_only(opp, only):
            continue
        weak, reason = is_weak(opp)
        if force and only:
            weak, reason = True, reason or "forced"
        if weak:
            targets.append((i, opp, reason))

    if limit:
        targets = targets[:limit]

    if not targets:
        print("No weak why_this_fits_short entries found. Nothing to do.")
        return

    print(f"Found {len(targets)} entries with weak why_this_fits_short.")

    if dry_run:
        for opp_idx, opp, reason in targets:
            title = opp.get("title") or opp.get("name") or "Unknown"
            print(f"  would rewrite: {title[:60]:<60} ({reason})")
        print(f"\nDry run — nothing called, nothing written.")
        return

    import anthropic
    client = anthropic.Anthropic(api_key=api_key)

    updated = 0
    errors  = 0

    for idx, (opp_idx, opp, reason) in enumerate(targets, 1):
        title = opp.get("title") or opp.get("name") or "Unknown"
        print(f"  [{idx:2d}/{len(targets)}] {title[:50]:<50} ({reason})", end=" ", flush=True)

        prompt = build_prompt(opp)
        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}],
            )
            new_why = response.content[0].text.strip()
            if new_why and len(new_why) > 20:
                # One retry when the line came back with nothing of her in it,
                # or long enough that her card would cut it off. The hook is the
                # whole point of the rewrite; shipping a second catalog sentence
                # would leave the card exactly where it was.
                notes = []
                if why_line_problem(new_why):
                    notes.append(
                        "That sentence could have been written about any artist. Rewrite it so one "
                        "clause is unmistakably about her — her watercolor diary, her book, her "
                        "exhibition record, her languages, her Tokyo/Beijing life, or what she "
                        "actually paints."
                    )
                if len(new_why) > MAX_WHY_CHARS:
                    notes.append(
                        f"It is also {len(new_why)} characters; her card cuts off after ~100. "
                        f"Cut it to under {MAX_WHY_CHARS} characters, keeping the clause about her "
                        "in the first sentence and dropping the rest."
                    )
                if notes:
                    retry = client.messages.create(
                        model="claude-haiku-4-5-20251001",
                        max_tokens=200,
                        messages=[
                            {"role": "user", "content": prompt},
                            {"role": "assistant", "content": new_why},
                            {"role": "user", "content":
                             " ".join(notes) + " Output the sentence only."},
                        ],
                    )
                    retried = retry.content[0].text.strip()
                    if retried and len(retried) > 20:
                        new_why = retried
                new_why = _trim_to_sentence(new_why, MAX_WHY_CHARS)
                opps[opp_idx]["why_this_fits_short"] = new_why
                # The Chinese and Japanese lines were translated from the OLD
                # sentence. content_translation_engine only asks whether a
                # target field exists, so leaving them in place would keep her
                # Chinese page on the sentence we just replaced. Clearing them
                # is what makes the rewrite reach the language she reads.
                for field in DERIVED_TRANSLATIONS:
                    opps[opp_idx].pop(field, None)
                updated += 1
                print("ok" if not why_line_problem(new_why) else "ok (still generic)")
            else:
                print("SKIPPED (empty response)")
        except Exception as e:
            print(f"ERROR: {e}")
            errors += 1

        time.sleep(0.3)

    OPP_PATH.write_text(json.dumps(opps, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDone. {updated}/{len(targets)} entries updated. {errors} errors.")
    if updated:
        print("Cleared why_it_fits_zh / why_it_fits_ja on updated entries — "
              "content_translation_engine.py will regenerate them.")


def _matches_only(opp: dict, needles) -> bool:
    hay = " ".join(str(opp.get(k) or "") for k in ("id", "name", "title")).lower()
    return any(n.lower() in hay for n in needles)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--only", action="append", default=[],
                    help="restrict to entries whose id/name/title contains this "
                         "substring (repeatable)")
    ap.add_argument("--limit", type=int, default=0, help="stop after N rewrites")
    ap.add_argument("--dry-run", action="store_true",
                    help="list what would be rewritten; call nothing, write nothing")
    ap.add_argument("--force", action="store_true",
                    help="rewrite the --only matches even if their why already "
                         "passes (used when the prompt itself has changed)")
    args = ap.parse_args()
    main(only=args.only, limit=args.limit, dry_run=args.dry_run, force=args.force)
