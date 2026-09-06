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
  --backlog       widen the scope from the card-face buckets to every entry
                  that can reach her at all — the one-off catch-up run
  --workers N     parallel model calls (default 1)
"""
import sys
import json
import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
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

# Buckets api.load_opportunities() drops before anything is served. An entry in
# one of these can never reach her, in any surface, so it is never worth a
# model call — even in --backlog mode.
NEVER_SERVED_BUCKETS = {"reject", "low_priority"}


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

# Model + list price in USD per million tokens, used to print what a run cost —
# a backlog pass is ~1,000 calls and whoever pays for it should not have to
# infer the bill from token counts.
#
# Why Sonnet 5 rather than Haiku: the prompt is ~3.7k tokens of fixed rules and
# fixed facts about her, and only ~40 tokens of per-entry detail. Haiku 4.5
# cannot cache that — its minimum cacheable prefix is 4,096 tokens, so a
# marked-up 3.7k block silently caches nothing and every call pays full price
# for the same text. Sonnet 5's minimum is 1,024, so the prefix is written once
# and read back at a tenth of the price for the rest of the run. That makes the
# stronger model the CHEAPER one here (~$0.0017/call against ~$0.0032 for
# uncached Haiku). Do not "optimize" this back to Haiku without re-checking
# that table — the saving is a rounding error and the cache disappears.
MODEL = "claude-sonnet-5"
PRICE_IN_PER_M  = 2.00
PRICE_OUT_PER_M = 10.00
CACHE_WRITE_MULT = 1.25   # writing the prefix costs 1.25x an input token
CACHE_READ_MULT  = 0.10   # reading it back costs a tenth


def SYSTEM_BLOCK():
    """The stable prompt, marked cacheable. Same object shape every call."""
    return [{"type": "text",
             "text": system_prompt(),
             "cache_control": {"type": "ephemeral"}}]


# Sonnet 5 thinks by default. Rewriting one sentence against a fixed rule set is
# not a reasoning task, and thinking tokens bill at the output rate — left on,
# a 60-token budget was spent entirely on thinking and returned no sentence.
NO_THINKING = {"type": "disabled"}


def first_text(response) -> str:
    """The response's text, wherever it sits in the content list.

    content[0] is not reliably the answer — with thinking enabled it is a
    ThinkingBlock, and reaching straight for .text raises AttributeError.
    """
    for block in response.content:
        if getattr(block, "type", "") == "text":
            return block.text
    return ""


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

    # Her subject is architecture and space. Cats do appear in the paintings,
    # but they are incidental — and the moment a cat is in the fact block, the
    # model reaches for it, because "a cat" is the easiest concrete noun in the
    # list. Drop them here so the reason a line gives is the reason that is
    # actually true: streets, buildings, interiors, the light in a known room.
    subjects = ", ".join(
        s for s in (vp.get("dominant_subjects") or [])
        if "cat" not in s.lower()
    ) or ""
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
        lines.append(
            f"- What she paints — architecture and space above all: {subjects}."
        )
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
    # The tier ladder is internal scoring, never something she should read.
    if tier_leak(why) or tier_leak(opp.get("why_it_fits_zh", "")):
        return True, "names the internal tier framework"
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
    # A line where the system talks about itself instead of to her. The
    # generator already refuses to WRITE one, but lines predating that guard
    # are sitting in the data — "I cannot write this line without seeing the
    # venue's actual requirements" was live on a publication_targets entry,
    # invisible to every other check here because it happens to mention her
    # watercolor diary. Checked in both languages, since either can reach her.
    if meta_problem(why) or meta_problem(zh):
        return True, "system talking about itself"
    return False, ""


_TIER_TAG_RE = re.compile(r"tier\s*\d", re.I)

# Built once per process; see system_prompt().
_SYSTEM_CACHE = None


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


_CHAR_COUNT_RE = re.compile(
    r"\s*[\(（]\s*\d+\s*(?:characters?|chars?|字符|个字|字|文字)\s*[\)）]\s*$", re.I)
_EMPHASIS_RE = re.compile(r"\*{1,3}([^*\n]+?)\*{1,3}")


def sanitize(text: str) -> str:
    """Strip the two things the model adds that her card renders literally.

    A prompt that says "count your characters" gets a character count back:
    roughly one line in four came back ending "(217 characters)", which the
    card prints as part of the sentence. And Markdown emphasis around a title
    (*Colour Diary*) arrives on her page as asterisks, because the card renders
    plain text, not Markdown.
    """
    text = (text or "").strip()
    # Fenced/quoted whole-line output.
    if len(text) > 1 and text[0] in "\"'“「" and text[-1] in "\"'”」":
        text = text[1:-1].strip()
    prev = None
    while prev != text:                       # a count can trail a count
        prev = text
        text = _CHAR_COUNT_RE.sub("", text).strip()
    text = _EMPHASIS_RE.sub(r"\1", text)
    return text.strip()


# Phrases that mean the model answered the SYSTEM instead of answering her.
# "I cannot recommend this opportunity because the recorded deadline has passed"
# is a note to a reviewer; on her page it is the app apologising to her in the
# first person about its own data quality.
_META_PATTERNS = (
    r"\bi (?:cannot|can't|can not|am unable|don't|do not|would not|couldn't)\b",
    r"\bas an ai\b",
    r"\bthis opportunity (?:cannot|should not|needs)\b",
    r"\b(?:needs|requires) verification\b",
    r"\bverify before\b",
    r"\bno actionable step\b",
    r"\bthe (?:recorded )?deadline (?:has )?(?:already )?passed",
    r"我无法|无法推荐|建议在推荐前",
)
_META_RE = re.compile("|".join(_META_PATTERNS), re.I)

# The tier ladder is an internal scoring concept. It has now leaked to her card
# twice — once via bucket names fed to the model, once invented by the model
# itself — so it is caught on output as well as kept out of the prompt.
_TIER_RE = re.compile(r"\btier[\s\-]?[1-4]\b|[一二三四]级(?:途径|机会|目标)|第[一二三四]级", re.I)


def tier_leak(text: str) -> bool:
    """True when a line names the internal tier ladder in any language."""
    return bool(_TIER_RE.search(text or ""))


def meta_problem(text: str) -> bool:
    """True when the line talks about the system's own limits instead of to her."""
    return bool(_META_RE.search(text or ""))


