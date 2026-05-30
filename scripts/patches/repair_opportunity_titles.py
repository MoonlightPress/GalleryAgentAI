import json
import os


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


opps = load_json(
    "memory/opportunities_master.json",
    []
)

fixed = 0

for idx, opp in enumerate(opps):

    title = (
        opp.get("title")
        or opp.get("name")
        or opp.get("opportunity_name")
    )

    if not title:

        source = (
            opp.get("source_link")
            or opp.get("source_url")
            or opp.get("official_website")
            or ""
        )

        category = opp.get("category", "Opportunity")

        generated = f"{category} #{idx+1}"

        if source:
            try:
                domain = source.split("//")[-1].split("/")[0]
                generated = f"{category} - {domain}"
            except:
                pass

        opp["title"] = generated
        fixed += 1

    else:
        opp["title"] = str(title)

save_json(
    "memory/opportunities_master.json",
    opps
)

print(f"Fixed {fixed} missing titles.")