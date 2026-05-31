
import json
import re
from pathlib import Path
from urllib.parse import quote_plus

SRC = "memory/tabf_validated_entities.json"
OUT_JSON = "memory/tabf_contact_queue.json"
OUT_REPORT = "reports/tabf_contact_queue.md"

SEARCH_INTENTS = {
    "publisher_or_press": [
        "official website",
        "submissions",
        "artist books",
        "contact",
    ],
    "gallery": [
        "official website",
        "contact",
        "publications",
    ],
    "art_book_fair": [
        "official website",
        "exhibitors",
        "application",
        "contact",
    ],
    "zine_or_book": [
        "publisher",
        "official page",
        "artist book",
    ],
    "artist_or_collective": [
        "official website",
        "publications",
        "contact",
    ],
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def google_query_url(query):
    return "https://www.google.com/search?q=" + quote_plus(query)

def make_tasks(entity):
    name = entity.get("name")
    typ = entity.get("validated_type", "unknown")
    intents = SEARCH_INTENTS.get(typ, ["official website", "contact"])

    tasks = []
    for intent in intents:
        q = f'{name} {intent}'
        tasks.append({
            "entity": name,
            "entity_type": typ,
            "task": f"Find {intent} for {name}",
            "query": q,
            "search_url": google_query_url(q),
            "priority": priority(entity, intent),
        })
    return tasks

def priority(entity, intent):
    base = entity.get("validation_score", 0)
    if intent in {"official website", "contact"}:
        base += 10
    if entity.get("validated_type") == "publisher_or_press":
        base += 10
    return min(100, base)

def main():
    data = load(SRC, {})
    entities = data.get("validated_entities", [])

    # Only harvest meaningful entity types first.
    entities = [
        e for e in entities
        if e.get("validated_type") in {"publisher_or_press", "gallery", "art_book_fair", "artist_or_collective"}
    ]

    tasks = []
    for e in entities:
        tasks.extend(make_tasks(e))

    tasks.sort(key=lambda x: x["priority"], reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(tasks, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# TABF Contact Harvester Queue",
        "",
        "Manual/automated search queue for validated TABF ecosystem entities.",
        "",
        f"Tasks: {len(tasks)}",
        "",
    ]

    current = None
    for t in tasks[:120]:
        if t["entity"] != current:
            current = t["entity"]
            lines.append(f"## {current}")
        lines.append(f"- Priority {t['priority']}: {t['task']}")
        lines.append(f"  - Query: `{t['query']}`")
        lines.append(f"  - Search: {t['search_url']}")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Tasks:", len(tasks))

if __name__ == "__main__":
    main()
