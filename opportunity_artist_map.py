
import json
from pathlib import Path
from collections import defaultdict

PROFILES = "memory/artist_profiles.json"
OUT_JSON = "memory/opportunity_artist_map.json"
OUT_REPORT = "reports/opportunity_artist_map.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    profiles = load(PROFILES, [])
    by_opp = defaultdict(list)

    for p in profiles:
        for opp in p.get("source_opportunities", []):
            by_opp[opp].append(p)

    rows = []
    for opp, artists in by_opp.items():
        artists.sort(key=lambda x: x.get("confidence", 0), reverse=True)
        rows.append({
            "title": opp,
            "artist_count": len(artists),
            "artists": artists[:20],
        })

    rows.sort(key=lambda x: x["artist_count"], reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(rows, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Opportunity Artist Map",
        "",
        "Shows which extracted artists/entities are associated with each opportunity.",
        "",
    ]

    for row in rows:
        lines.append(f"## {row['title']}")
        lines.append(f"- Artist/entity count: {row['artist_count']}")
        lines.append("")
        for a in row["artists"][:12]:
            roles = ", ".join(a.get("roles", []))
            kw = ", ".join(a.get("keywords", []))
            lines.append(f"- {a['name']} — {roles} — {kw or 'no keywords'}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
