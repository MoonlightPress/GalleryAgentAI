"""
ibm_email_writer.py

Writes venue-specific outreach email drafts for GEGYjiji using the Claude API.

Rewritten 2026-06-26 to the Squire (fit/truth) + Lore (voice) standards in
`_reviews/2026-06-26_email_pass/`. Key rules now enforced:
  • LANGUAGE FOLLOWS THE VENUE: Japanese for Japan venues, Chinese for Chinese
    venues, English only for genuinely international/Anglophone ones. (Email is
    the one place language matters — most venues are JP/CN; EN is for the
    occasional "brave" international target.)
  • RIGHT MECHANISM: skip venues that take no email — print-on-demand/self-serve
    (SUZURI), gallery-booth art fairs that only galleries enter (Tokyo Gendai),
    and any call whose deadline has already passed.
  • ANTI-SAMENESS: never default to the same "red walls / alleyways / pools /
    green ponds" image list; each draft gets a different rotated image from her
    world and must phrase its one practice-statement freshly.
  • NO INVENTED VENUE AESTHETIC: open from real venue facts only; if thin, open
    on a neutral verifiable fact, never manufactured praise.
  • DEDUPE by organisation; one venue = one draft.
  • TOP OF EACH SECTION, not only the top-N immediate-best-moves.

Writes email_ja / email_zh / email_en back to compact_opportunities.json and
standalone .txt files to reports/inquiry_drafts/.

Usage:
    python engines/ibm_email_writer.py            # generate (top per section)
    python engines/ibm_email_writer.py --limit 30
    python engines/ibm_email_writer.py --dry      # show targets+language, no API calls
"""
import sys
import json
import os
import re
import time
import argparse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

from engines.profile_sync import select_email_targets, clear_drafts_stale, follower_count_str
try:
    from engines.profile_sync import _is_eligible
except Exception:
    def _is_eligible(o):  # permissive fallback
        return True
try:
    from engines.deadline_normaliser import deadline_is_past
except Exception:
    def deadline_is_past(_field, today=None):
        return False
from engines.notify import notify_discord

OPP_PATH     = Path("deploy_data/compact_opportunities.json")
PROFILE_PATH = Path("memory/artist_master_profile.json")
ANALYSIS_DIR = Path("Memory/generated_analysis")
OUT_DIR      = Path("reports/inquiry_drafts")

# Sections that should never produce an outreach email.
JUNK_SECTIONS = {"reject", "research_needed", "low_priority"}


def load_artist_context() -> str:
    """Build artist context string from artist_master_profile.json."""
    if not PROFILE_PATH.exists():
        return _ARTIST_CONTEXT_FALLBACK

    profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    stmt    = profile.get("artist_statement", {})
    hist    = profile.get("career_history", {})

    verbatim_ja  = stmt.get("verbatim_source_ja", "")
    translated   = stmt.get("verbatim_translation_en", "")
    synthesized  = stmt.get("synthesized_en", "")
    tone_signal  = stmt.get("tone_signal", "")

    handles = hist.get("online_handles", {})
    insta   = handles.get("instagram", "@gegyjiji")
    followers = follower_count_str(profile)

    ctx = f"""Name: GEGYjiji (ジェジー / GEGY挤挤)
Instagram: {insta} (https://www.instagram.com/gegyjiji/) (~{followers} followers, daily watercolor diary)
Based: Tokyo (originally from Hunan Province, China; Beijing Fashion Institute — illustration/design)

Key works (use ONLY these — no invented awards, residencies, representation, sales, or follower numbers):
• "Colour Diary (色彩日記)" — first solo illustration collection, Oct 2021. Grew from a daily watercolor diary practice begun in 2020.
• "Tide from China Part1" — first Japan exhibition, Feb 2023. Group show with 5 other Chinese illustrators at ACG_Labo, Harajuku, Tokyo.
• Daily watercolor diary ("diary") — ongoing since 2020.

Her own voice (exhibition bio — for TONE reference only, do NOT copy its image list verbatim):
  Japanese: {verbatim_ja}
  Translation: {translated}

Tone note: {tone_signal}
Synthesized bio: {synthesized}

Truest self-description: "watercolor illustrator / 水彩イラストレーター" (illustration-ecosystem roots). "画家/painter" is acceptable but not the default for zine/book/illustration venues.
Career stage: building exhibition history and relationships; NO gallery representation."""
    # Redact the overused stock image-list from the context so the model can't
    # copy it verbatim into every draft (Lore's anti-sameness finding); the
    # rotated image_hint supplies a fresh image per email instead.
    for stock, repl in (
        ("赤い壁、路地、プール、緑の池", "［ありふれた日常の情景］"),
        ("red walls, alleyways, pools, green ponds", "[ordinary daily scenes]"),
    ):
        ctx = ctx.replace(stock, repl)
    return ctx


