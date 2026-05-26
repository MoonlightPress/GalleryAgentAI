import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import os
from datetime import datetime


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_text(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


opportunities = load_json("memory/opportunities.json", [])
filtered = load_json("memory/filtered_out_opportunities.json", [])
rejected = load_json("memory/rejected_opportunities.json", [])
profile = load_json("memory/artist_profile.json", {})
materials = load_json("memory/materials_memory.json", {})

visible = [
    o for o in opportunities
    if o.get("visibility", "primary") != "hidden"
]

primary = [
    o for o in visible
    if o.get("visibility", "primary") == "primary"
]

secondary = [
    o for o in visible
    if o.get("visibility", "primary") == "secondary"
]

unresolved = [
    o for o in visible
    if o.get("human_verification_needed")
]

ideal = [
    o for o in visible
    if o.get("recommendation_tier") == "ideal_next_step"
]

sustainable = [
    o for o in visible
    if o.get("recommendation_tier") == "emotionally_sustainable"
]

lines = []

lines.append("# Pipeline Status\n")
lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

lines.append("## Summary\n")
lines.append(f"- Visible opportunities: {len(visible)}")
lines.append(f"- Primary opportunities: {len(primary)}")
lines.append(f"- Secondary opportunities: {len(secondary)}")
lines.append(f"- Hidden opportunities: {len(filtered)}")
lines.append(f"- Rejected malformed opportunities: {len(rejected)}")
lines.append(f"- Opportunities with unresolved questions: {len(unresolved)}")
lines.append(f"- Ideal next steps: {len(ideal)}")
lines.append(f"- Emotionally sustainable: {len(sustainable)}\n")

lines.append("## Top Visible Opportunities\n")

for o in visible[:10]:
    lines.append(f"### {o.get('name', 'Unknown')}")
    lines.append(f"- Visibility: {o.get('visibility', 'primary')}")
    lines.append(f"- Tier: {o.get('recommendation_tier', 'unknown')}")
    lines.append(f"- Priority: {o.get('priority', '')}")
    lines.append(f"- Fit: {o.get('fit_score', '')}")
    lines.append(f"- Strategic: {o.get('strategic_score', '')}")
    lines.append(f"- Emotional resistance: {o.get('emotional_resistance', '')}")
    lines.append(f"- Next action: {o.get('next_action', '')}")
    lines.append("")

lines.append("## Remaining Verification Questions\n")

for o in unresolved:
    lines.append(f"### {o.get('name', 'Unknown')}")
    for q in o.get("human_verification_needed", []):
        lines.append(f"- {q}")
    lines.append("")

lines.append("## Artist Profile Snapshot\n")
lines.append(f"- Career stage: {profile.get('career_stage', '')}")
lines.append(f"- Primary mediums: {', '.join(profile.get('primary_mediums', []))}")
lines.append(f"- Preferred opportunity types: {', '.join(profile.get('preferred_opportunity_types', []))}")

lines.append("\n## Reusable Materials Snapshot\n")
lines.append(f"- Artist bios saved: {len(materials.get('artist_bios', []))}")
lines.append(f"- Artist statements saved: {len(materials.get('artist_statements', []))}")
lines.append(f"- CV versions saved: {len(materials.get('cv_versions', []))}")
lines.append(f"- Portfolio sets saved: {len(materials.get('portfolio_sets', []))}")
lines.append(f"- Image specs saved: {len(materials.get('image_specs', []))}")
lines.append(f"- Translations saved: {len(materials.get('translations', []))}")

save_text(
    "pipeline_status.md",
    "\n".join(lines)
)

print("Saved pipeline_status.md")