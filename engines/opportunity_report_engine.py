import json
import os
import re

def safe_filename(name):
    name = str(name)
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name[:80]
from datetime import date
from utils_filename import safe_filename

ARTIST_PROFILE_PATH = "memory/artist_master_profile.json"

def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback

def clean(value, fallback="Not publicly listed"):
    if value is None:
        return fallback
    value = str(value).strip()
    if not value or value.lower() in {"unknown", "none", "null", "n/a", "unverified"}:
        return fallback
    return value

def number(value, default=0.0):
    try:
        return float(value or default)
    except Exception:
        return default

def get_source(opp):
    return opp.get("source_link") or opp.get("source_url") or opp.get("official_website") or opp.get("submission_page") or ""

def category_label(raw):
    labels = {
        "zine_print": "Print / Zines / Bookstores",
        "bookstore_gallery": "Print / Zines / Bookstores",
        "bookstore_event": "Print / Zines / Bookstores",
        "cafe_gallery": "Cafe / Local Wall Spaces",
        "fair_popup": "Markets / Popups / Booths",
        "market_event": "Markets / Popups / Booths",
        "artist_space": "Artist Spaces",
        "event_space": "Artist Spaces",
        "gallery_event": "Galleries / Exhibition Calls",
        "gallery": "Galleries / Exhibition Calls",
        "residency": "Residencies / Longer Projects",
        "institutional": "Institutional / Grants",
    }
    return labels.get(raw, str(raw or "Other").replace("_", " ").title())

def fit_band(score):
    score = number(score)
    if score >= 8: return "Excellent fit"
    if score >= 7: return "Strong fit"
    if score >= 5.5: return "Promising"
    if score >= 4: return "Possible, but not urgent"
    return "Low priority"

def verification_items(opp):
    source = get_source(opp)
    submission = opp.get("submission_page")
    deadline = opp.get("deadline")
    fees = opp.get("fees")
    contact = opp.get("contact") or opp.get("email") or opp.get("contact_url")
    return [
        {"label": "Official/source website", "status": "verified" if source else "missing", "value": source or "No source attached"},
        {"label": "Submission process", "status": "verified" if submission else "needs_inquiry", "value": clean(submission)},
        {"label": "Deadline", "status": "verified" if deadline else "needs_inquiry", "value": clean(deadline)},
        {"label": "Fees", "status": "verified" if fees else "needs_inquiry", "value": clean(fees)},
        {"label": "Contact", "status": "verified" if contact else "needs_inquiry", "value": clean(contact)},
    ]

def verification_summary(opp):
    items = verification_items(opp)
    missing = [item["label"] for item in items if item["status"] != "verified"]
    verified = [item["label"] for item in items if item["status"] == "verified"]
    if not missing:
        return "Core public information appears present."
    return f"Verified: {', '.join(verified) if verified else 'none'}. Needs checking: {', '.join(missing)}."

def upgraded_score(opp, profile):
    base = number(opp.get("overall_score"), 0)
    category = category_label(opp.get("category")).lower()
    ideal = " ".join(profile.get("ideal_opportunity_types", [])).lower()
    bump = 0.0
    if any(word in ideal for word in category.split()):
        bump += 0.8
    if get_source(opp):
        bump += 0.4
    if opp.get("submission_page"):
        bump += 0.4
    if not opp.get("fees") or str(opp.get("fees")).lower() in {"unknown", "none", "n/a"}:
        bump -= 0.2
    return round(max(0, min(10, base + bump)), 1)

def confidence_level(opp):
    present = 0
    if get_source(opp): present += 1
    if opp.get("submission_page"): present += 1
    if opp.get("deadline"): present += 1
    if opp.get("fees"): present += 1
    if opp.get("why_this_fits_short") or opp.get("three_bullets"): present += 1
    if present >= 4: return "High"
    if present >= 2: return "Medium"
    return "Low"

def artist_fit_reasons(opp, profile):
    category = category_label(opp.get("category"))
    themes = profile.get("core_themes", [])
    visual = profile.get("visual_language", [])
    reasons = []
    reasons.append(f"Opportunity type: {category}.")
    if themes:
        reasons.append("Artist themes to compare against this venue: " + ", ".join(themes[:6]) + ".")
    if visual:
        reasons.append("Visual-language fit signals: " + ", ".join(visual[:6]) + ".")
    return reasons

def opportunity_report_markdown(opp, profile=None):
    profile = profile or load_json(ARTIST_PROFILE_PATH, {})
    title = opp.get("title") or opp.get("name") or "Unknown"
    score = upgraded_score(opp, profile)
    source = get_source(opp)
    fit_reasons = "\n".join([f"- {r}" for r in artist_fit_reasons(opp, profile)])
    verification = "\n".join([f"- **{i['label']}**: {i['value']} ({i['status']})" for i in verification_items(opp)])
    bullets = opp.get("three_bullets", [])
    bullet_text = "\n".join([f"- {b}" for b in bullets]) if bullets else "- No bullet analysis stored yet."

    return f"""# {title}

## 1. Quick Judgment
**Fit score:** {score}/10  
**Fit band:** {fit_band(score)}  
**Confidence:** {confidence_level(opp)}  
**Type:** {category_label(opp.get("category"))}  
**City:** {clean(opp.get("city"), "City not listed")}  

## 2. Verification Status
{verification_summary(opp)}

{verification}

## 3. Why This May Fit the Artist
{fit_reasons}

## 4. Public Opportunity Summary
{clean(opp.get("one_sentence") or opp.get("suggested_display_summary"), "No short summary available.")}

## 5. Existing Fit Notes
{clean(opp.get("why_this_fits_short"), "No stored fit explanation yet.")}

## 6. Key Points
{bullet_text}

## 7. Submission / Logistics
- **Deadline:** {clean(opp.get("deadline"))}
- **Fees:** {clean(opp.get("fees"))}
- **Submission page:** {clean(opp.get("submission_page"))}
- **Source:** {source or "No source attached"}

## 8. Risk / Unknowns
{clean(opp.get("dealbreaker"), "No hard dealbreaker recorded. Manual verification recommended.")}

## 9. Recommended Next Step
{clean(opp.get("quick_action"), "Open the source link and verify whether submissions or inquiries are currently accepted.")}

## 10. Inquiry Need
If submission/contact details are missing, generate a short inquiry email instead of presenting the opportunity as fully verified.

_Last generated: {date.today().isoformat()}_
"""

if __name__ == "__main__":
    opps = load_json("deploy_data/compact_opportunities.json", [])
    profile = load_json(ARTIST_PROFILE_PATH, {})
    os.makedirs("reports/opportunities", exist_ok=True)
    for idx, opp in enumerate(opps):
        title = safe_filename(opp.get("title") or opp.get("name") or f"opportunity_{idx}", max_len=70)
        report = opportunity_report_markdown(opp, profile)
        with open(f"reports/opportunities/{idx:03d}_{safe_filename(title)}.md", "w", encoding="utf-8") as f:
            f.write(report)
    print(f"Generated {len(opps)} opportunity reports.")
