"""
ibm_email_writer.py

Writes venue-specific email drafts for the top N Tier 1-2 IBM opportunities
using Claude API. Each draft references the venue's actual focus, names specific
works (Colour Diary, Tide from China), and matches tone to venue type.

Writes email_ja / email_en back to deploy_data/compact_opportunities.json
and saves standalone .txt files to reports/inquiry_drafts/ibm_*.txt.

Usage:
    python engines/ibm_email_writer.py
    python engines/ibm_email_writer.py --limit 10
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

OPP_PATH     = Path("deploy_data/compact_opportunities.json")
ANALYSIS_DIR = Path("Memory/generated_analysis")
OUT_DIR      = Path("reports/inquiry_drafts")

# ── Artist context loaded once ────────────────────────────────────────────────
ARTIST_CONTEXT = """
Name: GEGYjiji (ジェジー / 挤挤)
Twitter/X: @GegYjiji (~90,000 followers, illustration-community audience)
Instagram: @gegyjiji
Based: Tokyo (originally from China, Beijing Fashion Institute — illustration/design)

Key works:
• "Colour Diary (色彩日記)" — first solo illustration collection, Oct 2021.
  Grew directly from a daily watercolor diary practice she started in 2020.
• "Tide from China Part1" — first Japan exhibition, Feb 2023. Group show
  with 5 other Chinese illustrators at ACG_Labo, Harajuku, Tokyo.
• Daily watercolor diary — ongoing since 2020, posted to social media.

Visual world: urban atmospheres, Tokyo neighborhoods, domestic interiors, interior
light, cats, memory, quiet observation. Watercolor. Intimate scale. Transparency
and silence rather than drama. Cross-cultural seeing — a Chinese eye on Tokyo.

Career stage: Tier 1–2. Building exhibition history and relationships. No gallery
representation. First serious approach to zine/book/café venues.
""".strip()

# Category → (primary_lang, tone_key, action_phrase, max_sentences)
TONE_MAP = {
    "zine_shop_consignment": ("ja", "casual",           "consignment inquiry",                4),
    "bookstore_gallery":     ("ja", "warm_professional", "consignment or exhibition inquiry",  5),
    "bookstore_event":       ("ja", "warm_professional", "event or talk inquiry",              4),
    "cafe_gallery":          ("ja", "neighborly",        "short-term exhibition inquiry",      3),
    "zine_fair_booth":       ("ja", "application",       "booth application inquiry",          4),
    "fair_popup":            ("en", "professional",      "exhibitor application inquiry",      5),
    "gallery":               ("ja", "formal",            "submission / exhibition proposal",   6),
    "gallery_event":         ("en", "professional",      "open call submission",               5),
    "artist_space":          ("ja", "formal",            "space-use application",              5),
    "event_space":           ("ja", "formal",            "event participation inquiry",        5),
    "market_event":          ("ja", "warm_professional", "participation inquiry",              4),
}

TONE_DESC = {
    "casual":           "Casual and warm — fellow artists talking. No stiff honorifics.",
    "warm_professional":"Warm but professional. Respectful without being robotic.",
    "neighborly":       "Very brief, neighborly. Like a note left at the counter.",
    "application":      "Friendly and clear. State the practical info they need.",
    "professional":     "Professional and concise. Appropriate for first contact.",
    "formal":           "Professionally formal. Correct Japanese keigo or English register.",
}


def slug(s):
    return re.sub(r"[^\w]+", "_", s.lower().strip(), flags=re.UNICODE).strip("_")


def find_analysis(name: str) -> str:
    """Return the most recent generated_analysis file body for this venue."""
    if not ANALYSIS_DIR.exists():
        return ""
    key = slug(name)
    matches = sorted(
        [f for f in ANALYSIS_DIR.iterdir() if key[:12] in f.stem],
        reverse=True,
    )
    if matches:
        return matches[0].read_text(encoding="utf-8")[:2500]
    return ""


def is_international(opp: dict) -> bool:
    city    = str(opp.get("city", "") or "").lower()
    country = str(opp.get("country", "") or "").lower()
    japan_cities = {"tokyo", "東京", "osaka", "kyoto", "shimokitazawa", "koenji", "shimokitazawa, tokyo", ""}
    # Treat as domestic if city contains "tokyo" or country is "japan" or both empty
    if "tokyo" in city or "japan" in country:
        return False
    if not city and not country:
        return False  # assume Tokyo if unknown
    return city not in japan_cities or ("japan" not in country and country != "")


def build_prompt(opp: dict, analysis: str) -> tuple[str, str]:
    name     = opp.get("name") or opp.get("title") or "Unknown"
    category = opp.get("category", "gallery")
    city     = opp.get("city", "Tokyo") or "Tokyo"
    website  = opp.get("official_website", "") or ""
    contact  = opp.get("contact", "") or ""
    deadline = opp.get("deadline", "") or ""
    overview = opp.get("overview", "") or ""
    why_fits = opp.get("why_it_fits", "") or ""

    primary_lang, tone_key, action, max_sentences = TONE_MAP.get(
        category, ("en", "professional", "general inquiry", 5)
    )

    # Override language for clearly international venues
    if is_international(opp) and primary_lang == "ja":
        primary_lang = "en"

    tone_desc = TONE_DESC.get(tone_key, "Professional and warm.")

    lang_instruction = (
        f"Write the email in Japanese only. Use appropriate keigo but keep it human.\n"
        f"Limit to {max_sentences} sentences in the body (not counting subject line or sign-off)."
        if primary_lang == "ja"
        else
        f"Write the email in English only.\n"
        f"Limit to {max_sentences} sentences in the body (not counting subject line or sign-off)."
    )

    extra_context = ""
    if overview:
        extra_context += f"\nVenue description: {overview}"
    if why_fits:
        extra_context += f"\nWhy this fits the artist: {why_fits}"
    if analysis:
        extra_context += f"\n\nResearch notes:\n{analysis}"

    prompt = f"""You are writing a real outreach email on behalf of GEGYjiji, a Tokyo-based Chinese watercolor artist.

