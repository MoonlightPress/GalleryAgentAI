
import json
from pathlib import Path

CHANNELS = "memory/career_channels.json"
OUT_JSON = "memory/career_battle_plans.json"
OUT_REPORT = "reports/career_battle_plans.md"

BATTLE_PLANS = {
    "zines": {
        "maximum_impact": "Place one finished zine in 3-5 local shops and use those placements as proof-of-activity.",
        "60_day_goal": "Print 20 copies and secure 1-3 shop placements.",
        "phases": [
            {
                "phase": "Build the object",
                "tasks": [
                    "Select one coherent theme.",
                    "Choose 12-20 images or pages.",
                    "Make one finished zine PDF.",
                    "Print 20 test copies."
                ]
            },
            {
                "phase": "Local placement",
                "tasks": [
                    "Map 3 Koenji shops, 1 Nakano shop, and 10 nearby shops.",
                    "Visit the nearest 3 with one sample copy.",
                    "Ask whether they accept consignment, small press zines, or artist books.",
                    "Track response status."
                ]
            },
            {
                "phase": "Expansion",
                "tasks": [
                    "Approach 5 additional shops.",
                    "Prepare a short bilingual description.",
                    "Post only after a placement or real action occurs."
                ]
            }
        ],
        "metrics": [
            "shops researched",
            "shops visited",
            "copies placed",
            "copies sold",
            "follow-up dates"
        ]
    },
    "artist_books": {
        "maximum_impact": "Turn the strongest body of work into one artist-book prototype, then use it for TABF-style applications.",
        "60_day_goal": "Create one prototype and compare it against 5 similar artist books.",
        "phases": [
            {
                "phase": "Prototype",
                "tasks": [
                    "Choose one body of work.",
                    "Create a 10-20 page sequence.",
                    "Export a print-ready PDF.",
                    "Photograph the mockup."
                ]
            },
            {
                "phase": "Benchmark",
                "tasks": [
                    "Find 5 comparable artist books.",
                    "Note size, price, page count, binding, and presentation.",
                    "Identify what makes her object distinct."
                ]
            },
            {
                "phase": "Applications",
                "tasks": [
                    "Prepare TABF application materials.",
                    "Shortlist 3 artist-book fairs or bookstores.",
                    "Prepare one concise project statement."
                ]
            }
        ],
        "metrics": [
            "prototype completed",
            "comparable books reviewed",
            "applications prepared",
            "stores/fairs researched"
        ]
    },
    "illustration_galleries": {
        "maximum_impact": "Use Pinpoint-style opportunities as the formal exhibition bridge.",
        "60_day_goal": "Prepare one strong PDF and submit to the best-fit illustration/gallery opportunity.",
        "phases": [
            {
                "phase": "Portfolio",
                "tasks": [
                    "Select 8-12 strongest works.",
                    "Order them into a coherent visual sequence.",
                    "Write a 100-word artist statement.",
                    "Create one PDF portfolio."
                ]
            },
            {
                "phase": "Fit check",
                "tasks": [
                    "Review 10 artists from Pinpoint or similar galleries.",
                    "Compare medium, tone, subject, and presentation.",
                    "Decide whether the opportunity is truly similar or only adjacent."
                ]
            },
            {
                "phase": "Submission",
                "tasks": [
                    "Confirm deadline and fee.",
                    "Prepare application images.",
                    "Submit or mark as not worth it."
                ]
            }
        ],
        "metrics": [
            "portfolio completed",
            "artists reviewed",
            "applications submitted",
            "responses received"
        ]
    },
    "small_press_publishers": {
        "maximum_impact": "Build a shortlist of publishers who actually handle artist books, zines, or illustration-adjacent editions.",
        "60_day_goal": "Research 20, shortlist 5, contact 2.",
        "phases": [
            {
                "phase": "Research",
                "tasks": [
                    "Collect 20 publishers/presses.",
                    "Tag each by country, style, openness, and contact method.",
                    "Reject generic or poor-fit publishers."
                ]
            },
            {
                "phase": "Shortlist",
                "tasks": [
                    "Choose 5 that match her work.",
                    "Find comparable artists/books they published.",
                    "Prepare one specific reason for each."
                ]
            },
            {
                "phase": "Contact",
                "tasks": [
                    "Send 2 careful emails.",
                    "Attach portfolio or artist-book PDF only when appropriate.",
                    "Track responses."
                ]
            }
        ],
        "metrics": [
            "publishers researched",
            "publishers shortlisted",
            "emails sent",
            "responses received"
        ]
    },
    "print_markets": {
        "maximum_impact": "Test which images people will buy before investing too much in large editions.",
        "60_day_goal": "Prepare 10 prints and test one small market or popup.",
        "phases": [
            {
                "phase": "Product test",
                "tasks": [
                    "Select 10 works.",
                    "Make small print editions.",
                    "Set prices.",
                    "Prepare basic packaging."
                ]
            },
            {
                "phase": "Market test",
                "tasks": [
                    "Find 5 local print/zine/design markets.",
                    "Choose one realistic event.",
                    "Prepare table/display checklist."
                ]
            }
        ],
        "metrics": [
            "prints prepared",
            "markets researched",
            "events applied to",
            "sales"
        ]
    },
    "social_platforms": {
        "maximum_impact": "Use social platforms to document real progress, not as a substitute for career actions.",
        "60_day_goal": "Create a simple posting system tied to zines, shop visits, and finished work.",
        "phases": [
            {
                "phase": "Content base",
                "tasks": [
                    "Prepare 10 image posts.",
                    "Prepare 3 process videos.",
                    "Prepare 3 shop/zine/story posts."
                ]
            },
            {
                "phase": "Tie to real actions",
                "tasks": [
                    "Post when a zine is printed.",
                    "Post when a shop visit happens.",
                    "Post when a piece is placed or exhibited."
                ]
            }
        ],
        "metrics": [
            "posts prepared",
            "process videos prepared",
            "real-world actions documented",
            "portfolio link clicks"
        ]
    },
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    channels = load(CHANNELS, [])
    plans = []

    for c in channels:
        bp = BATTLE_PLANS.get(c["channel_id"], {})
        plans.append({
            "channel_id": c["channel_id"],
            "title": c["title"],
            "coverage_status": c.get("current_coverage_status"),
            "local_density_targets": c.get("local_density_targets"),
            "maximum_impact": bp.get("maximum_impact"),
            "60_day_goal": bp.get("60_day_goal"),
            "phases": bp.get("phases", []),
            "metrics": bp.get("metrics", []),
            "known_opportunities": c.get("known_opportunities", []),
            "known_entities": c.get("known_entities", []),
        })

    Path("memory").mkdir(exist_ok=True)
    json.dump(plans, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = [
        "# Career Battle Plans",
        "",
        "Channel-level action plans. This is meant to answer: what should an artist do with this ecosystem?",
        "",
    ]

    for p in plans:
        lines.append(f"## {p['title']}")
        lines.append(f"- Coverage: {p['coverage_status']}")
        lines.append(f"- Maximum impact: {p['maximum_impact']}")
        lines.append(f"- 60-day goal: {p['60_day_goal']}")
        d = p.get("local_density_targets", {})
        if d.get("tokyo_known_target") is not None:
            lines.append(f"- Map target: {d.get('tokyo_known_target')} Tokyo entries; {d.get('koenji_target')} Koenji; {d.get('nakano_target')} Nakano; {d.get('radius_20km_target')} within 20km of Koenji.")
        lines.append("")
        for phase in p["phases"]:
            lines.append(f"### {phase['phase']}")
            for task in phase["tasks"]:
                lines.append(f"- {task}")
            lines.append("")
        lines.append("### Metrics")
        for m in p["metrics"]:
            lines.append(f"- {m}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
