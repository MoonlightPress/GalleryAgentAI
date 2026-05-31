
import json
from pathlib import Path

SRC = "memory/artist_profiles.json"
BIOS = "memory/artist_biographies.json"
OUT_JSON = "memory/real_artist_profiles.json"
OUT_REPORT = "reports/real_artist_profiles.md"

BAD_TERMS = [
    "Award", "Prize", "Exhibition", "Gallery", "Society", "Competition", "Book Fair",
    "Institute", "Association", "Open Calls", "Annual Exhibition", "Foundation",
    "Federation", "Application", "Contact", "Privacy", "Policy", "Menu", "Schedule",
    "Newsletter", "Copyright", "Event Hire", "Venue Hire", "Art Gallery", "Visual Arts",
    "Value", "The ", "Year Award"
]

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def is_bad_name(name):
    if not name:
        return True
    if any(term.lower() in name.lower() for term in BAD_TERMS):
        return True
    if name.isupper():
        return True
    if len(name) < 3 or len(name) > 40:
        return True
    return False

def main():
    profiles = load(SRC, [])
    bios = load(BIOS, [])

    bio_names = {b["artist_name"] for b in bios}
    filtered = []

    for p in profiles:
        name = p.get("name")
        if is_bad_name(name):
            continue

        # Strongly prefer names confirmed by biography extractor.
        p = dict(p)
        p["biography_confirmed"] = name in bio_names
        if p["biography_confirmed"] or p.get("confidence", 0) >= 0.8:
            filtered.append(p)

    # Add bios that may not have profile rows.
    existing = {p.get("name") for p in filtered}
    for b in bios:
        if b["artist_name"] not in existing:
            filtered.append({
                "name": b["artist_name"],
                "source_opportunities": [b["source_opportunity"]],
                "source_urls": [b["source_url"]] if b.get("source_url") else [],
                "roles": b["roles"],
                "keywords": ["books"] if b["books_or_work_titles"] else [],
                "confidence": b["confidence"],
                "biography_confirmed": True,
                "evidence": [b["bio_text"]],
            })

    filtered.sort(key=lambda x: (x.get("biography_confirmed", False), x.get("confidence", 0)), reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(filtered, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Real Artist Profiles",
        "",
        "Filtered profile list, removing awards, organizations, and navigation fragments.",
        "",
        f"Total real-ish profiles: {len(filtered)}",
        "",
    ]

    for p in filtered:
        lines.append(f"## {p.get('name')}")
        lines.append(f"- Biography confirmed: {p.get('biography_confirmed')}")
        lines.append(f"- Confidence: {p.get('confidence')}")
        lines.append(f"- Roles: {', '.join(p.get('roles', []))}")
        lines.append(f"- Source opportunities: {', '.join(p.get('source_opportunities', []))}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Filtered profiles:", len(filtered))

if __name__ == "__main__":
    main()
