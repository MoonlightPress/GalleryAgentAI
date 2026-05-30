
import json
import os
import re
from pathlib import Path
from collections import defaultdict

SCRAPED_PATHS = [
    "ingestion/scraped_pages.json",
    "ingestion/deep_crawl_results.json",
]

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "memory/publication_frequency.json"
REPORT_PATH = "reports/publication_frequency_report.md"

FREQUENCY_PATTERNS = {
    "annual": [
        "annual",
        "yearly",
        "every year",
        "once a year",
        "2024",
        "2025",
        "2026"
    ],
    "biannual": [
        "biannual",
        "biennial",
        "every two years",
        "biennale"
    ],
    "monthly": [
        "monthly",
        "each month",
        "every month"
    ],
    "rolling": [
        "rolling",
        "ongoing",
        "always open",
        "open year-round",
        "continuous"
    ],
    "periodic": [
        "periodic",
        "regularly",
        "from time to time",
        "seasonal"
    ]
}

PUBLICATION_WORDS = [
    "publish",
    "publication",
    "photobook",
    "artist book",
    "zine",
    "printed matter",
    "issue",
    "edition",
    "catalogue",
    "catalog",
    "magazine"
]


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def source_name(record):
    return record.get("source_name") or record.get("source") or record.get("title") or "Unknown"


def text_of(record):
    return (
        record.get("text")
        or record.get("text_excerpt")
        or ""
    )


def detect_frequency(text):
    lower = (text or "").lower()

    hits = {}

    for freq, patterns in FREQUENCY_PATTERNS.items():
        matched = [p for p in patterns if p in lower]
        if matched:
            hits[freq] = matched

    if not hits:
        return "unknown", {}

    # prefer explicit rolling/monthly/annual over vague periodic
    order = ["rolling", "monthly", "annual", "biannual", "periodic"]

    for key in order:
        if key in hits:
            return key, hits

    return list(hits.keys())[0], hits


def publication_strength(text):
    lower = (text or "").lower()
    hits = [w for w in PUBLICATION_WORDS if w in lower]
    return len(hits), hits


def main():
    records = []

    for path in SCRAPED_PATHS:
        records.extend(load_json(path, []))

    frequency = {}

    for record in records:
        name = source_name(record)
        text = text_of(record)

        freq, freq_hits = detect_frequency(text)
        pub_score, pub_hits = publication_strength(text)

        if name not in frequency:
            frequency[name] = {
                "source_name": name,
                "source_url": record.get("final_url") or record.get("source_url") or record.get("url") or "",
                "detected_frequency": freq,
                "frequency_evidence": freq_hits,
                "publication_signal_score": pub_score,
                "publication_terms": pub_hits,
                "confidence": "low"
            }
        else:
            current = frequency[name]
            if pub_score > current.get("publication_signal_score", 0):
                current["publication_signal_score"] = pub_score
                current["publication_terms"] = pub_hits
            if current.get("detected_frequency") == "unknown" and freq != "unknown":
                current["detected_frequency"] = freq
                current["frequency_evidence"] = freq_hits

    for item in frequency.values():
        if item["detected_frequency"] != "unknown" and item["publication_signal_score"] >= 3:
            item["confidence"] = "medium"
        if item["detected_frequency"] != "unknown" and item["publication_signal_score"] >= 6:
            item["confidence"] = "high"

    save_json(OUT_PATH, frequency)

    lines = [
        "# Publication Frequency Report",
        "",
        "This report estimates how often sources publish, open calls, or run relevant opportunities.",
        ""
    ]

    for name, item in sorted(frequency.items(), key=lambda x: x[1].get("publication_signal_score", 0), reverse=True):
        lines.append(f"## {name}")
        lines.append(f"- Frequency: {item.get('detected_frequency')}")
        lines.append(f"- Confidence: {item.get('confidence')}")
        lines.append(f"- Publication signal: {item.get('publication_signal_score')}")
        lines.append(f"- Terms: {', '.join(item.get('publication_terms', [])[:12])}")
        lines.append(f"- Source: {item.get('source_url')}")
        lines.append("")

    Path(REPORT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(REPORT_PATH).write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUT_PATH}")
    print(f"Wrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
