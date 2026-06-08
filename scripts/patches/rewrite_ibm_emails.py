"""
rewrite_ibm_emails.py

Targeted rewrites for IBM email drafts that fail quality checks.
Only rewrites drafts that are:
- Wrong format for the venue type (e.g., inquiry email to a self-serve platform)
- Too generic / missing specific venue details
- Missing key artist identity (urban watercolor, daily practice, Instagram)

Run this after ibm_email_writer.py to fix specific problem drafts.

Usage:
    python scripts/patches/rewrite_ibm_emails.py
"""
import sys
import json
import os
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent.parent
OPP_PATH = ROOT / "deploy_data" / "compact_opportunities.json"
OUT_DIR = ROOT / "reports" / "inquiry_drafts"

# In a git worktree, shared repo may be parent's parent's parent
SHARED_REPO = ROOT.parent.parent.parent if "worktrees" in str(ROOT) else ROOT

ARTIST_CONTEXT = """Name: GEGYjiji (ジェジー / GEGY挤挤)
Instagram: @gegyjiji (https://www.instagram.com/gegyjiji/) (~90,000 followers, daily watercolor diary)
Based: Tokyo (originally from Hunan Province, China; Beijing Fashion Institute — illustration/design)

Key works:
- "Colour Diary (色彩日記)" — first solo illustration collection, Oct 2021.
  Grew directly from a daily watercolor diary practice she started in 2020.
- "Tide from China Part1" — first Japan exhibition, Feb 2023. Group show
  with 5 other Chinese illustrators at ACG_Labo, Harajuku, Tokyo.
- Daily watercolor diary ("diary") — ongoing since 2020.

Artist's own voice (from exhibition bio, ACG_Labo 2023):
  Japanese: 私たちは、あたりまえの生活の中に美しいものを見つけようとしています。
  Translation: We are trying to find beautiful things in our everyday life.

Practice: Quiet urban observation. Red walls, alleyways, green ponds, domestic interiors, seasonal light.
Architecture as memory. Daily seriality. Watercolor exclusively.
Career stage: Tier 1-2. Building exhibition history and relationships. No gallery representation."""

# Venues that need targeted rewrites
# Each entry: (filename, venue_name, category, what_they_do, what_to_write, lang)
REWRITES = [
    {
        "filename": "ibm_10_suzuri.txt",
        "venue": "SUZURI",
        "category": "print_on_demand_platform",
        "lang": "ja",
        "venue_desc": "SUZURI is a Japanese print-on-demand platform where artists upload original artwork and sell merchandise (T-shirts, tote bags, phone cases, stickers, etc.). It's self-serve — there is no inquiry process. Artists simply create an account and upload their work.",
        "action": "platform onboarding guide (not an email — write as practical setup notes for the artist herself, in Japanese, explaining how to approach SUZURI as a platform: what to set up, what works, what to list first)",
        "prompt_extra": "This is NOT an outreach email. SUZURI is a self-serve platform — you sign up directly. Write practical notes FOR the artist (GEGYjiji), in Japanese, explaining: (1) how to think about SUZURI as a revenue channel given her 90k Instagram audience, (2) what type of products to list first (stickers/posters likely best fit for watercolor), (3) how to connect her Instagram presence to her SUZURI shop. Keep it concise, practical, friendly. Start with: 【SUZURI 出品メモ】"
    },
    {
        "filename": "ibm_09_hattifnatt_koenji_cafe_gallery.txt",
        "venue": "HATTIFNATT Koenji",
        "category": "cafe_gallery",
        "lang": "ja",
        "venue_desc": "HATTIFNATT Koenji is a Koenji cafe gallery known for its storybook, fairytale aesthetic. They are well known for hosting exhibitions of work with warmth, intimacy, cats, whimsy, and soft illustration styles. The space itself has a hand-crafted, illustrated feel. They actively program local and independent artists whose work matches their storybook sensibility.",
        "action": "short-term exhibition inquiry email",
        "prompt_extra": "Write in Japanese (keigo, but warm and neighborly — not stiff). The opening should specifically reference HATTIFNATT's storybook / picture-book aesthetic, and make the connection explicit: her work features cats, interior light, quiet domestic and urban scenes — the same emotional register as their space. Reference both her daily diary practice and the cats that appear in her work. Keep it very short — cafe galleries don't want long emails. 3 short paragraphs max, ~100 words body. Sign off as GEGYjiji."
    }
]


