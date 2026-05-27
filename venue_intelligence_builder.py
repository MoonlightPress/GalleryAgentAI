
import json, os, re
from collections import defaultdict
from datetime import date
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
VENUE_DIR = Path("memory/venues")
QUEUE_PATH = "memory/research_queue.json"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def slugify(text):
    text = str(text or "unknown").lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_") or "unknown"

def get_source(opp):
    return opp.get("source_link") or opp.get("source_url") or opp.get("official_website") or opp.get("submission_page") or ""

def venue_name_for(opp):
    return opp.get("organization") or opp.get("venue") or opp.get("title") or opp.get("name") or "Unknown Venue"

def category_label(raw):
    labels = {
        "zine_print": "Print / Zines / Bookstores",
        "bookstore_gallery": "Print / Zines / Bookstores",
        "bookstore_event": "Print / Zines / Bookstores",
        "cafe_gallery": "Cafe / Local Wall Spaces",
        "fair_popup": "Markets / Popups / Booths",
        "market_event": "Markets / Popups / Booths",
        "artist_space": "Artist Spaces",
        "event_space": "Artist Spaces",
        "gallery_event": "Galleries / Exhibition Calls",
        "gallery": "Galleries / Exhibition Calls",
        "residency": "Residencies / Longer Projects",
        "institutional": "Institutional / Grants",
    }
    return labels.get(raw, str(raw or "Other").replace("_", " ").title())

def infer_venue_type(opp):
    blob = (str(opp.get("category") or "") + " " + str(opp.get("title") or "")).lower()
    if "book" in blob or "zine" in blob or "print" in blob: return "bookstore / print space"
    if "cafe" in blob or "coffee" in blob: return "cafe wall / local exhibition space"
    if "market" in blob or "popup" in blob or "fair" in blob: return "market / popup / booth"
    if "residency" in blob: return "residency"
    if "gallery" in blob: return "gallery"
    return "artist opportunity venue"

def missing_fields_for(opp):
    missing = []
    if not get_source(opp): missing.append("official/source website")
    if not opp.get("submission_page"): missing.append("submission process")
    if not opp.get("deadline"): missing.append("deadline")
    if not opp.get("fees"): missing.append("fees")
    if not (opp.get("contact") or opp.get("email") or opp.get("contact_url")): missing.append("contact")
    return missing

def build_venue_record(name, opportunities):
    first = opportunities[0]
    source_links, categories, cities, missing = [], set(), set(), set()

    for opp in opportunities:
        source = get_source(opp)
        if source and source not in source_links: source_links.append(source)
        if opp.get("category"): categories.add(category_label(opp.get("category")))
        if opp.get("city"): cities.add(str(opp.get("city")))
        for item in missing_fields_for(opp): missing.add(item)

    return {
        "venue_name": name,
        "venue_slug": slugify(name),
        "venue_type": infer_venue_type(first),
        "city": ", ".join(sorted(cities)) if cities else "",
        "country": "",
        "website": source_links[0] if source_links else "",
        "source_links": source_links,
        "categories_seen": sorted(categories),
        "accepts_unsolicited_work": "unknown",
        "submission_style": "unknown",
        "typical_artists": [],
        "typical_mediums": [],
        "known_aesthetic": [],
        "price_level": "unknown",
        "risk_notes": [],
        "fit_notes": [],
        "verification_notes": ["Automatically created from opportunity data.", "Needs manual/web research before being treated as verified."],
        "missing_information": sorted(missing),
        "opportunity_titles": [opp.get("title") or opp.get("name") or "Unknown opportunity" for opp in opportunities],
        "last_researched": "",
        "created_at": date.today().isoformat(),
        "updated_at": date.today().isoformat()
    }

def main():
    opps = load_json(OPP_PATH, [])
    VENUE_DIR.mkdir(parents=True, exist_ok=True)

    grouped = defaultdict(list)
    for opp in opps:
        grouped[venue_name_for(opp)].append(opp)

    research_queue = []
    for name, items in grouped.items():
        record = build_venue_record(name, items)
        save_json(VENUE_DIR / f"{record['venue_slug']}.json", record)

        if record["missing_information"]:
            research_queue.append({
                "venue_name": record["venue_name"],
                "venue_slug": record["venue_slug"],
                "priority": "high" if len(record["missing_information"]) >= 3 else "medium",
                "missing": record["missing_information"],
                "recommended_action": "Research venue website or send inquiry draft.",
                "source": record["website"]
            })

    save_json(QUEUE_PATH, research_queue)
    print(f"Created/updated {len(grouped)} venue records.")
    print(f"Created research queue with {len(research_queue)} items.")

if __name__ == "__main__":
    main()
