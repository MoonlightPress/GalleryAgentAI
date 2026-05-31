
import json
from pathlib import Path

DNA = "memory/artist_dna.json"
FIT = "memory/artist_fit_scores.json"
EVIDENCE_CARDS = "memory/opportunity_evidence_cards.json"
TABF_VALIDATED = "memory/tabf_validated_entities.json"
PINPOINT_GRAPH = "memory/artist_career_graph.json"

OUT_JSON = "memory/career_channels.json"
OUT_REPORT = "reports/career_channels.md"

CHANNELS = {
    "zines": {
        "title": "Zines",
        "description": "Small printed works sold through zine shops, fairs, bookstores, and direct artist networks.",
        "why_it_fits": [
            "Low barrier to entry.",
            "Compatible with intimate watercolor and works-on-paper imagery.",
            "Lets the artist test audience response without waiting for gallery approval.",
            "Good bridge between prints, books, and small exhibitions."
        ],
        "fit_terms": ["zines", "prints", "small intimate works", "print and zine compatible imagery"],
        "opportunity_types": ["zine_shop", "zine_fair", "artist_book_store", "print_market"],
        "target_assets": ["1 finished zine", "20-50 printed copies", "short artist bio", "price sheet"],
    },
    "artist_books": {
        "title": "Artist Books",
        "description": "Sequenced art objects, small books, or book-like editions for fairs, bookstores, and publishers.",
        "why_it_fits": [
            "Strong fit for quiet observational work and visual sequencing.",
            "Raises the work above loose images or prints.",
            "Connects directly to TABF-style ecosystems.",
            "Can be shown to galleries, publishers, and shops."
        ],
        "fit_terms": ["artist books", "zines", "works on paper", "quiet observational work"],
        "opportunity_types": ["artist_book_fair", "artist_book_store", "small_press_publisher"],
        "target_assets": ["1 artist book prototype", "10-20 page sequence", "print-ready PDF", "mockup photos"],
    },
    "illustration_galleries": {
        "title": "Illustration Galleries",
        "description": "Galleries and competitions near illustration, picture books, small works, and publication culture.",
        "why_it_fits": [
            "Best bridge between watercolor images and formal exhibition.",
            "Better fit than traditional painting societies.",
            "Can lead to publishing or picture-book adjacent opportunities.",
            "Pinpoint-style opportunities already show evidence of similar artists."
        ],
        "fit_terms": ["watercolor", "illustration-adjacent galleries", "quiet contemporary galleries"],
        "opportunity_types": ["illustration_gallery", "bookstore_gallery", "quiet_contemporary_gallery"],
        "target_assets": ["portfolio PDF", "8-12 selected images", "short statement", "application materials"],
    },
    "small_press_publishers": {
        "title": "Small Press Publishers",
        "description": "Independent presses, artist-book publishers, and design/publishing studios.",
        "why_it_fits": [
            "Potential path for editions, books, and collaborations.",
            "More aligned with zines and artist books than generic gallery submissions.",
            "Can create international visibility through a small object.",
            "Useful even when no formal open call exists."
        ],
        "fit_terms": ["small press culture", "artist books", "zines", "prints"],
        "opportunity_types": ["small_press_publisher"],
        "target_assets": ["publisher shortlist", "sample PDF", "one-page pitch", "edition concept"],
    },
    "print_markets": {
        "title": "Print Markets",
        "description": "Markets, popups, and fairs where prints, small editions, postcards, and zines can be sold directly.",
        "why_it_fits": [
            "Immediate feedback from buyers.",
            "Good for testing which images people respond to.",
            "Can generate small but real income.",
            "Supports zines, prints, and local visibility."
        ],
        "fit_terms": ["prints", "small intimate works", "works on paper"],
        "opportunity_types": ["print_market", "zine_fair"],
        "target_assets": ["10 prints", "price list", "small display kit", "QR code / Instagram card"],
    },
    "social_platforms": {
        "title": "Instagram / TikTok",
        "description": "Audience-building and documentation channels, not the core career path by themselves.",
        "why_it_fits": [
            "Useful for showing process, new zines, shop placements, and exhibition visits.",
            "Should support real-world opportunities rather than replace them.",
            "Best used as proof-of-activity and relationship maintenance.",
            "Low cost, but easy to waste time if not tied to concrete goals."
        ],
        "fit_terms": ["visual archive", "process", "audience"],
        "opportunity_types": ["social_media"],
        "target_assets": ["10 post backlog", "3 process videos", "shop visit photos", "link page"],
    },
}

