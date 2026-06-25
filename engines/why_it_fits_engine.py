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
"""
import sys
import json
import os
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent))

from engines.profile_sync import follower_count_str

ROOT     = Path(__file__).parent.parent
OPP_PATH = ROOT / "deploy_data" / "compact_opportunities.json"
PROFILE_PATH = ROOT / "memory" / "artist_master_profile.json"

TARGET_BUCKETS = {
    "immediate_best_moves",
    "publication_targets",
    "japan_book_ecosystem",
    "stretch_targets",
    "relationship_builders",
}


def _follower_count() -> str:
    """Read her real follower count from the profile (never hardcode a literal).

    Falls back to the profile_sync default if the profile is missing/unreadable.
    """
    try:
        master = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    except Exception:
        master = {}
    return follower_count_str(master)


ARTIST_CONTEXT = """GEGYjiji — Chinese watercolor painter based in Tokyo.
Practice: Urban environments, architecture, memory, disappearing moments, quiet atmosphere.
Works: daily watercolor diary since 2020 ("diary" series), first solo collection Colour Diary (Oct 2021), first Japan group exhibition "Tide from China" (Feb 2023, ACG_Labo Harajuku).
Career stage: emerging, early Tier 2.
Style: quiet observation, architectural documentation, ordinary scenes transformed, atmospheric light.
Medium: watercolor on paper exclusively."""


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
    return False, ""


def build_prompt(opp: dict) -> str:
    title    = opp.get("title") or opp.get("name") or "Unknown"
    one_sent = opp.get("one_sentence") or ""
    category = opp.get("category") or opp.get("category_label") or ""
    city     = opp.get("city") or ""
    tags     = opp.get("tags") or []
    bucket   = opp.get("exclusive_primary_bucket") or ""
    why_old  = opp.get("why") or opp.get("why_this_fits_short") or ""
    tags_str = ", ".join(str(t) for t in tags if t)

    followers = _follower_count()

    return f"""You are writing a short note that the artist GEGYjiji will read about herself.
She is a Chinese watercolor painter in Tokyo. Her work: urban environments, architecture,
memory, disappearing moments, quiet atmosphere. Daily watercolor practice, {followers} Instagram
followers. Career stage: early Tier 2.

Venue/Opportunity: {title}
What it is: {one_sent}
Category: {category}
City: {city}
Bucket: {bucket}
Tags: {tags_str}
Previous why note: {why_old[:200] if why_old else '(none)'}

Write ONE to TWO sentences explaining specifically WHY this venue/opportunity fits HER practice.
- Address her directly in the SECOND PERSON ("you", "your work", "your daily diary"). Never write
  about her in the third person — never use "she", "her work" as if describing someone else, and
  never use her name "GEGYjiji" in the sentence.
- Be specific to this venue — mention what they actually do and why it connects to your work
- Reference watercolor, urban/architectural focus, or your daily practice where relevant
- Do NOT be generic ("a good fit for emerging artists")
- Do NOT repeat the one_sentence description word-for-word
- Do NOT start with "This" — start with the venue name or a specific aspect of the opportunity
- Do NOT use garbled phrases — use "watercolor" or "works on paper"
- NEVER mention internal taxonomy or system terms ("Tier 1", "Tier 2", "bucket", "immediate best
  moves", "stretch target", "score") — this copy is for her, not for the system.
- NEVER include meta-instructions, caveats to a reviewer, or verification notes (e.g.
  "建议在推荐前进行核实" / "verify before recommending" / "needs verification"). Output only the
  finished, her-facing sentence.
- If it's a grant: explain why the grant criteria match your practice specifically
- If it's a bookstore/zine: explain why your daily observation practice and printed work fits their curatorial identity
- If it's an art fair: explain the strategic fit or limitation honestly
- Keep it to 1-2 sentences maximum

Output the 1-2 sentences only, nothing else."""


def main():
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
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    import anthropic
    client = anthropic.Anthropic(api_key=api_key)

    opps = json.loads(OPP_PATH.read_text(encoding="utf-8"))

    targets = []
    for i, opp in enumerate(opps):
        bucket     = opp.get("exclusive_primary_bucket", "")
        visibility = opp.get("recommendation_visibility", "show")
        if bucket not in TARGET_BUCKETS:
            continue
        if visibility == "hidden":
            continue
        weak, reason = is_weak(opp)
        if weak:
            targets.append((i, opp, reason))

    if not targets:
        print("No weak why_this_fits_short entries found. Nothing to do.")
        return

    print(f"Found {len(targets)} entries with weak why_this_fits_short.")

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
                opps[opp_idx]["why_this_fits_short"] = new_why
                updated += 1
                print(f"ok")
            else:
                print("SKIPPED (empty response)")
        except Exception as e:
            print(f"ERROR: {e}")
            errors += 1

        time.sleep(0.3)

    OPP_PATH.write_text(json.dumps(opps, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDone. {updated}/{len(targets)} entries updated. {errors} errors.")


if __name__ == "__main__":
    main()
