
import json
import os

OPP_PATH = "deploy_data/compact_opportunities.json"

TYPE_WEIGHTS = {
    "photobook_publisher": 1.2,
    "artist_book_fair": 1.1,
    "art_bookstore": 0.8,
    "photo_open_call": 0.7,
    "photo_publication": 0.9,
    "photo_festival": 0.7,
    "event_listing": 0.2,
}

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def main():
    opps = load_json(OPP_PATH, [])

    for opp in opps:
        stype = opp.get("source_type") or opp.get("category") or ""
        weight = TYPE_WEIGHTS.get(stype, 0)

        opp["source_type_weight"] = weight
        opp["overall_score"] = round(
            min(9.4, float(opp.get("overall_score", 0) or 0) + weight),
            2
        )

    opps.sort(key=lambda x: float(x.get("overall_score", 0) or 0), reverse=True)

    with open(OPP_PATH, "w", encoding="utf-8") as f:
        json.dump(opps, f, indent=2, ensure_ascii=False)

    print(f"Applied source type weights to {len(opps)} opportunities.")

if __name__ == "__main__":
    main()
