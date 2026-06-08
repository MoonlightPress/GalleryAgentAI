"""
add_japanese_opportunities.py

Adds 8 verified Japanese opportunities discovered via manual research:
- Suisai Renmei (watercolor federation open call)
- Suisaijin (transparent watercolor society)
- Watercolors 2026 (Tokyo Metropolitan Theatre)
- JIWI 26th International Watercolor Exhibition
- Ginza Chuo Gallery open call
- PARADISE AIR residency (Matsudo)
- ARCUS Project residency (Ibaraki)
- YUI-PORT residency (Niigata)

These will be picked up by approved_candidate_importer.py on the next pipeline run.
"""
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT     = Path(__file__).parent.parent.parent
OPP_PATH = ROOT / "ingestion" / "approved_candidates.json"

NEW_ENTRIES = [
    {
        "title": "水彩連盟展 (Suisai Renmei Exhibition) — Annual Open Call",
        "organization": "水彩連盟 (Suisai Renmei)",
        "category": "japan_watercolor_open_call",
        "city": "Tokyo",
        "country": "Japan",
        "overall_score": 8.0,
        "prestige_score": 7,
        "difficulty_score": 6,
        "confidence_level": "high",
        "verification_status": "verified",
        "source_type": "manual_research",
        "source_url": "https://www.artkoubo.jp/suisairenmei/",
        "official_website": "https://www.suisai-renmei.org/",
        "submission_page": "https://www.artkoubo.jp/suisairenmei/",
        "deadline": "Annual — 85th edition April 2026, next call expected late 2026",
        "fees": "Entry fee required — check current application",
        "one_sentence": "Annual open call by the Suisai Renmei watercolor federation at the National Art Center Roppongi — one of Japan's most respected dedicated watercolor societies.",
        "why_this_fits_short": "Dedicated to transparent watercolor at the National Art Center — directly suited to GEGYjiji's atmospheric, paper-based urban work at a Tier 3 credibility level.",
        "quick_action": "Check suisai-renmei.org for next annual call opening. Prepare 1-2 urban watercolor pieces in eligible format.",
        "three_bullets": [
            "Annual open call at National Art Center Roppongi",
            "One of Japan's most respected watercolor societies",
            "Accepts contemporary approaches alongside traditional work"
        ],
        "fit_keyword_hits": ["watercolor", "painting", "japan", "open_call", "institutional"],
        "reject_keyword_hits": [],
        "manual_review_needed": False,
        "missing_fields": ["exact_deadline"],
        "quality_gate_status": "approved",
        "quality_gate_reasons": ["watercolor-specific", "Japan institutional", "open call format"],
    },
    {
        "title": "水彩人展 (Suisaijin Exhibition) — Annual Transparent Watercolor Call",
        "organization": "水彩人 (Suisaijin)",
        "category": "japan_watercolor_open_call",
        "city": "Tokyo",
        "country": "Japan",
        "overall_score": 7.5,
        "prestige_score": 7,
        "difficulty_score": 5,
        "confidence_level": "high",
        "verification_status": "verified",
        "source_type": "manual_research",
        "source_url": "https://suisaijin.net/",
        "official_website": "https://suisaijin.net/",
        "submission_page": "https://suisaijin.net/",
        "deadline": "Annual September exhibition at Tokyo Metropolitan Art Museum",
        "fees": "Entry fee required — check current application",
        "one_sentence": "Annual watercolor-only exhibition at Tokyo Metropolitan Art Museum, focused on the richness and possibilities of transparent watercolor since 1999.",
        "why_this_fits_short": "Founded specifically to research transparent watercolor's possibilities — the conceptual framing matches GEGYjiji's exploratory, atmosphere-focused practice precisely.",
        "quick_action": "Check suisaijin.net for next annual application cycle (typically spring for September show).",
        "three_bullets": [
            "Annual transparent watercolor-specific society since 1999",
            "Tokyo Metropolitan Art Museum venue (Ueno)",
            "Conceptually serious — open to contemporary approaches"
        ],
        "fit_keyword_hits": ["watercolor", "painting", "japan", "open_call", "institutional"],
        "reject_keyword_hits": [],
        "manual_review_needed": False,
        "missing_fields": ["exact_deadline"],
        "quality_gate_status": "approved",
        "quality_gate_reasons": ["transparent watercolor specific", "Japan institutional", "open call"],
    },
    {
        "title": "Watercolors 2026 — Tokyo Metropolitan Theatre Open Exhibition",
        "organization": "日本文芸社 / Watercolors 2026 executive committee",
        "category": "japan_watercolor_open_call",
        "city": "Tokyo",
        "country": "Japan",
        "overall_score": 7.0,
        "prestige_score": 5,
        "difficulty_score": 3,
        "confidence_level": "high",
        "verification_status": "verified",
        "source_type": "manual_research",
        "source_url": "https://nihonbungei.net/watercolors_2026/",
        "official_website": "https://nihonbungei.net/watercolors_2026/",
        "submission_page": "https://nihonbungei.net/watercolors_2026/",
        "deadline": "Check nihonbungei.net/watercolors_2026/ for 2026 submission deadline",
        "fees": "Check current application",
        "one_sentence": "Watercolor-only public exhibition at Tokyo Metropolitan Theatre, open to all regardless of career level or credentials.",
        "why_this_fits_short": "Watercolor-only format shown at a landmark Tokyo venue — ideal for an emerging artist building early exhibition history with no credential barrier.",
        "quick_action": "Check nihonbungei.net/watercolors_2026/ for submission deadline and entry requirements.",
        "three_bullets": [
            "Watercolor-only — no other media accepted",
            "Tokyo Metropolitan Theatre (landmark venue)",
            "Open to all career levels — no credentials required"
        ],
        "fit_keyword_hits": ["watercolor", "japan", "open_call", "accessible"],
        "reject_keyword_hits": [],
        "manual_review_needed": False,
        "missing_fields": ["exact_deadline", "fees"],
        "quality_gate_status": "approved",
        "quality_gate_reasons": ["watercolor-only format", "accessible Tokyo venue"],
    },
    {
        "title": "第26回 国際水彩画展 (26th JIWI International Watercolor Exhibition)",
        "organization": "Japan International Watercolor Institute (JIWI)",
        "category": "japan_watercolor_open_call",
        "city": "Niigata",
        "country": "Japan",
        "overall_score": 6.5,
        "prestige_score": 5,
        "difficulty_score": 3,
        "confidence_level": "high",
        "verification_status": "verified",
        "source_type": "manual_research",
        "source_url": "https://iwf.iacn.jp/international-watercolor-exhibition-japan/",
        "official_website": "https://iwf.iacn.jp/",
        "submission_page": "https://iwf.iacn.jp/international-watercolor-exhibition-japan/",
        "deadline": "Annual — check iwf.iacn.jp for next cycle dates",
        "fees": "Check current application",
        "one_sentence": "International watercolor-only open call broadcast on YouTube and shown at Sado International Museum — designed for cross-border participation.",
        "why_this_fits_short": "International watercolor-only call with low barrier for a Chinese painter based in Japan — provides cross-border visibility for urban and atmospheric work.",
        "quick_action": "Check iwf.iacn.jp for next annual application cycle.",
        "three_bullets": [
            "International watercolor-only call from Japan",
            "YouTube broadcast gives global audience reach",
            "Low barrier for international artists based in Japan"
        ],
        "fit_keyword_hits": ["watercolor", "international", "japan", "open_call"],
        "reject_keyword_hits": [],
        "manual_review_needed": False,
        "missing_fields": ["exact_deadline", "fees"],
        "quality_gate_status": "approved",
        "quality_gate_reasons": ["watercolor-specific international", "accessible for China-based artists in Japan"],
    },
    {
        "title": "第6回銀座中央ギャラリー公募展 (6th Ginza Chuo Gallery Open Call)",
        "organization": "銀座中央ギャラリー (Ginza Chuo Gallery)",
        "category": "gallery",
        "city": "Tokyo",
        "country": "Japan",
        "overall_score": 7.0,
        "prestige_score": 5,
        "difficulty_score": 4,
        "confidence_level": "high",
        "verification_status": "verified",
        "source_type": "manual_research",
        "source_url": "https://chuogallery.com/events/2026/411/20260622koubo/index.html",
        "official_website": "https://chuogallery.com/",
        "submission_page": "https://chuogallery.com/events/2026/411/20260622koubo/index.html",
        "deadline": "Annual — 6th edition June 22-28 2026. Next cycle expected spring 2027.",
        "fees": "5000 JPY entry fee (post-selection)",
        "one_sentence": "Long-running Ginza gallery with annual juried open call that explicitly accepts watercolor at F4 scale with affordable entry.",
        "why_this_fits_short": "Explicitly accepts watercolor at intimate F4 scale in Ginza — suited to GEGYjiji's small-format daily diary work with a juried Ginza venue for CV.",
        "quick_action": "Monitor chuogallery.com for 2027 application opening. Prepare 1-2 F4 watercolor pieces.",
        "three_bullets": [
            "Ginza gallery with annual juried open call",
            "Explicitly accepts watercolor at F4 scale",
            "5,000 JPY entry — accessible and juried by gallery + public"
        ],
        "fit_keyword_hits": ["watercolor", "gallery", "tokyo", "ginza", "open_call"],
        "reject_keyword_hits": [],
        "manual_review_needed": False,
        "missing_fields": ["contact"],
        "quality_gate_status": "approved",
        "quality_gate_reasons": ["watercolor accepted", "Tokyo Ginza gallery", "accessible fee"],
    },
    {
        "title": "PARADISE AIR — Short Stay Artist Residency (Matsudo, Chiba)",
        "organization": "PARADISE AIR",
        "category": "residency",
        "city": "Matsudo",
        "country": "Japan",
        "overall_score": 7.0,
        "prestige_score": 5,
        "difficulty_score": 4,
        "confidence_level": "high",
        "verification_status": "verified",
        "source_type": "manual_research",
        "source_url": "https://www.paradiseair.info/en/opencall/",
        "official_website": "https://www.paradiseair.info/en/",
        "submission_page": "https://www.paradiseair.info/en/opencall/",
        "deadline": "Rolling open call — check paradiseair.info/en/opencall/ for current cycle",
        "fees": "None — accommodation provided",
        "one_sentence": "Open-genre artist residency 30 minutes from Tokyo in a working-class city district, with accommodation and exhibition venue.",
        "why_this_fits_short": "The everyday city-as-subject ethos and working-class Matsudo context directly fits GEGYjiji's urban observation practice — near Tokyo proximity keeps it practical.",
        "quick_action": "Check paradiseair.info/en/opencall/ for current open call. Submit portfolio with urban work and brief project proposal.",
        "three_bullets": [
            "Open-genre rolling call near Tokyo",
            "Accommodation + exhibition venue included",
            "Working-class urban district — ideal for city-observation watercolor"
        ],
        "fit_keyword_hits": ["residency", "japan", "urban", "rolling", "near_tokyo"],
        "reject_keyword_hits": [],
        "manual_review_needed": False,
        "missing_fields": [],
        "quality_gate_status": "approved",
        "quality_gate_reasons": ["open-genre residency near Tokyo", "practical for urban watercolor"],
    },
    {
        "title": "ARCUS Project 2027 — International Creator Artist-in-Residence (Ibaraki)",
        "organization": "ARCUS Project",
        "category": "residency",
        "city": "Moriya, Ibaraki",
        "country": "Japan",
        "overall_score": 8.0,
        "prestige_score": 8,
        "difficulty_score": 7,
        "confidence_level": "high",
        "verification_status": "verified",
        "source_type": "manual_research",
        "source_url": "https://www.arcus-project.com/en/news/open-call-2026/",
        "official_website": "https://www.arcus-project.com/en/",
        "submission_page": "https://www.arcus-project.com/en/news/open-call-2026/",
        "deadline": "Annual — 2026 cycle closed March 2026. Next 2027 cycle expected February 2027.",
        "fees": "None — fully funded (airfare + 540,000 JPY + studio)",
        "one_sentence": "Japan's most prominent fully-funded 90-day artist residency since 1994 near Tokyo for international visual artists.",
        "why_this_fits_short": "Fully-funded Japan residency accepting visual artists for serious production — the research-based city-observation format fits an urban architectural watercolor practice.",
        "quick_action": "Monitor arcus-project.com for 2027 cycle opening (expected February 2027). Review past residents to calibrate application.",
        "three_bullets": [
            "Japan's premier fully-funded residency — since 1994",
            "90 days with 540,000 JPY support + airfare + studio",
            "Strong institutional CV weight for Tier 3 career building"
        ],
        "fit_keyword_hits": ["residency", "japan", "funded", "institutional", "international"],
        "reject_keyword_hits": [],
        "manual_review_needed": False,
        "missing_fields": ["contact"],
        "quality_gate_status": "approved",
        "quality_gate_reasons": ["fully funded Japan residency", "institutional CV value", "visual artists accepted"],
    },
    {
        "title": "YUI-PORT Artist-in-Residence — Niigata Port City",
        "organization": "YUI-PORT (新潟市芸術創造村・国際青少年センター)",
        "category": "residency",
        "city": "Niigata",
        "country": "Japan",
        "overall_score": 6.5,
        "prestige_score": 5,
        "difficulty_score": 3,
        "confidence_level": "medium",
        "verification_status": "strong_partial",
        "source_type": "manual_research",
        "source_url": "https://www.yui-port.com/en/activities-offering.php",
        "official_website": "https://www.yui-port.com/en/",
        "submission_page": "https://www.yui-port.com/en/activities-offering.php",
        "deadline": "Rolling — short-stay and invitation programs, check yui-port.com for current openings",
        "fees": "None — free lodging provided",
        "one_sentence": "Open-genre artist residency with free lodging in Niigata port city, accepting all nationalities and mediums for short-stay and longer programs.",
        "why_this_fits_short": "Niigata's historic port-city architecture offers fresh material for a Tokyo-based urban painter — free lodging makes a short stay very low-barrier to attempt.",
        "quick_action": "Contact YUI-PORT via yui-port.com to inquire about short-stay availability. Prepare 5-10 urban watercolor portfolio images.",
        "three_bullets": [
            "Free lodging in historic Niigata port-city environment",
            "Open to all nationalities and media",
            "Short-stay option — low commitment, low cost entry point"
        ],
        "fit_keyword_hits": ["residency", "japan", "urban", "accessible", "rolling"],
        "reject_keyword_hits": [],
        "manual_review_needed": False,
        "missing_fields": ["contact", "exact_deadline"],
        "quality_gate_status": "approved",
        "quality_gate_reasons": ["Japan residency", "free lodging", "open-genre"],
    },
]


def main():
    existing = json.loads(OPP_PATH.read_text(encoding="utf-8"))
    print(f"Existing approved candidates: {len(existing)}")

    # Check for duplicates by title
    existing_titles = {e.get("title", "").lower() for e in existing}
    to_add = []
    for entry in NEW_ENTRIES:
        if entry["title"].lower() not in existing_titles:
            to_add.append(entry)
            print(f"  Adding: {entry['title'][:60]}")
        else:
            print(f"  Skip duplicate: {entry['title'][:60]}")

    combined = existing + to_add
    OPP_PATH.write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nAdded {len(to_add)} entries. Total: {len(combined)}")


if __name__ == "__main__":
    main()