_ARTIST_CONTEXT_FALLBACK = """
Name: GEGYjiji (ジェジー / 挤挤)
Instagram: @gegyjiji (~27,000 followers, daily watercolor diary)
Based: Tokyo. Watercolor. Daily diary practice since 2020. Colour Diary (2021).
""".strip()


# She paints PLACES — ordinary locations and their quiet atmosphere — NOT a list
# of objects or colours. Each draft leads with a different place so the emails
# vary naturally, without ever cataloguing "red walls / alleyways / pools…".
PRACTICE_PLACES = [
    "a quiet room at home",
    "a street corner she passes every day",
    "a neighbourhood park",
    "the view from a train window as the seasons change",
    "an ordinary corner of the city most people walk past",
    "a familiar place seen in a new light",
    "the rooms and streets of everyday life",
    "a station or a café she knows well",
]

# Category → (tone_key, action, max_sentences). Language is decided separately by
# the venue, NOT here (that was the bug: uncovered categories defaulted to EN).
TONE_MAP = {
    "zine_shop_consignment": ("casual",            "consignment inquiry",                4),
    "bookstore_gallery":     ("warm_professional",  "consignment or exhibition inquiry",  5),
    "bookstore_event":       ("warm_professional",  "event or talk inquiry",              4),
    "cafe_gallery":          ("neighborly",         "short-term exhibition inquiry",      3),
    "zine_fair_booth":       ("application",        "booth application inquiry",           4),
    "fair_popup":            ("professional",       "exhibitor application inquiry",       5),
    "gallery":               ("formal",             "submission / exhibition proposal",    6),
    "gallery_event":         ("professional",       "open-call submission inquiry",        5),
    "artist_space":          ("formal",             "space-use application",               5),
    "event_space":           ("formal",             "event participation inquiry",         5),
    "market_event":          ("warm_professional",  "participation inquiry",               4),
    "japan_watercolor_open_call": ("formal",        "open-call entry inquiry",             5),
    "global_watercolor_open_call":("professional",  "open-call entry inquiry",             5),
    "global_open_call":      ("professional",       "open-call entry inquiry",             5),
}
TONE_DESC = {
    "casual":            "Casual and warm — fellow makers talking. Light, no stiff honorifics.",
    "warm_professional": "Warm but professional. Respectful, never robotic.",
    "neighborly":        "Very brief, neighborly — like a note left at the counter.",
    "application":       "Friendly and clear; state the practical info they need.",
    "professional":      "Professional and concise, for a first contact.",
    "formal":            "Professionally formal — correct Japanese keigo (ご担当者様 / 存じます) or formal English/Chinese register.",
}

_JP_CITIES = ["tokyo", "東京", "osaka", "大阪", "kyoto", "京都", "nagoya", "名古屋", "fukuoka",
              "福岡", "yokohama", "横浜", "kobe", "神戸", "sapporo", "shimokitazawa", "koenji",
              "daikanyama", "shibuya", "渋谷", "harajuku", "原宿", "japan", "日本"]
_CN_CITIES = ["beijing", "北京", "shanghai", "上海", "shenzhen", "深圳", "guangzhou", "广州",
              "changsha", "长沙", "chengdu", "成都", "hangzhou", "杭州", "china", "中国"]
_EN_COUNTRIES = ["canada", "united kingdom", "uk", "u.k", "united states", "usa", "u.s",
                 "australia", "france", "germany", "netherlands", "singapore", "international"]


def _blob(opp: dict) -> str:
    parts = [opp.get(k, "") for k in
             ("name", "title", "organization", "category", "city", "country",
              "one_sentence", "overview", "why_it_fits", "why_this_fits_short", "tags")]
    return " ".join(str(p) for p in parts if p).lower()


