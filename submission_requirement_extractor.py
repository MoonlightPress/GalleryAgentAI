
import json
from pathlib import Path

SRC = "memory/submission_pages.json"
OUT = "memory/submission_requirements.json"

REQ_TERMS = {
    "portfolio": ["portfolio", "作品集", "ポートフォリオ"],
    "artist_statement": ["artist statement", "statement", "ステートメント", "コンセプト"],
    "bio": ["bio", "biography", "profile", "プロフィール", "略歴"],
    "cv": ["cv", "resume", "résumé", "履歴", "経歴"],
    "images": ["images", "jpg", "jpeg", "png", "image files", "作品画像", "画像"],
    "pdf": ["pdf"],
    "dimensions": ["dimensions", "size", "サイズ", "寸法"],
    "price": ["price", "pricing", "販売価格", "価格"],
    "edition": ["edition", "editions", "部数"],
    "application_form": ["application form", "form", "応募フォーム", "申込フォーム"],
}

def detect_requirements(text):
    low = text.lower()
    found = []
    for label, terms in REQ_TERMS.items():
        if any(t.lower() in low for t in terms):
            found.append(label)
    return found

def main():
    pages = json.loads(Path(SRC).read_text(encoding="utf-8"))

    for page in pages:
        text = page.get("full_text", "")
        page["requirements_detected"] = detect_requirements(text)

        if not page["requirements_detected"]:
            page["requirements_detected"] = ["manual_review_needed"]

    Path(OUT).write_text(json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
