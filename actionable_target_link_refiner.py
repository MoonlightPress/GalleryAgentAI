
import json
from pathlib import Path

TARGETS = "memory/actionable_targets_refined.json"
FALLBACK = "memory/actionable_targets.json"
PROMOTED = "memory/promoted_opportunity_links.json"
OUT = "memory/actionable_targets_with_links.json"
REPORT = "reports/actionable_now_with_links.md"

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def by_title(rows):
    return {x.get("title"): x for x in rows if x.get("title")}

def first_url(rows):
    if rows:
        return rows[0].get("url")
    return "unknown"

def refine(target, promoted):
    target = dict(target)
    promoted = promoted or {}

    target["application_form_url"] = first_url(promoted.get("application_forms", []))
    target["submission_guidelines_url"] = first_url(promoted.get("submission_guidelines", []))
    target["contact_page_url"] = first_url(promoted.get("contact_pages", []))
    target["open_call_url"] = first_url(promoted.get("open_calls", []))
    target["instagram_url"] = first_url(promoted.get("instagram", []))

    if target["application_form_url"] != "unknown":
        target["recommended_next_url"] = target["application_form_url"]
        target["recommended_next_action"] = "Open the application form and confirm required materials."
    elif target["submission_guidelines_url"] != "unknown":
        target["recommended_next_url"] = target["submission_guidelines_url"]
        target["recommended_next_action"] = "Read the submission guidelines and extract deadline, fee, and materials."
    elif target["open_call_url"] != "unknown":
        target["recommended_next_url"] = target["open_call_url"]
        target["recommended_next_action"] = "Open the current open-call page and choose the relevant call."
    elif target["contact_page_url"] != "unknown":
        target["recommended_next_url"] = target["contact_page_url"]
        target["recommended_next_action"] = "Use the contact page to verify submission/contact process."
    else:
        target["recommended_next_url"] = target.get("official_submission_url") or "unknown"
        target["recommended_next_action"] = "Manual research needed."

    confidence = float(target.get("confidence", 0) or 0)
    if target["application_form_url"] != "unknown":
        confidence += 0.12
    if target["submission_guidelines_url"] != "unknown":
        confidence += 0.08
    if target["contact_page_url"] != "unknown":
        confidence += 0.06
    if target["open_call_url"] != "unknown":
        confidence += 0.08

    target["confidence"] = round(min(0.99, confidence), 2)
    target["status"] = "actionable" if target["confidence"] >= 0.65 else "needs_final_verification"
    return target

def main():
    targets = load(TARGETS, None)
    if targets is None:
        targets = load(FALLBACK, [])
    promoted = by_title(load(PROMOTED, []))

    refined = [refine(t, promoted.get(t.get("title"))) for t in targets]
    refined.sort(key=lambda x: (x.get("status") == "actionable", x.get("confidence", 0)), reverse=True)

    Path("memory").mkdir(exist_ok=True)
    json.dump(refined, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = ["# Actionable Now With Promoted Links", "", "Uses promoted application/contact/open-call links.", ""]
    ready = [x for x in refined if x.get("status") == "actionable"]
    verify = [x for x in refined if x.get("status") != "actionable"]

    def section(title, rows):
        lines.append(f"## {title}")
        lines.append("")
        if not rows:
            lines.append("_No items._")
            lines.append("")
            return
        for t in rows:
            lines.append(f"### {t.get('title')}")
            lines.append(f"- Status: {t.get('status')}")
            lines.append(f"- Confidence: {int(float(t.get('confidence', 0)) * 100)}%")
            lines.append(f"- Recommended next action: {t.get('recommended_next_action')}")
            lines.append(f"- Recommended URL: {t.get('recommended_next_url')}")
            lines.append(f"- Application form: {t.get('application_form_url')}")
            lines.append(f"- Guidelines: {t.get('submission_guidelines_url')}")
            lines.append(f"- Open call: {t.get('open_call_url')}")
            lines.append(f"- Contact page: {t.get('contact_page_url')}")
            lines.append(f"- Deadline: {t.get('deadline')}")
            lines.append(f"- Fee: {t.get('fee')}")
            lines.append("")

    section("Ready / Near Ready", ready)
    section("Needs Final Verification", verify)

    Path("reports").mkdir(exist_ok=True)
    Path(REPORT).write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT)
    print("Wrote", REPORT)

if __name__ == "__main__":
    main()
