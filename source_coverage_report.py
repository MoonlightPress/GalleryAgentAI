
import json
import os
from collections import Counter
from pathlib import Path

SOURCE_TARGETS_PATH = "source_targets.json"
ADVANCED_REGISTRY_PATH = "advanced_source_registry.json"
OUT_PATH = "reports/source_coverage_report.md"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def main():
    targets = load_json(SOURCE_TARGETS_PATH, {}).get("seed_sources", [])
    advanced = load_json(ADVANCED_REGISTRY_PATH, {}).get("priority_sources", [])

    all_sources = targets + advanced
    by_type = Counter(s.get("source_type") or s.get("type") or "unknown" for s in all_sources)
    by_region = Counter(s.get("region", "unknown") for s in all_sources)
    by_group = Counter(s.get("source_group", "ungrouped") for s in all_sources)

    lines = [
        "# Source Coverage Report",
        "",
        f"Total configured source entries: {len(all_sources)}",
        "",
        "## By Type",
        ""
    ]

    for k, v in by_type.most_common():
        lines.append(f"- {k}: {v}")

    lines += ["", "## By Region", ""]

    for k, v in by_region.most_common():
        lines.append(f"- {k}: {v}")

    lines += ["", "## By Group", ""]

    for k, v in by_group.most_common():
        lines.append(f"- {k}: {v}")

    lines += [
        "",
        "## Next Coverage Gaps",
        "",
        "- Add Korean photobook / independent publishing spaces.",
        "- Add Taiwan photography and artist-book spaces.",
        "- Add Chinese-language artist publication sources.",
        "- Add small European artist-run photography spaces.",
        "- Add Japanese independent gallery submission pages."
    ]

    Path(OUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(OUT_PATH).write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_PATH}")

if __name__ == "__main__":
    main()