LOCAL_DENSITY_PLACEHOLDERS = {
    "zines": {
        "tokyo_known_target": 100,
        "koenji_target": 3,
        "nakano_target": 1,
        "radius_20km_target": 10,
        "note": "Targets are placeholders until local shop crawler is built."
    },
    "artist_books": {
        "tokyo_known_target": 40,
        "koenji_target": 1,
        "nakano_target": 1,
        "radius_20km_target": 8,
        "note": "Includes art book stores, book fairs, and publisher/bookstore hybrids."
    },
    "illustration_galleries": {
        "tokyo_known_target": 30,
        "koenji_target": 1,
        "nakano_target": 1,
        "radius_20km_target": 10,
        "note": "Prioritize illustration/picture-book/small-work galleries over formal painting societies."
    },
    "small_press_publishers": {
        "tokyo_known_target": 50,
        "koenji_target": 1,
        "nakano_target": 1,
        "radius_20km_target": 12,
        "note": "Includes indie publishers, risograph studios, and artist-book presses."
    },
    "print_markets": {
        "tokyo_known_target": 25,
        "koenji_target": 1,
        "nakano_target": 1,
        "radius_20km_target": 8,
        "note": "Includes fairs, popups, handmade markets, and design festa-style events."
    },
    "social_platforms": {
        "tokyo_known_target": None,
        "koenji_target": None,
        "nakano_target": None,
        "radius_20km_target": None,
        "note": "Not location-based. Use as amplification for real-world channel progress."
    },
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def collect_known_evidence():
    fit = load(FIT, [])
    cards = load(EVIDENCE_CARDS, [])
    tabf = load(TABF_VALIDATED, {})
    graph = load(PINPOINT_GRAPH, {})

    evidence = {
        "opportunities_by_type": {},
        "tabf_entities": tabf.get("validated_entities", []),
        "pinpoint_artists": graph.get("artists", []),
    }

    for row in fit:
        for typ in row.get("opportunity_types", []):
            evidence["opportunities_by_type"].setdefault(typ, []).append({
                "title": row.get("title"),
                "score": row.get("combined_personal_score"),
                "label": row.get("fit_label"),
            })

    return evidence

def build_channel(channel_id, cfg, evidence):
    opps = []
    for typ in cfg["opportunity_types"]:
        opps.extend(evidence["opportunities_by_type"].get(typ, []))

    # De-dupe opportunities.
    seen = set()
    deduped = []
    for o in opps:
        if o["title"] not in seen:
            seen.add(o["title"])
            deduped.append(o)

    density = LOCAL_DENSITY_PLACEHOLDERS[channel_id]

    known_entities = []
    if channel_id in {"zines", "artist_books", "small_press_publishers"}:
        for e in evidence["tabf_entities"]:
            if e.get("validated_type") in {"publisher_or_press", "art_book_fair", "zine_or_book", "gallery"}:
                known_entities.append({
                    "name": e.get("name"),
                    "type": e.get("validated_type"),
                    "score": e.get("validation_score"),
                })
    elif channel_id == "illustration_galleries":
        for a in evidence["pinpoint_artists"]:
            known_entities.append({
                "name": a.get("artist_name"),
                "type": "similar_artist",
                "score": None,
            })

    return {
        "channel_id": channel_id,
        "title": cfg["title"],
        "description": cfg["description"],
        "why_it_fits": cfg["why_it_fits"],
        "target_assets": cfg["target_assets"],
        "opportunity_types": cfg["opportunity_types"],
        "known_opportunities": deduped,
        "known_entities": known_entities[:15],
        "local_density_targets": density,
        "current_coverage_status": coverage_status(deduped, known_entities, density),
    }

def coverage_status(opps, entities, density):
    if len(opps) >= 5 or len(entities) >= 10:
        return "usable initial map"
    if len(opps) >= 2 or len(entities) >= 5:
        return "partial map"
    return "needs expansion"

def main():
    evidence = collect_known_evidence()
    channels = [build_channel(cid, cfg, evidence) for cid, cfg in CHANNELS.items()]

    priority = {
        "zines": 1,
        "artist_books": 2,
        "illustration_galleries": 3,
        "small_press_publishers": 4,
        "print_markets": 5,
        "social_platforms": 6,
    }
    channels.sort(key=lambda x: priority.get(x["channel_id"], 99))

    Path("memory").mkdir(exist_ok=True)
    json.dump(channels, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Career Channels",
        "",
        "Channel-level strategy view. Opportunities are leaves; channels are branches.",
        "",
    ]

    for c in channels:
        lines.append(f"## {c['title']}")
        lines.append(c["description"])
        lines.append("")
        lines.append(f"- Coverage status: {c['current_coverage_status']}")
        d = c["local_density_targets"]
        if d["tokyo_known_target"] is not None:
            lines.append(f"- Target map size: {d['tokyo_known_target']} Tokyo entries")
            lines.append(f"- Local target: {d['koenji_target']} Koenji, {d['nakano_target']} Nakano, {d['radius_20km_target']} within 20km of Koenji")
        lines.append("")
        lines.append("### Why this fits")
        for x in c["why_it_fits"]:
            lines.append(f"- {x}")
        lines.append("")
        lines.append("### Target assets")
        for x in c["target_assets"]:
            lines.append(f"- {x}")
        lines.append("")
        if c["known_opportunities"]:
            lines.append("### Known opportunities")
            for o in c["known_opportunities"][:8]:
                lines.append(f"- {o['title']} — {o.get('score')} — {o.get('label')}")
            lines.append("")
        if c["known_entities"]:
            lines.append("### Known ecosystem examples")
            for e in c["known_entities"][:10]:
                lines.append(f"- {e['name']} — {e['type']}")
            lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
