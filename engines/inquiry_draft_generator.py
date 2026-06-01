
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from opportunity_report_engine import load_json
from utils_filename import safe_filename

OPP_PATH = "deploy_data/compact_opportunities.json"
OUT_DIR = Path("reports/inquiry_drafts")

def title_of(opp):
    return opp.get("title") or opp.get("name") or "Unknown"

def org_of(opp):
    return opp.get("organization") or title_of(opp)

def missing_fields(opp):
    missing = []
    if not opp.get("submission_page"): missing.append("submission process")
    if not opp.get("deadline"): missing.append("deadline")
    if not opp.get("fees"): missing.append("fees")
    if not (opp.get("contact") or opp.get("email") or opp.get("contact_url")): missing.append("contact")
    return missing

def inquiry_draft(opp):
    org = org_of(opp)
    missing = missing_fields(opp)
    questions = []
    if "submission process" in missing: questions.append("whether you currently accept artist submissions or exhibition proposals")
    if "deadline" in missing: questions.append("whether there is a current or upcoming deadline")
    if "fees" in missing: questions.append("whether there are any application, participation, or exhibition fees")
    if "contact" in missing: questions.append("the best contact address or form for this kind of inquiry")
    question_sentence = "; ".join(questions) if questions else "whether there are any current opportunities for artists"

    return f"""Subject: Artist submission / exhibition inquiry

Hello,

I am writing to ask about {org}.

I am interested in learning {question_sentence}.

The artist I am writing about works with quiet, atmospheric images of place, architecture, memory, and everyday spaces. If this might fit your programming, I would be grateful to know the appropriate next step.

Portfolio:
[portfolio link]

Thank you,
[artist name]
"""

def main():
    opps = load_json(OPP_PATH, [])
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    for idx, opp in enumerate(opps):
        if not missing_fields(opp): continue
        safe_title = safe_filename(title_of(opp), max_len=60)
        (OUT_DIR / f"{idx:03d}_{safe_title}.txt").write_text(inquiry_draft(opp), encoding="utf-8")
        count += 1
    print(f"Generated {count} inquiry drafts.")

if __name__ == "__main__":
    main()
