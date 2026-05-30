
import json
import os
from pathlib import Path
from random import shuffle

QUEUE_PATH = "memory/research_priority_queue.json"
OUT_PATH = "reports/daily_artist_quests.md"


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def main():

    queue = load_json(
        QUEUE_PATH,
        [],
    )

    shuffle(queue)

    quests = []

    for item in queue[:5]:

        quests.append(
            f"- Research {item.get('title')} submission process."
        )

    for item in queue[5:8]:

        quests.append(
            f"- Compare {item.get('title')} to similar institutions."
        )

    lines = [
        "# Daily Artist Quests",
        "",
        "Today's strategic tasks:",
        "",
    ]

    lines.extend(quests)

    Path(OUT_PATH).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    Path(OUT_PATH).write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(
        f"Wrote {OUT_PATH}"
    )


if __name__ == "__main__":
    main()