def venue_language(opp: dict) -> str:
    """ja / zh / en, decided by the venue's real location & operating language."""
    country = str(opp.get("country", "") or "").lower()
    city    = str(opp.get("city", "") or "").lower()
    cat     = str(opp.get("category", "") or "").lower()
    blob    = _blob(opp)

    # Explicitly international / Anglophone → English.
    if any(c in country for c in _EN_COUNTRIES):
        return "en"
    if cat.startswith("global_") or "global_" in cat:
        # Global calls are run in English unless clearly CN/JP-hosted.
        if not any(c in blob for c in _CN_CITIES) and "japan" not in blob and "日本" not in blob:
            return "en"
    # China.
    if "china" in country or "中国" in blob or any(c in city for c in _CN_CITIES):
        return "zh"
    # Japan (also catches the japan_* categories that used to fall through to EN).
    if "japan" in country or "日本" in blob or "japan" in cat or any(c in city for c in _JP_CITIES):
        return "ja"
    # Unknown: most of her targets are domestic Japanese, so default JA — never
    # silently default to English (that was the old bug).
    if any(c in blob for c in _EN_COUNTRIES) or "international" in blob:
        return "en"
    return "ja"


def skip_reason(opp: dict):
    """Return a string reason if NO email should be generated, else None."""
    blob = _blob(opp)
    deadline = opp.get("deadline") or ""

    # Already-closed calls — never draft a live application to a past deadline.
    try:
        if deadline and deadline_is_past(deadline):
            return f"deadline passed ({deadline})"
    except Exception:
        pass

    # Self-serve print-on-demand (SUZURI): you upload, there is no one to email.
    if any(k in blob for k in ("print-on-demand", "print on demand", "upload designs",
                               "artists upload", "self-serve", "you upload", "prints and ships")):
        return "self-serve print-on-demand (no email; make an account instead)"

    # Gallery-booth art fairs: only galleries exhibit; she has no representation.
    # (Exclude art/zine BOOK fairs, which take individual exhibitors.)
    is_book_fair = ("book fair" in blob or "art book" in blob or "zine" in blob)
    if not is_book_fair and ("art fair" in blob or "art_fair" in blob):
        if any(k in blob for k in ("galleries apply", "gallery applications", "gallery-booth",
                                   "by gallery", "represented artists", "only galleries", "exhibitor galleries")):
            return "gallery-booth fair (galleries enter, not individual artists)"

    return None


def slug(s):
    return re.sub(r"[^\w]+", "_", s.lower().strip(), flags=re.UNICODE).strip("_")


def find_analysis(name: str) -> str:
    if not ANALYSIS_DIR.exists():
        return ""
    key = slug(name)
    matches = sorted([f for f in ANALYSIS_DIR.iterdir() if key[:12] in f.stem], reverse=True)
    if matches:
        return matches[0].read_text(encoding="utf-8")[:2500]
    return ""


def pick_tone_action(opp: dict):
    cat = str(opp.get("category", "") or "")
    if cat in TONE_MAP:
        tone_key, action, n = TONE_MAP[cat]
    else:
        blob = _blob(opp)
        if any(k in blob for k in ("open call", "open-call", "competition", "award", "prize", "公募")):
            tone_key, action, n = ("professional", "open-call entry inquiry", 5)
        elif any(k in blob for k in ("cafe", "café", "coffee", "roaster")):
            tone_key, action, n = ("neighborly", "short-term exhibition inquiry", 3)
        else:
            tone_key, action, n = ("warm_professional", "introduction / inquiry", 5)
    return tone_key, action, n


