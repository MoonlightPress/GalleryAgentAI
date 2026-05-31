
import json
from pathlib import Path

TARGETS = "memory/actionable_targets.json"
EXTRACTIONS = "memory/official_page_extractions.json"
OUT_JSON = "memory/actionable_targets_refined.json"
OUT_REPORT = "reports/actionable_now_refined.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def has(v):
    return v and str(v).strip().lower() not in {"unknown", "none", "null", "n/a"}

def by_title(rows):
    return {r.get("title"): r for r in rows}

def refine(target, extraction):
    target = dict(target)

    if extraction:
        if not has(target.get("official_contact_email")) and extraction.get("emails"):
            target["official_contact_email"] = extraction["emails"][0]
            target["contact_source"] = "official_page_extraction"

        if not has(target.get("deadline")) and extraction.get("dates"):
            target["deadline"] = extraction["dates"][0]
            target["deadline_source"] = "official_page_extraction"

        if not has(target.get("fee")) and extraction.get("fees"):
            target["fee"] = extraction["fees"][0]
            target["fee_source"] = "official_page_extraction"

        if target.get("required_materials") == ["manual requirement check needed"] and extraction.get("requirements"):
            target["required_materials"] = extraction["requirements"]

        if extraction.get("eligibility_clues"):
            target["eligibility"] = extraction["eligibility_clues"]

        target["extraction_summary"] = {
            "emails_found": len(extraction.get("emails", [])),
            "dates_found": len(extraction.get("dates", [])),
            "fees_found": len(extraction.get("fees", [])),
            "requirements_found": len(extraction.get("requirements", [])),
            "urls_checked": extraction.get("source_urls_checked", []),
        }

    confidence = 0
    if has(target.get("official_submission_url")): confidence += 0.2
    if has(target.get("official_contact_email")): confidence += 0.2
    if has(target.get("deadline")): confidence += 0.2
    if has(target.get("fee")): confidence += 0.1
    if target.get("required_materials") and target.get("required_materials") != ["manual requirement check needed"]: confidence += 0.15
    if target.get("eligibility"): confidence += 0.15

    target["confidence"] = round(min(0.99, confidence), 2)
    target["status"] = "actionable" if target["confidence"] >= 0.65 else "needs_final_verification"

    return target

def main():
    targets = load(TARGETS, [])
    extractions = by_title(load(EXTRACTIONS, []))

    refined = [refine(t, extractions.get(t.get("title"))) for t in targets]
    refined.sort(key=lambda x: (x["status"] == "actionable", x["confidence"]), reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(refined, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = ["# Actionable Now Refined", "", "Updated after official page extraction.", ""]
    ready = [x for x in refined if x["status"] == "actionable"]
    verify = [x for x in refined if x["status"] != "actionable"]

    def section(title, rows):
        lines.append(f"## {title}")
        lines.append("")
        if not rows:
            lines.append("_No items._")
            lines.append("")
            return
        for t in rows:
            lines.append(f"### {t['title']}")
            lines.append(f"- Status: {t['status']}")
            lines.append(f"- Confidence: {int(t['confidence'] * 100)}%")
            lines.append(f"- Submission URL: {t.get('official_submission_url')}")
            lines.append(f"- Contact: {t.get('official_contact_email')}")
            lines.append(f"- Deadline: {t.get('deadline')}")
            lines.append(f"- Fee: {t.get('fee')}")
            lines.append("")
            lines.append("#### Required materials / requirement signals")
            for m in t.get("required_materials", []):
                lines.append(f"- {m}")
            if t.get("eligibility"):
                lines.append("")
                lines.append("#### Eligibility clues")
                for e in t["eligibility"][:5]:
                    lines.append(f"- {e}")
            lines.append("")

    section("Ready / Near Ready", ready)
    section("Needs Final Verification", verify)

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Actionable:", len(ready), "Needs verification:", len(verify))

if __name__ == "__main__":
    main()