def system_prompt() -> str:
    """The stable half of the prompt — everything that does not vary by entry.

    Split out from the per-entry half so it can be sent as a cached system
    block. A backlog pass is ~1,000 calls and this text is ~4,300 tokens of the
    ~4,700 in each one; without caching the run pays full price to re-read her
    profile and the same rules a thousand times over. Cached, the repeat reads
    cost a tenth of that. Nothing here may vary between calls — one changed
    byte invalidates the prefix for every subsequent entry.
    """
    global _SYSTEM_CACHE
    if _SYSTEM_CACHE is None:
        _SYSTEM_CACHE = f"""You are writing the one sentence GEGYjiji reads underneath an opportunity on her own
app — the line that tells her why THIS one is worth her attention. She reads it in Chinese; it is
written in English first and translated faithfully, so whatever you write must survive translation.

WHO SHE IS (draw on these facts; invent nothing beyond them):
{artist_facts()}

Today's date: {_today_str()}

=== NEVER SEND HER AT A DATE THAT HAS ALREADY PASSED ===
Compare any date you are about to write against today's date above. If the recorded deadline is in
the past, or is a repeating annual round, do NOT tell her to act "before" it — the venue is either
rolling or on its next cycle, so give her the step without the date ("email them a small zine
dummy") instead of a deadline she has already missed. Cite a date only when it is still ahead.
Do not NAME a past date at all, not even to report that it has gone ("the August 16 deadline has
passed") — a date she cannot act on is noise, and opening on it wastes the line she reads first.
Lead instead with what the venue takes, then give her the step.

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
  - what she actually paints: architecture and space — Tokyo streets, city corners, quiet
    buildings, interiors and the light coming through a window she knows well
Cats are NOT her subject. They pass through some of the paintings the way a passer-by does, and a
line that leans on them describes the wrong artist. Never make a cat the reason.
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

=== NEVER WRITE ABOUT YOURSELF OR ABOUT THE DATA ===
This line appears on her page as advice from her own app. Never use "I", never mention that you
cannot recommend something, never comment on missing or stale information, and never open on the
news that a deadline has passed. If the record is thin, write the honest practical step anyway
("email them to ask what they take and when they next open") and stop there.

=== PLAIN TEXT, AND THE SENTENCE ALONE ===
Her card renders exactly what you write. So: no Markdown (no *asterisks* around a title), no
quotation marks around the whole line, no preamble, and NEVER append a character count or any note
about your own answer — "(174 characters)" is printed onto her card verbatim.

Output the 1-2 sentences only, nothing else. Under {MAX_WHY_CHARS} characters.

The specific opportunity follows in the next message."""
    return _SYSTEM_CACHE