def build_prompt(opp: dict, analysis: str, artist_context: str, lang: str, place_hint: str) -> str:
    name     = opp.get("name") or opp.get("title") or "Unknown"
    org      = opp.get("organization", "") or ""
    category = opp.get("category", "") or ""
    city     = opp.get("city", "") or ""
    country  = opp.get("country", "") or ""
    website  = opp.get("official_website", "") or opp.get("submission_page", "") or ""
    contact  = opp.get("contact", "") or ""
    deadline = opp.get("deadline", "") or ""
    overview = opp.get("overview", "") or opp.get("one_sentence", "") or ""
    why_fits = opp.get("why_it_fits", "") or opp.get("why_this_fits_short", "") or ""

    tone_key, action, max_sentences = pick_tone_action(opp)
    tone_desc = TONE_DESC.get(tone_key, "Professional and warm.")

    if lang == "ja":
        lang_instruction = (f"Write the email in NATURAL Japanese. Match keigo to the venue type "
                            f"({tone_desc}). Keep loanwords correct (委託販売／コンサインメント — NEVER 'コンスメント'). "
                            f"Subject line first, prefixed '件名: '. Limit the body to ~{max_sentences} sentences.")
    elif lang == "zh":
        lang_instruction = (f"用自然、温暖、得体的简体中文写这封邮件（{tone_desc}）。称呼与敬语要符合对方机构类型。"
                            f"第一行是主题，以'主题：'开头。正文控制在 ~{max_sentences} 句以内。")
    else:
        lang_instruction = (f"Write the email in NATURAL English ({tone_desc}). No sentence longer than ~30 words; "
                            f"break run-ons. Subject line first, prefixed 'Subject: '. Limit the body to ~{max_sentences} sentences.")

    extra = ""
    if overview:  extra += f"\nVenue (from real data): {overview}"
    if why_fits:  extra += f"\nWhy it may fit her: {why_fits}"
    if analysis:  extra += f"\n\nResearch notes:\n{analysis}"

    return f"""You are writing ONE real, immediately-sendable outreach email for GEGYjiji, a Tokyo-based Chinese watercolor illustrator.

## ARTIST
{artist_context}

## VENUE
Name: {name}{(' — ' + org) if org and org != name else ''}
Category: {category}
Location: {city}{(', ' + country) if country else ''}
Website: {website or '(none listed)'}
Contact: {contact or '(not listed)'}
Deadline: {deadline or '(none / rolling)'}{extra}

## TASK
Write a short, specific {action} from GEGYjiji to {name}.

{lang_instruction}

HARD RULES:
- OPENER: do NOT start with "I am writing to inquire/ask about…", "I am reaching out regarding…", or any throat-clear. Open with ONE true, specific detail about THIS venue (its neighbourhood, format, or programme), or a plain human line.
- NO INVENTED AESTHETIC: use only venue facts given above. If they are thin, open on a neutral verifiable fact (location, format, programme type). NEVER claim the venue is "quiet/intimate/champions X" unless the data says so. If the data WARNS against assuming a fit, do not assert the opposite.
- ONE practice-statement, phrased freshly. Describe her work as painting ORDINARY PLACES and the quiet atmosphere of everyday life — lead this draft with {place_hint}. Name a PLACE or its feeling in one natural sentence. Do NOT list objects or colours, and NEVER catalogue "red walls / alleyways / pools / green ponds" (赤い壁／路地／プール／緑の池) — an inventory of things reads like a form letter, not a person.
- NAME ONE work that fits: Colour Diary + the daily diary for zine/book/café/consignment; Tide from China for gallery/exhibition contexts. Don't dump her whole CV — a café needs only the diary + Colour Diary.
- DEADLINE: if a real FUTURE deadline is given above, mention it. Do not ask for information that is already public.
- Mention Instagram @gegyjiji (https://www.instagram.com/gegyjiji/) once, naturally. No Twitter/X. Leave a clean slot for her name + portfolio link at the sign-off.
- Render the venue's name in the email's own language; do not embed Japanese script inside an English sentence (or vice-versa).
- Plain text only. No markdown, asterisks, or [brackets]. NEVER use em dashes (— or ―); use commas, periods, or 、。 instead. Subject and body must agree (edition numbers, years). Sign off as: GEGYjiji

Output the email text only, nothing else."""


_GARBLE_FIXES = {"コンスメント": "コンサインメント"}


def lint_draft(draft: str, lang: str = "en") -> str:
    for bad, good in _GARBLE_FIXES.items():
        draft = draft.replace(bad, good)
    # No em dashes, ever (Scott's standing rule — they read as machine-written).
    sep = "、" if lang in ("ja", "zh") else ", "
    for dash in ("――", "—", "―"):
        draft = draft.replace(dash, sep)
    draft = draft.replace("、、", "、").replace(", ,", ",").replace("  ", " ")
    return draft


def _key(opp):
    return (opp.get("organization") or opp.get("name") or opp.get("title") or "").strip().lower()


def _section(opp):
    return opp.get("exclusive_primary_bucket") or opp.get("section") or opp.get("category") or ""


