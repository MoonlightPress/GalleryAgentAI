"""
fix_malformed_bullets.py

Detects entries where three_bullets[0] is a tag-like string (action type label
that was incorrectly stored as a bullet), clears the field, and regenerates
using the same rule-based fallback logic.
"""
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

OPP_PATH = Path(__file__).parent.parent.parent / "deploy_data" / "compact_opportunities.json"

# Import fallback logic from sibling script
sys.path.insert(0, str(Path(__file__).parent))
from generate_fallback_bullets import fallback_bullets


def _is_tag(s: str) -> bool:
    """True if s looks like a machine tag rather than readable bullet text."""
    if not isinstance(s, str):
        return False
    stripped = s.strip()
    if len(stripped) > 35:
        return False
    # Tags: no sentence punctuation, limited spaces, often snake_case or camelCase
    has_punct = any(c in stripped for c in ".,:!?")
    words = stripped.split()
    if has_punct and len(words) > 3:
        return False
    # Likely a tag if very short with underscore or all-lowercase few words
    if "_" in stripped:
        return True
    if len(words) <= 2 and stripped == stripped.lower():
        return True
    return False


def main():
    opps = json.loads(OPP_PATH.read_text(encoding="utf-8"))
    fixed = 0
    for opp in opps:
        bullets = opp.get("three_bullets") or []
        if bullets and _is_tag(bullets[0]):
            opp["three_bullets"] = fallback_bullets(opp)
            fixed += 1

    OPP_PATH.write_text(json.dumps(opps, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Fixed malformed bullets in {fixed} entries.")


if __name__ == "__main__":
    main()
