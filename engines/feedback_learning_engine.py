
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
REL_PATH = "memory/relationship_memory.json"
LEARNED_PROFILE_PATH = "memory/learned_artist_preferences.json"
FEEDBACK_REPORT_PATH = "reports/feedback_learning_report.md"


POSITIVE_STATES = {
    "interested",
    "submitted",
    "waiting",
    "follow_up",
    "conversation_started",
    "soft_relationship",
    "strong_relationship",
}

NEGATIVE_STATES = {
    "rejected",
    "archived",
}


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def title_of(opp):
    return opp.get("title") or opp.get("name") or "Unknown"


def tokens_from_opp(opp):
    tokens = []

    for key in [
        "category",
        "category_label",
        "city",
        "country",
        "source_type",
        "verification_status",
        "research_priority",
    ]:
        value = opp.get(key)
        if value:
            tokens.append(f"{key}:{str(value).lower()}")

    for tag in opp.get("tags", []):
        tokens.append(f"tag:{str(tag).lower()}")

    text_fields = [
        opp.get("one_sentence", ""),
        opp.get("why_this_fits_short", ""),
        " ".join(str(x) for x in opp.get("three_bullets", [])),
    ]

    keywords = [
        "photobook",
        "zine",
        "artist book",
        "gallery",
        "cafe",
        "residency",
        "grant",
        "publication",
        "printed matter",
        "international",
        "community",
        "bookstore",
        "quiet",
        "memory",
        "architecture",
        "place",
        "daily",
        "atmospheric",
        "photography",
    ]

    blob = " ".join(text_fields).lower()

    for word in keywords:
        if word in blob:
            tokens.append(f"keyword:{word}")

    return tokens


def build_lookup(opps):
    return {title_of(opp): opp for opp in opps}


def main():
    opps = load_json(OPP_PATH, [])
    memory = load_json(REL_PATH, {})

    lookup = build_lookup(opps)

    positive = Counter()
    negative = Counter()

    positive_titles = []
    negative_titles = []

    for title, rel in memory.items():
        opp = lookup.get(title)
        if not opp:
            continue

        state = rel.get("state", "unseen")
        favorite = rel.get("favorite", False)
        interest = float(rel.get("interest_level", 0) or 0)

        tokens = tokens_from_opp(opp)

        if state in POSITIVE_STATES or favorite or interest >= 7:
            positive_titles.append(title)
            for token in tokens:
                positive[token] += 1 + int(interest // 3)

        if state in NEGATIVE_STATES:
            negative_titles.append(title)
            for token in tokens:
                negative[token] += 1

    learned = {
        "positive_titles": positive_titles,
        "negative_titles": negative_titles,
        "positive_signals": positive.most_common(40),
        "negative_signals": negative.most_common(40),
        "preference_weights": {},
    }

    all_tokens = set(positive.keys()) | set(negative.keys())

    for token in all_tokens:
        learned["preference_weights"][token] = round(
            positive[token] * 0.45 - negative[token] * 0.65,
            2,
        )

    save_json(LEARNED_PROFILE_PATH, learned)

    lines = [
        "# Feedback Learning Report",
        "",
        "This report summarizes what the system has learned from saved, rejected, interested, submitted, or relationship-tracked opportunities.",
        "",
        "## Positive Signals",
        "",
    ]

    for token, count in positive.most_common(20):
        lines.append(f"- {token}: {count}")

    lines += ["", "## Negative Signals", ""]

    for token, count in negative.most_common(20):
        lines.append(f"- {token}: {count}")

    lines += ["", "## Positive Titles", ""]

    for title in positive_titles:
        lines.append(f"- {title}")

    lines += ["", "## Negative Titles", ""]

    for title in negative_titles:
        lines.append(f"- {title}")

    Path(FEEDBACK_REPORT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(FEEDBACK_REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Learned {len(learned['preference_weights'])} preference weights.")
    print(f"Wrote {LEARNED_PROFILE_PATH}")
    print(f"Wrote {FEEDBACK_REPORT_PATH}")


if __name__ == "__main__":
    main()
