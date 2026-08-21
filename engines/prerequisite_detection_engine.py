"""
prerequisite_detection_engine.py

Scans each opportunity's text for prerequisite signals and adds a
`prerequisites: []` array. Also hard-codes known prerequisites on
specific named opportunities (gallery fairs, prestige targets, etc.).
"""

import sys
import json
import os
import re
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
    # Structural, not meetable-in-time: she is an individual artist. Found
    # 2026-07-27 — Tokyo Grant Category II (deadline 3 days out) surfaced as
    # actionable but is open to 団体 (organizations) only. The bucket engine
    # routes this signal to reject; the others keep their normal routing.
    "organizations_only": [
        "団体のみ",
        "団体に限る",
        "団体が対象",
        "個人は応募できません",
        "個人での応募は不可",
        "個人不可",
        "must be organizations",
        "organizations based in",
        "organizations only",
        "groups only",
        "individuals are ineligible",
        "individuals are not eligible",
        "npo法人・実行委員会が対象",
    ],
    # Participant age restriction — she is 26 and will never be a minor again.
    # NARROW on purpose: "children's illustration" is a GENRE she works in, not
    # an age limit, and student calls are explicitly kept (she IS a student —
    # Scott, 2026-06-19). Only phrasings that restrict WHO may enter match.
    "youth_only": [
        "青少年美术",
        "青少年絵画",
        "青少年アート",
        "青少年美術",
        "youth art competition",
        "youth art contest",
        "under 18",
        "18歳以下",
        "小中学生対象",
        "高校生以下",
        "ages 6-17",
        "ages 5-17",
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
        "eligibility",  # hand-verified restriction via manual_research — may
                        # state a constraint the scraped prose never mentioned
    ]:
        val = opp.get(key)
        if val:
            parts.append(str(val))
    for item in opp.get("tags", []) or []:
        parts.append(str(item))
    return " ".join(parts).lower()


# A contest FOR children, as opposed to the children's-book/illustration GENRE
# she actually works in. Plain substring matching cannot separate these: the
# 2026-08-21 miss was 第十七届花王国际儿童环境绘画大赛 / "17th Kao International
# Children's Environmental Painting Competition", where 環境/"Environmental"
# sits between the audience word and the medium word, so neither "儿童绘画" nor
# "children's painting competition" appears as a literal substring.
#
# The rule that separates them: children + a PAINTING/DRAWING contest means the
# children are the ENTRANTS. Children + book/picture-book/illustration means
# children are the AUDIENCE — Bologna Children's Book Fair is a real target for
# her and must never match.
_YOUNG      = r"(?:children'?s?|kids'?|儿童|兒童|児童|こども|子ども|子供)"
_PAINTING   = r"(?:painting|drawing|art)\s*(?:competition|contest|prize)|绘画大赛|繪畫大賽|絵画コンクール|画コンクール|絵画大会"
_GENRE_WORD = re.compile(r"(?:picture\s*book|children'?s?\s*book|絵本|児童書|繪本|illustration\s*(?:award|competition|contest|prize))")
_YOUTH_CONTEST_RE = re.compile(
    rf"{_YOUNG}[^。.;\n]{{0,40}}?(?:{_PAINTING})"
)


def _is_childrens_painting_contest(text):
    """True when the text describes a painting/drawing contest whose entrants
    are children. Genre mentions (children's book, picture book, illustration
    award) veto it — that is her actual working genre."""
    if _GENRE_WORD.search(text):
        return False
    return bool(_YOUTH_CONTEST_RE.search(text))


def detect_from_text(text):
    found = []
    for prereq, signals in SIGNAL_RULES.items():
        if any(s in text for s in signals):
            found.append(prereq)
    if "youth_only" not in found and _is_childrens_painting_contest(text):
        found.append("youth_only")
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