def select_targets(opps: list, master: dict, limit: int) -> list:
    """Top immediate-best-moves PLUS the top of every real section, deduped by
    organisation, with no-email venues (closed/self-serve/gallery-only) removed."""
    base = select_email_targets(opps, master, limit)

    eligible = [o for o in opps if _is_eligible(o) and _section(o) not in JUNK_SECTIONS]
    by_sec = {}
    for o in eligible:
        by_sec.setdefault(_section(o), []).append(o)
    section_tops = []
    for lst in by_sec.values():
        lst.sort(key=lambda x: float(x.get("overall_score") or 0), reverse=True)
        section_tops.extend(lst[:2])   # top 2 of each section

    out, seen = [], set()
    for o in base + section_tops:
        k = _key(o)
        if not k or k in seen:
            continue
        if skip_reason(o):
            continue
        seen.add(k)
        out.append(o)
    return out[:limit]


def call_claude(client, prompt: str) -> str:
    import anthropic
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=700,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


def _load_api_key():
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key and Path(".env").exists():
        for line in Path(".env").read_text(encoding="utf-8").splitlines():
            if line.startswith("ANTHROPIC_API_KEY="):
                key = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
    return key


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--dry", action="store_true", help="show targets + language, no API calls")
    args = parser.parse_args()

    opps   = json.loads(OPP_PATH.read_text(encoding="utf-8"))
    master = json.loads(PROFILE_PATH.read_text(encoding="utf-8")) if PROFILE_PATH.exists() else {}

    targets = select_targets(opps, master, args.limit)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Report what's being skipped, for transparency.
    skipped = [(o.get("name") or o.get("title"), skip_reason(o))
               for o in opps if _is_eligible(o) and _section(o) not in JUNK_SECTIONS and skip_reason(o)]

    if args.dry:
        print(f"Would write {len(targets)} drafts (top per section, deduped):\n")
        for i, o in enumerate(targets, 1):
            nm = (o.get("name") or o.get("title") or "?")[:46]
            print(f"  [{i:2d}] {nm:<46} {venue_language(o):>2} | {_section(o)}")
        print(f"\nSkipped {len(skipped)} no-email venues, e.g.:")
        for nm, why in skipped[:12]:
            print(f"  - {str(nm)[:46]:<46} {why}")
        return

    api_key = _load_api_key()
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not found."); sys.exit(1)
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    artist_context = load_artist_context()

    print(f"Writing {len(targets)} drafts (top per section); skipping {len(skipped)} no-email venues.")
    errors, written = 0, set()
    for i, opp in enumerate(targets, 1):
        name = opp.get("name") or opp.get("title") or "Unknown"
        lang = venue_language(opp)
        place_hint = PRACTICE_PLACES[(i - 1) % len(PRACTICE_PLACES)]
        print(f"  [{i:2d}/{len(targets)}] {name[:46]:<46} ({lang})", end=" ", flush=True)
        analysis = find_analysis(name)
        prompt = build_prompt(opp, analysis, artist_context, lang, place_hint)
        try:
            draft = lint_draft(call_claude(client, prompt), lang)
            opp["email_ja"] = opp.get("email_ja") or ""
            opp["email_en"] = opp.get("email_en") or ""
            opp["email_zh"] = opp.get("email_zh") or ""
            opp[f"email_{lang}"] = draft
            fname = f"ibm_{i:02d}_{slug(name)[:48]}.txt"
            (OUT_DIR / fname).write_text(draft, encoding="utf-8")
            written.add(fname)
            print("ok")
        except Exception as e:
            print(f"ERROR: {e}"); errors += 1
        time.sleep(0.25)

    # Prune stale drafts ONLY if we produced new ones — never leave the folder
    # empty because a run failed (e.g. out of API credits or a network error).
    if written:
        for f in OUT_DIR.glob("ibm_*.txt"):
            if f.name not in written:
                f.unlink()

    OPP_PATH.write_text(json.dumps(opps, ensure_ascii=False, indent=2), encoding="utf-8")
    if master.get("email_drafts_stale") and errors == 0:
        clear_drafts_stale(master)
        PROFILE_PATH.write_text(json.dumps(master, ensure_ascii=False, indent=2), encoding="utf-8")

    ok = len(targets) - errors
    print(f"\n{ok}/{len(targets)} drafts written -> {OUT_DIR}/ibm_*.txt")
    notify_discord(f"Draft regen: {ok}/{len(targets)} written" + (f", {errors} failed" if errors else ""),
                   status="success" if errors == 0 else "failure")


if __name__ == "__main__":
    main()