def load_api_key():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        try:
            from dotenv import load_dotenv
            load_dotenv(ROOT / ".env")
            load_dotenv(SHARED_REPO / ".env")
            api_key = os.environ.get("ANTHROPIC_API_KEY")
        except ImportError:
            pass
    if not api_key:
        for env_path in [ROOT / ".env", SHARED_REPO / ".env"]:
            if env_path.exists():
                for line in env_path.read_text(encoding="utf-8").splitlines():
                    if line.startswith("ANTHROPIC_API_KEY="):
                        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break
            if api_key:
                break
    return api_key


def rewrite_draft(client, rewrite_spec: dict) -> str:
    venue = rewrite_spec["venue"]
    category = rewrite_spec["category"]
    lang = rewrite_spec["lang"]
    venue_desc = rewrite_spec["venue_desc"]
    action = rewrite_spec["action"]
    prompt_extra = rewrite_spec["prompt_extra"]

    lang_instruction = (
        "Write in Japanese only. Use appropriate keigo but keep it human and warm."
        if lang == "ja"
        else "Write in English only. Professional and concise."
    )

    prompt = f"""You are writing on behalf of GEGYjiji, a Tokyo-based Chinese watercolor artist.

## ARTIST PROFILE
{ARTIST_CONTEXT}

## VENUE
Name: {venue}
Category: {category}
What they do: {venue_desc}
What to write: {action}

## LANGUAGE
{lang_instruction}

## SPECIFIC INSTRUCTIONS
{prompt_extra}

## REQUIREMENTS (for email drafts only — skip if writing notes)
- Do NOT include placeholders like [link] or [date]
- Do NOT mention Twitter or X — Instagram @gegyjiji (https://www.instagram.com/gegyjiji/) only
- Do NOT use markdown formatting
- Subject line required as first line: "件名: " (Japanese) or "Subject: " (English)
- Sign off as: GEGYjiji
- Immediately sendable

Output only the final text, nothing else."""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


def slug(s):
    import re
    return re.sub(r"[^\w]+", "_", s.lower().strip(), flags=re.UNICODE).strip("_")


def main():
    api_key = load_api_key()
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    import anthropic
    client = anthropic.Anthropic(api_key=api_key)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Rewriting {len(REWRITES)} IBM email drafts...")
    print()

    updated = []

    for spec in REWRITES:
        venue = spec["venue"]
        fname = spec["filename"]
        print(f"  Rewriting: {fname} ({venue})...", end=" ", flush=True)

        try:
            new_text = rewrite_draft(client, spec)
            out_path = OUT_DIR / fname
            out_path.write_text(new_text, encoding="utf-8")
            print("ok")
            print(f"  Preview: {new_text[:150]}...")
            print()
            updated.append(fname)
        except Exception as e:
            print(f"ERROR: {e}")

        time.sleep(0.5)

    # Also update compact_opportunities.json email fields for these venues
    opps = json.loads(OPP_PATH.read_text(encoding="utf-8"))
    for spec in REWRITES:
        venue_name = spec["venue"]
        fname = spec["filename"]
        out_path = OUT_DIR / fname
        if not out_path.exists():
            continue
        draft_text = out_path.read_text(encoding="utf-8")
        lang = spec["lang"]

        for opp in opps:
            title = (opp.get("title") or opp.get("name") or "").lower()
            if venue_name.lower() in title or slug(venue_name)[:12] in slug(title)[:20]:
                if lang == "ja":
                    opp["email_ja"] = draft_text
                else:
                    opp["email_en"] = draft_text
                print(f"  Updated compact_opportunities.json for: {opp.get('title') or opp.get('name')}")

    OPP_PATH.write_text(json.dumps(opps, ensure_ascii=False, indent=2), encoding="utf-8")
    print()
    print(f"Done. {len(updated)} draft(s) rewritten: {', '.join(updated)}")


if __name__ == "__main__":
    main()
