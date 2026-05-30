
import json
import os
from pathlib import Path

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_PATH = "reports/social_proof_strategy.md"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def prestige(opp):
    return float(
        opp.get(
            "prestige_score",
            0
        ) or 0
    )

def main():

    opps = load_json(
        OPP_PATH,
        []
    )

    top = sorted(
        opps,
        key=prestige,
        reverse=True,
    )[:25]

    lines = [
        "# Social Proof Strategy",
        "",
        "These opportunities may create disproportionate reputation value.",
        "",
    ]

    for opp in top:

        title = opp.get(
            "title",
            "Unknown"
        )

        lines.append(
            f"## {title}"
        )

        lines.append("")

        lines.append(
            f"- Prestige: {opp.get('prestige_score')}"
        )

        lines.append(
            f"- Why: {opp.get('why_this_fits_short','')}"
        )

        lines.append(
            "- Strategic Value: "
            "Even a small relationship here may create downstream legitimacy."
        )

        lines.append("")

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