def build_prompt(opp: dict) -> str:
    """The per-entry half: just this opportunity's facts."""
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

    return f"""Venue/Opportunity: {title}
What it is: {one_sent}
Category: {category}
City: {city}
Deadline (as recorded, may be stale): {deadline or '(unknown)'}
Fee: {fees or '(unknown)'}
Tags: {tags_str}
Previous why note: {why_old[:200] if why_old else '(none)'}"""


def _servable(opp: dict) -> bool:
    """Can this entry reach her at all? Mirrors api.load_opportunities()."""
    return (
        opp.get("exclusive_primary_bucket") not in NEVER_SERVED_BUCKETS
        and opp.get("status") != "permanently_closed"
        and opp.get("recommendation_visibility") != "hidden"
    )


def main(only=(), limit=0, dry_run=False, force=False, backlog=False, workers=1):
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
        if backlog:
            # Every entry that can reach her, not just the card-face buckets.
            # The default scope is deliberately narrow because this engine runs
            # on every pipeline pass; the backlog run is the one-off that clears
            # the tail behind it.
            if not _servable(opp):
                continue
        else:
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
    done    = 0
    tok_in      = 0
    tok_out     = 0
    tok_cache_r = 0
    tok_cache_w = 0
    lock        = threading.Lock()

    def count(usage):
        """Fold one response's token usage into the run totals."""
        nonlocal tok_in, tok_out, tok_cache_r, tok_cache_w
        with lock:
            tok_in      += usage.input_tokens
            tok_out     += usage.output_tokens
            tok_cache_r += getattr(usage, "cache_read_input_tokens", 0) or 0
            tok_cache_w += getattr(usage, "cache_creation_input_tokens", 0) or 0

    def rewrite(job):
        """Generate one line. Returns (opp_idx, new_why or None, note)."""
        opp_idx, opp, reason = job
        nonlocal tok_in, tok_out, tok_cache_r, tok_cache_w
        prompt = build_prompt(opp)
        response = client.messages.create(
            model=MODEL,
            max_tokens=200,
            system=SYSTEM_BLOCK(),
            thinking=NO_THINKING,
            messages=[{"role": "user", "content": prompt}],
        )
        count(response.usage)
        new_why = sanitize(first_text(response))
        if not new_why or len(new_why) <= 20:
            return opp_idx, None, "SKIPPED (empty response)"
        # One retry when the line came back with nothing of her in it,
        # or long enough that her card would cut it off. The hook is the
        # whole point of the rewrite; shipping a second catalog sentence
        # would leave the card exactly where it was.
        notes = []
        if meta_problem(new_why):
            notes.append(
                "Never write about yourself, your recommendation, or the state of the data — she "
                "reads this line on her own page, and 'I cannot recommend this' is the app "
                "apologising to her. Never open on a deadline having passed either. Write to her "
                "in the second person about what this venue takes and what she could send them."
            )
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
                model=MODEL,
                max_tokens=200,
                system=SYSTEM_BLOCK(),
                thinking=NO_THINKING,
                messages=[
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": new_why},
                    {"role": "user", "content":
                     " ".join(notes) + " Output the sentence only."},
                ],
            )
            count(retry.usage)
            retried = sanitize(first_text(retry))
            if retried and len(retried) > 20:
                new_why = retried
        new_why = _trim_to_sentence(new_why, MAX_WHY_CHARS)
        if meta_problem(new_why):
            # Twice asked and still writing about itself. Her existing line is
            # weak, but a weak line is a weak line — the app talking about its
            # own data quality on her card is a different and worse failure,
            # and the serve-time guard already keeps weak lines off the face.
            return opp_idx, None, "SKIPPED (meta/self-referential after retry)"
        return opp_idx, new_why, "ok" if not why_line_problem(new_why) else "ok (still generic)"

    def apply(opp_idx, new_why):
        opps[opp_idx]["why_this_fits_short"] = new_why
        # The Chinese and Japanese lines were translated from the OLD
        # sentence. content_translation_engine only asks whether a
        # target field exists, so leaving them in place would keep her
        # Chinese page on the sentence we just replaced. Clearing them
        # is what makes the rewrite reach the language she reads.
        for field in DERIVED_TRANSLATIONS:
            opps[opp_idx].pop(field, None)

    def save():
        OPP_PATH.write_text(json.dumps(opps, ensure_ascii=False, indent=2), encoding="utf-8")

    def record(job, result, exc):
        """Log one finished job and fold it into the list. Holds the lock."""
        nonlocal updated, errors, done
        opp_idx, opp, reason = job
        title = opp.get("title") or opp.get("name") or "Unknown"
        done += 1
        if exc is not None:
            errors += 1
            print(f"  [{done:4d}/{len(targets)}] {title[:50]:<50} ERROR: {exc}", flush=True)
            return
        _, new_why, note = result
        if new_why:
            apply(opp_idx, new_why)
            updated += 1
            # A long backlog run that dies at entry 900 should not throw away
            # 900 paid-for sentences; checkpoint as we go.
            if updated % 50 == 0:
                save()
        print(f"  [{done:4d}/{len(targets)}] {title[:50]:<50} ({reason}) {note}", flush=True)

    if workers > 1:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(rewrite, job): job for job in targets}
            for fut in as_completed(futures):
                job = futures[fut]
                try:
                    result, exc = fut.result(), None
                except Exception as e:          # noqa: BLE001 — logged per entry
                    result, exc = None, e
                with lock:
                    record(job, result, exc)
    else:
        for job in targets:
            try:
                result, exc = rewrite(job), None
            except Exception as e:              # noqa: BLE001 — logged per entry
                result, exc = None, e
            record(job, result, exc)
            time.sleep(0.3)

    save()
    cost = (
        tok_in        / 1e6 * PRICE_IN_PER_M
        + tok_out     / 1e6 * PRICE_OUT_PER_M
        + tok_cache_w / 1e6 * PRICE_IN_PER_M * CACHE_WRITE_MULT
        + tok_cache_r / 1e6 * PRICE_IN_PER_M * CACHE_READ_MULT
    )
    print(f"\nDone. {updated}/{len(targets)} entries updated. {errors} errors.")
    print(f"Tokens: {tok_in:,} in / {tok_out:,} out / "
          f"{tok_cache_r:,} cache-read / {tok_cache_w:,} cache-write")
    print(f"Estimated cost at list price: ~${cost:.2f}")
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
    ap.add_argument("--backlog", action="store_true",
                    help="widen the scope from the card-face buckets to EVERY "
                         "entry that can reach her (skips reject/low_priority/"
                         "hidden/closed) — the one-off catch-up run")
    ap.add_argument("--workers", type=int, default=1,
                    help="parallel model calls (default 1; 8 is comfortable for "
                         "a backlog run)")
    args = ap.parse_args()
    main(only=args.only, limit=args.limit, dry_run=args.dry_run, force=args.force,
         backlog=args.backlog, workers=args.workers)
