
import json
from pathlib import Path
from collections import defaultdict

SRC = "memory/artist_profiles.json"
OUT_JSON = "memory/artist_clusters.json"
OUT_REPORT = "reports/artist_clusters.md"

CLUSTERS = {
    "watercolor / works on paper": ["watercolor", "works_on_paper"],
    "illustration / picture books": ["illustrator", "picture_book_artist", "illustration", "children_books", "books"],
    "zines / artist books": ["zine_maker", "zines", "books", "publisher"],
    "gallery / exhibition path": ["gallery_artist", "exhibitor", "painting", "painter"],
    "award / selected artists": ["award_winner", "winner_or_selected_artist"],
    "judges / gatekeepers": ["judge"],
    "publishers / bookstores": ["publisher_or_bookstore", "publisher"],
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def profile_tokens(profile):
    return set(profile.get("roles", []) + profile.get("keywords", []))

def main():
    profiles = load(SRC, [])
    clusters = {name: [] for name in CLUSTERS}

    for p in profiles:
        tokens = profile_tokens(p)
        for cname, needed in CLUSTERS.items():
            if tokens.intersection(set(needed)):
                clusters[cname].append(p)

    result = []
    for cname, members in clusters.items():
        members.sort(key=lambda x: x.get("confidence", 0), reverse=True)
        result.append({
            "cluster": cname,
            "count": len(members),
            "artists": members[:30],
        })

    result.sort(key=lambda x: x["count"], reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(result, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Artist Clusters",
        "",
        "Groups historical entities into useful artist-career categories.",
        "",
    ]

    for c in result:
        lines.append(f"## {c['cluster']}")
        lines.append(f"- Count: {c['count']}")
        lines.append("")
        if c["artists"]:
            for a in c["artists"][:12]:
                lines.append(f"- {a['name']} — confidence {a.get('confidence')} — {', '.join(a.get('source_opportunities', []))}")
        else:
            lines.append("_No artists yet._")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
