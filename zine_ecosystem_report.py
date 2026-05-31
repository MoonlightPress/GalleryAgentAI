
import json
from pathlib import Path
from collections import Counter, defaultdict

SRC = "memory/zine_ecosystem_seed.json"
OUT_JSON = "memory/zine_ecosystem_summary.json"
OUT_REPORT = "reports/zine_ecosystem.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    data = load(SRC, {})
    items = data.get("seed_opportunities", [])
    target = data.get("target_total", 100)

    by_category = Counter(x["category"] for x in items)
    by_area = Counter(x["area"] for x in items)
    by_status = Counter(x["status"] for x in items)

    coverage = round(len(items) / target * 100, 1)

    summary = {
        "target_total": target,
        "known_count": len(items),
        "coverage_percent": coverage,
        "by_category": dict(by_category),
        "by_area": dict(by_area),
        "by_status": dict(by_status),
        "highest_leverage_gap": "Local Tokyo zine/book shops are under-mapped. Build Koenji/Nakano/Shimokitazawa coverage next.",
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(summary, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Zine Ecosystem",
        "",
        f"- Known entries: {len(items)}",
        f"- Target entries: {target}",
        f"- Coverage: {coverage}%",
        "",
        "## Highest Leverage Gap",
        summary["highest_leverage_gap"],
        "",
        "## By Category",
        "",
    ]

    for k, v in by_category.most_common():
        lines.append(f"- {k}: {v}")

    lines += ["", "## By Area", ""]
    for k, v in by_area.most_common():
        lines.append(f"- {k}: {v}")

    lines += ["", "## By Status", ""]
    for k, v in by_status.most_common():
        lines.append(f"- {k}: {v}")

    lines += ["", "## Current Best Targets", ""]
    for x in items[:20]:
        lines.append(f"- {x['name']} — {x['category']} — {x['status']}")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
