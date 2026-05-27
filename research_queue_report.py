
import json, os
from pathlib import Path

QUEUE_PATH = "memory/research_queue.json"
OUT_PATH = "reports/research_queue.md"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def main():
    queue = load_json(QUEUE_PATH, [])
    Path("reports").mkdir(exist_ok=True)
    lines = ["# Research Queue", "", "These are opportunities/venues with missing verification details.", ""]
    for item in queue:
        title = item.get("title") or item.get("venue_name") or "Unknown"
        lines.append(f"## {title}")
        lines.append(f"- Priority: {item.get('priority')}")
        if item.get("score") is not None: lines.append(f"- Score: {item.get('score')}")
        if item.get("organization"): lines.append(f"- Organization: {item.get('organization')}")
        if item.get("source"): lines.append(f"- Source: {item.get('source')}")
        lines.append(f"- Missing: {', '.join(item.get('missing', []))}")
        lines.append(f"- Recommended action: {item.get('recommended_action')}")
        lines.append("")
    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
