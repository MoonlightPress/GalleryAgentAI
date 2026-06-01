import json
import os
import hashlib


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def make_id(name, url):
    raw = f"{name}|{url}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest()[:12]


seed_opportunities = [
    {
        "name": "Asian Art Contemporary - Artist Interview Program",
        "organization": "Asian Art Contemporary",
        "type": "publication",
        "category": "publication",
        "city": "New York",
        "country": "United States",
        "official_website": "https://asianartcontemporary.com",
        "submission_page": "https://asianartcontemporary.com/category/opportunity/call-for-artists",
        "source_url": "https://asianartcontemporary.com/category/opportunity/call-for-artists",
        "deadline": "Rolling",
        "fees": "$45–75",
        "status": "active",
        "visibility": "secondary",
        "priority": "C",
        "friction_level": "low",
        "notes": "Artist interview/publication platform. Useful after statement and portfolio framing improve."
    },
    {
        "name": "TOKAS-Emerging",
        "organization": "Tokyo Arts and Space",
        "type": "open_call",
        "category": "institutional_exhibition",
        "city": "Tokyo",
        "country": "Japan",
        "official_website": "https://www.tokyoartsandspace.jp/en/",
        "submission_page": "https://www.tokyoartsandspace.jp/en/application/about_opencall.html",
        "source_url": "https://www.tokyoartsandspace.jp/en/application/about_opencall.html",
        "deadline": "Annual / check current cycle",
        "fees": "Unknown",
        "status": "requires_verification",
        "visibility": "secondary",
        "priority": "C",
        "friction_level": "high",
        "notes": "Eligibility and residency requirements must be verified before any work."
    },
    {
        "name": "Kyoto Art Center - Artist in Residence Program",
        "organization": "Kyoto Art Center",
        "type": "residency",
        "category": "residency",
        "city": "Kyoto",
        "country": "Japan",
        "official_website": "https://www.kac.or.jp/eng/",
        "submission_page": "https://www.kac.or.jp/eng/program/air/",
        "source_url": "https://www.kac.or.jp/eng/program/air/",
        "deadline": "Annual / check current cycle",
        "fees": "Unknown",
        "status": "watch",
        "visibility": "primary",
        "priority": "A",
        "friction_level": "medium_high",
        "notes": "Major long-term residency target. Strong institutional fit if timing and proposal are right."
    },
    {
        "name": "Studio Kura Artist Residency",
        "organization": "Studio Kura",
        "type": "residency",
        "category": "residency",
        "city": "Itoshima",
        "country": "Japan",
        "official_website": "https://studiokura.info/en/artist-in-residence/",
        "submission_page": "https://studiokura.info/en/artist-in-residence/",
        "source_url": "https://studiokura.info/en/artist-in-residence/",
        "deadline": "Rolling / check availability",
        "fees": "Paid residency",
        "status": "active",
        "visibility": "secondary",
        "priority": "C",
        "friction_level": "medium",
        "notes": "Accessible Japan residency, but cost/social/rural fit must be evaluated carefully."
    },
    {
        "name": "Saruya Artist in Residence",
        "organization": "Saruya",
        "type": "residency",
        "category": "residency",
        "city": "Fujiyoshida",
        "country": "Japan",
        "official_website": "https://saruya-hostel.com/air/",
        "submission_page": "https://saruya-hostel.com/air/",
        "source_url": "https://saruya-hostel.com/air/",
        "deadline": "Check current cycle",
        "fees": "Unknown",
        "status": "active",
        "visibility": "primary",
        "priority": "A",
        "friction_level": "medium",
        "notes": "Fujiyoshida / Mt. Fuji regional research residency. Strong thematic fit if costs and deadline work."
    }
]

for opp in seed_opportunities:
    opp["id"] = make_id(opp["name"], opp["source_url"])
    opp["source_link"] = opp["source_url"]
    opp["source_status"] = "verified_link_present"

save_json("memory/opportunities_master.json", seed_opportunities)
save_json("memory/opportunities.json", seed_opportunities)

print(f"Seeded {len(seed_opportunities)} verified-source opportunities.")