## ARTIST PROFILE
{ARTIST_CONTEXT}

## VENUE
Name: {name}
Category: {category}
City: {city}
Website: {website}
Contact: {contact if contact else "(not listed)"}
Deadline: {deadline if deadline else "(none / rolling)"}
{extra_context}

## TASK
Write a short, specific {action} email from GEGYjiji to {name}.
Tone: {tone_desc}

{lang_instruction}

Requirements:
- Open with something that shows you know this specific venue — their aesthetic, format, or reputation. Do NOT write generic praise like "I love your space."
- Name at least one specific work: "Colour Diary" or "Tide from China" — use whichever fits better for this venue type.
- Mention daily watercolor practice only if natural and brief (one clause, not a paragraph).
- Do NOT include a placeholder like [portfolio link] — mention "作品集" or "portfolio" naturally in one clause, linking to Instagram @gegyjiji or Twitter @GegYjiji.
- Do NOT use markdown, asterisks, or formatting marks — plain text only.
- Subject line is required as the first line, prefixed: "件名: " (Japanese) or "Subject: " (English).
- Sign off as: GEGYjiji
- The email must be immediately sendable — no [brackets], no instructions, no template language.

Output the email text only, nothing else.
"""
    return prompt, primary_lang


def call_claude(client, prompt: str) -> str:
    import anthropic
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=700,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    # Load API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.environ.get("ANTHROPIC_API_KEY")
        except ImportError:
            pass
    if not api_key:
        # Try reading .env directly
        env_path = Path(".env")
        if env_path.exists():
            for line in env_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("ANTHROPIC_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    import anthropic
    client = anthropic.Anthropic(api_key=api_key)

    opps = json.loads(OPP_PATH.read_text(encoding="utf-8"))

    # Build index for fast lookup
    opp_index = {o.get("id", ""): i for i, o in enumerate(opps)}

    # Top N Tier 1-2 by score
    tier12 = [o for o in opps if o.get("career_tier") in (1, 2)]
    tier12.sort(key=lambda x: float(x.get("overall_score") or 0), reverse=True)
    targets = tier12[: args.limit]

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Writing Claude-generated email drafts for top {len(targets)} IBM opportunities...")
    errors = 0

    for i, opp in enumerate(targets, 1):
        name = opp.get("name") or opp.get("title") or "Unknown"
        print(f"  [{i:2d}/{len(targets)}] {name[:50]:<50}", end=" ", flush=True)

        analysis = find_analysis(name)
        prompt, lang = build_prompt(opp, analysis)

        try:
            draft = call_claude(client, prompt)

            # Store in correct field
            if lang == "ja":
                opp["email_ja"] = draft
                opp["email_en"] = opp.get("email_en") or ""
            else:
                opp["email_en"] = draft
                opp["email_ja"] = opp.get("email_ja") or ""
            opp["email_zh"] = opp.get("email_zh") or ""

            # Write standalone file (overwrites old template version)
            fname = f"ibm_{i:02d}_{slug(name)[:48]}.txt"
            (OUT_DIR / fname).write_text(draft, encoding="utf-8")
            print(f"ok ({lang})")
        except Exception as e:
            print(f"ERROR: {e}")
            errors += 1

        time.sleep(0.25)

    # Write results back
    OPP_PATH.write_text(json.dumps(opps, ensure_ascii=False, indent=2), encoding="utf-8")
    ok_count = len(targets) - errors
    print(f"\n{ok_count}/{len(targets)} drafts written.")
    print(f"Standalone files: {OUT_DIR}/ibm_*.txt")
    print(f"email_ja / email_en fields updated in compact_opportunities.json")


if __name__ == "__main__":
    main()
