import json
import os
from collections import Counter


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


opps = load_json("memory/opportunities_master.json", [])

by_category = Counter(
    opp.get("category", "unknown")
    for opp in opps
)

by_city = Counter(
    opp.get("city", "unknown")
    for opp in opps
)

with_links = [
    opp for opp in opps
    if opp.get("source_link", "").startswith("http")
]

needs_review = [
    opp for opp in opps
    if opp.get("needs_council_review")
]

lines = []

lines.append("# Opportunity Database Status")
lines.append("")
lines.append(f"Total master records: {len(opps)}")
lines.append(f"Records with source links: {len(with_links)}")
lines.append(f"Needs council review: {len(needs_review)}")
lines.append("")

lines.append("## By Category")
for category, count in by_category.most_common():
    lines.append(f"- {category}: {count}")

lines.append("")
lines.append("## By City")
for city, count in by_city.most_common():
    lines.append(f"- {city}: {count}")

lines.append("")
lines.append("## Source-Link Problems")
for opp in opps:
    if not opp.get("source_link", "").startswith("http"):
        lines.append(f"- {opp.get('name', 'Unknown')}")

with open("opportunity_database_status.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Saved opportunity_database_status.md")