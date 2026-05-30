
import json
import os
from pathlib import Path

PATHS = {
    "opportunities": "deploy_data/compact_opportunities.json",
    "candidates": "ingestion/opportunity_candidates.json",
    "approved_candidates": "ingestion/approved_candidates.json",
    "rejected_candidates": "ingestion/rejected_candidates.json",
    "strategy_feed": "memory/strategy_feed.json",
    "fit_audit": "memory/fit_audit.json",
}


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def count_file(path):
    data = load_json(path, None)

    if isinstance(data, list):
        return len(data)

    if isinstance(data, dict):
        return len(data.keys())

    return "missing" if data is None else "exists"


def main():
    lines = ["# Pipeline Debug Summary", ""]

    for label, path in PATHS.items():
        lines.append(f"- {label}: {count_file(path)}")

    opps = load_json(PATHS["opportunities"], [])

    if opps:
        lines += ["", "## Top 15 Opportunities", ""]

        for opp in opps[:15]:
            lines.append(
                f"- {opp.get('title')} — {opp.get('overall_score')}/10 — "
                f"{opp.get('verification_status','')} — "
                f"{opp.get('url_verification_status','')} — "
                f"{opp.get('final_score_guard_note','')}"
            )

    approved = load_json(PATHS["approved_candidates"], [])
    rejected = load_json(PATHS["rejected_candidates"], [])

    lines += ["", "## Approved Candidate Sample", ""]

    for c in approved[:20]:
        lines.append(
            f"- {c.get('title')} — {c.get('overall_score')} — approved — "
            f"{', '.join(c.get('quality_gate_reasons', []))}"
        )

    lines += ["", "## Rejected Candidate Sample", ""]

    for c in rejected[:20]:
        lines.append(
            f"- {c.get('title')} — {c.get('overall_score')} — rejected — "
            f"{', '.join(c.get('quality_gate_reasons', []))}"
        )

    out = Path("reports/pipeline_debug_summary.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
