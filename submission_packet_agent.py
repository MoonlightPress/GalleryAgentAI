import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import json
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from anthropic import Anthropic


load_dotenv(dotenv_path=".env")

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-5"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def fetch_page_text(url):
    if not url:
        return ""

    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
    except Exception:
        return ""

    soup = BeautifulSoup(r.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    return soup.get_text("\n", strip=True)[:18000]


def generate_submission_packet(opportunity, page_text, artist_profile, materials):
    prompt = f"""
You are Agent P: Submission Packet Agent.

Convert this opportunity into an EXECUTABLE submission plan.

Artist Profile:
{json.dumps(artist_profile, indent=2, ensure_ascii=False)}

Reusable Materials Memory:
{json.dumps(materials, indent=2, ensure_ascii=False)}

Opportunity:
{json.dumps(opportunity, indent=2, ensure_ascii=False)}

Website Text:
{page_text}

Return ONLY valid JSON.

Schema:
{{
  "submission_requirements": {{
    "number_of_images": "",
    "image_specs": [],
    "statement_requirements": [],
    "cv_requirements": [],
    "file_format_requirements": [],
    "eligibility_requirements": [],
    "deadline": "",
    "fees": "",
    "submission_method": ""
  }},
  "execution_plan": {{
    "estimated_total_time": "",
    "difficulty": "",
    "recommended_order": [],
    "missing_materials": [],
    "likely_pain_points": [],
    "recommended_preparation_strategy": []
  }},
  "artist_packet_recommendation": {{
    "recommended_image_types": [],
    "recommended_tone": "",
    "portfolio_strategy": "",
    "suggested_work_count": ""
  }}
}}

Rules:
- Be extremely concrete.
- Extract exact requirements whenever possible.
- Prefer specific numbers over vague language.
- Use reusable materials when relevant.
- Do not invent information.
- If unknown, say "Not clearly specified."
- Convert vague application language into actionable steps.
"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    cleaned = response.content[0].text.replace("```json", "").replace("```", "").strip()
    return json.loads(cleaned)


def main():
    opportunities = load_json("memory/opportunities.json", [])
    artist_profile = load_json("memory/artist_profile.json", {})
    materials = load_json("memory/materials_memory.json", {})

    updated = []

    print("\nGenerating submission packets...\n")

    for opp in opportunities:
        name = opp.get("name", "UNKNOWN")
        print(f"PACKET: {name}")

        url = opp.get("submission_page") or opp.get("contact_page") or opp.get("official_website")
        page_text = fetch_page_text(url)

        if not page_text:
            print("  FAILED PAGE FETCH")
            updated.append(opp)
            continue

        try:
            packet = generate_submission_packet(
                opp,
                page_text,
                artist_profile,
                materials
            )

            opp["submission_packet"] = packet
            updated.append(opp)
            print("  SUCCESS")

        except Exception as e:
            print(f"  FAILED: {e}")
            updated.append(opp)

    save_json("memory/opportunities.json", updated)

    print("\nSaved submission packets.\n")


if __name__ == "__main__":
    main()