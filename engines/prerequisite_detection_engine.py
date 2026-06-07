"""
prerequisite_detection_engine.py

Scans each opportunity's text for prerequisite signals and adds a
`prerequisites: []` array. Also hard-codes known prerequisites on
specific named opportunities (gallery fairs, prestige targets, etc.).
"""

import sys
import json
import os
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

OPP_PATH = "deploy_data/compact_opportunities.json"

# ---------------------------------------------------------------------------
# Signal detection rules
# ---------------------------------------------------------------------------

SIGNAL_RULES = {
    "gallery_representation": [
        "gallery application",
        "represented artists only",
        "by a gallery",
        "gallery representative",
        "must be represented",
        "gallery members only",
        "gallery applicants",
        "galleries only",
        "submitted by galleries",
    ],
    "invitation_only": [
        "invitation only",
        "by invitation",
        "invite only",
        "invitation-only",
        "invitational",
        "selected artists only",
        "curated selection only",
    ],
    "exhibition_credits_3": [
        "minimum 3 solo",
        "at least 3 exhibitions",
        "3+ shows",
        "minimum three solo",
    ],
    "exhibition_credits_5": [
        "minimum 5",
        "5+ exhibitions",
        "established artist",
        "substantial exhibition history",
    ],
    "publication_history": [
        "published artist",
        "publication history",
        "published work",
        "existing publications",
    ],
    "japanese_residency": [
        "japan resident",
        "residing in japan",
        "japanese resident",
        "japan-based only",
    ],
    "gallery_cv": [
        "exhibition cv",
        "professional cv",
        "full cv required",
        "exhibition record required",
    ],
}

# ---------------------------------------------------------------------------
# Hard-coded overrides — match by title.lower() or name.lower() substring
# ---------------------------------------------------------------------------

HARD_CODED = {
    "art sg 2026":                    ["gallery_representation"],
    "art sg":                         ["gallery_representation"],
    "tokyo gendai 2026":              ["gallery_representation"],
    "tokyo gendai":                   ["gallery_representation"],
    "art fair tokyo":                 ["gallery_representation"],
    "art vancouver 2026":             ["gallery_representation"],
    "art vancouver":                  ["gallery_representation"],
    "royal watercolour society":      ["exhibition_credits_5", "gallery_cv"],
    "american watercolor society":    ["exhibition_credits_5"],
    "asian cultural council":         ["exhibition_credits_3"],
    "asian cultural council fellowship": ["exhibition_credits_3"],
    "cité internationale des arts":   ["exhibition_credits_3"],
    "cite internationale des arts":   ["exhibition_credits_3"],
    "center for book arts":           ["publication_history"],
    "printed matter":                 ["publication_history"],
    "offprint":                       ["publication_history"],
    "mack":                           ["invitation_only"],
    "torch press":                    ["invitation_only"],
}


def build_text_blob(opp):
    parts = []
    for key in [
        "title", "name", "organization",
        "one_sentence", "why_this_fits_short",
        "quick_action", "confirmation_gate_note",
        "relationship_note",
    ]:
        val = opp.get(key)
        if val:
            parts.append(str(val))
    for item in opp.get("tags", []) or []:
        parts.append(str(item))
    return " ".join(parts).lower()


def detect_from_text(text):
    found = []
    for prereq, signals in SIGNAL_RULES.items():
        if any(s in text for s in signals):
            found.append(prereq)
    return found


def hard_coded_for(opp):
    title = str(opp.get("title") or opp.get("name") or "").lower()
    found = []
    for key, prereqs in HARD_CODED.items():
        if key in title:
            found.extend(prereqs)
    return found


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    opps = load_json(OPP_PATH, [])
    if not opps:
        print("No opportunities found — nothing to process.")
        return

    counter = Counter()
    with_prereqs = 0

    for opp in opps:
        text = build_text_blob(opp)
        detected = detect_from_text(text)
        hard = hard_coded_for(opp)

        merged = sorted(set(detected + hard))
        opp["prerequisites"] = merged
        opp["has_prerequisites"] = len(merged) > 0

        if merged:
            with_prereqs += 1
            for p in merged:
                counter[p] += 1

    save_json(OPP_PATH, opps)

    print(f"\nPrerequisite detection complete.")
    print(f"  Total opportunities processed : {len(opps)}")
    print(f"  Opportunities with prerequisites: {with_prereqs}")
    print(f"\nMost common prerequisites:")
    for prereq, count in counter.most_common():
        print(f"  {prereq}: {count}")

    # Spot-check named entries
    print("\nSpot-check (hard-coded entries):")
    check_names = [
        "art sg", "tokyo gendai", "art fair tokyo",
        "royal watercolour society", "american watercolor society",
        "asian cultural council", "cité internationale des arts",
        "center for book arts", "printed matter", "mack", "torch press",
    ]
    for opp in opps:
        title = str(opp.get("title") or opp.get("name") or "").lower()
        for cn in check_names:
            if cn in title:
                print(f"  {opp.get('title') or opp.get('name')}: {opp['prerequisites']}")
                break


if __name__ == "__main__":
    main()
