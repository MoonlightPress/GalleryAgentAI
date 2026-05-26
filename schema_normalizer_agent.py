import json
import os
import re


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def infer_name(opp):
    candidates = [
        opp.get("name"),
        opp.get("title"),
        opp.get("opportunity_name"),
        opp.get("program_name"),
        opp.get("organization"),
    ]

    for c in candidates:
        if c and str(c).strip():
            return str(c).strip()

    text = " ".join([
        str(opp.get("one_sentence", "")),
        str(opp.get("why_fit", "")),
        str(opp.get("strategic_reasoning", "")),
        str(opp.get("next_action", "")),
    ])

    known_names = [
        "Tokyo Arts and Space",
        "TOKAS",
        "Asian Art Contemporary",
        "Tokyo Contemporary Art Award",
        "TCAA",
        "Kyoto Art Center",
        "Studio Kura",
        "Saruya",
        "Mt. Fuji",
        "Fujiyoshida"
    ]

    for name in known_names:
        if name.lower() in text.lower():
            return name

    return "Unknown"


def infer_type(opp):
    candidates = [
        opp.get("type"),
        opp.get("category"),
        opp.get("opportunity_type"),
    ]

    for c in candidates:
        if c and str(c).strip():
            return str(c).strip()

    text = " ".join([
        str(opp.get("name", "")),
        str(opp.get("title", "")),
        str(opp.get("one_sentence", "")),
        str(opp.get("why_fit", "")),
        str(opp.get("strategic_reasoning", "")),
    ]).lower()

    if "residency" in text or "artist in residence" in text:
        return "residency"

    if "award" in text:
        return "award"

    if "interview" in text or "publication" in text:
        return "publication"

    if "exhibition" in text or "open call" in text:
        return "open_call"

    return "unknown"


def infer_city(opp):
    candidates = [
        opp.get("city"),
        opp.get("location"),
        opp.get("neighborhood"),
    ]

    for c in candidates:
        if c and str(c).strip():
            return str(c).strip()

    text = json.dumps(opp, ensure_ascii=False).lower()

    city_map = {
        "tokyo": "Tokyo",
        "kyoto": "Kyoto",
        "itoshima": "Itoshima",
        "fukuoka": "Fukuoka",
        "fujiyoshida": "Fujiyoshida",
        "mt. fuji": "Fujiyoshida",
        "new york": "New York",
        "aomori": "Aomori",
        "ibaraki": "Ibaraki",
    }

    for key, value in city_map.items():
        if key in text:
            return value

    return ""


def normalize_one(opp):
    opp["name"] = infer_name(opp)
    opp["type"] = infer_type(opp)
    opp["city"] = infer_city(opp)

    if "country" not in opp or not opp.get("country"):
        text = json.dumps(opp, ensure_ascii=False).lower()

        if any(x in text for x in ["tokyo", "kyoto", "japan", "fujiyoshida", "itoshima", "aomori", "ibaraki"]):
            opp["country"] = "Japan"
        elif "new york" in text:
            opp["country"] = "United States"
        else:
            opp["country"] = ""

    opp.setdefault("organization", opp.get("name", ""))
    opp.setdefault("description", opp.get("why_fit", "") or opp.get("strategic_reasoning", ""))
    opp.setdefault("deadline", "")
    opp.setdefault("fees", "")
    opp.setdefault("status", "active")
    opp.setdefault("priority", "C")
    opp.setdefault("visibility", "secondary")

    return opp


def main():
    opportunities = load_json("memory/opportunities.json", [])

    normalized = [
        normalize_one(opp)
        for opp in opportunities
    ]

    save_json("memory/opportunities.json", normalized)

    print(f"Normalized {len(normalized)} opportunities.")


if __name__ == "__main__":
    main()