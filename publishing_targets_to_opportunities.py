
import json
from pathlib import Path
from datetime import date

COMPACT_PATHS = [
    Path("memory/compact_opportunities.json"),
    Path("Memory/compact_opportunities.json"),
    Path("deploy_data/compact_opportunities.json"),
]

OUT_MEMORY = Path("memory/compact_opportunities.json")
OUT_DEPLOY = Path("deploy_data/compact_opportunities.json")
OUT_REPORT = Path("reports/publishing_opportunities_added.md")

CATEGORY = "book_publishing"
SOURCE_TAG = "publishing_category_import_v1"

PUBLISHING_TARGETS = [
    {
        "title": "Publishing / Artist Books — Battle Plan",
        "organization": "Mochi Career System",
        "opportunity_type": "category_summary",
        "city": "Tokyo / Online",
        "overall_score": 8.1,
        "one_sentence": "Publishing is the next step after the zine path: one finished printed object can become a pitch, sample, portfolio proof, and conversation starter.",
        "why_this_fits_short": "This path fits an artist whose work can become a quiet book object, small edition, photobook, or publication proposal.",
        "quick_action": "Finish one zine or artist-book prototype, then compare it against torch press, twelvebooks, and shashasha.",
        "fees": "Usually low direct cost; mostly preparation time.",
        "difficulty": "medium",
        "status": "research_next",
        "tier": 0,
        "confidence": 85,
        "three_bullets": [
            "Best after one finished zine or artist-book prototype exists.",
            "Phase 1 targets: torch press, twelvebooks, shashasha.",
            "Success condition: one publication package and two careful outreach attempts."
        ],
    },
    {
        "title": "torch press",
        "organization": "torch press",
        "opportunity_type": "small_press_publisher",
        "city": "Tokyo",
        "overall_score": 7.6,
        "one_sentence": "Small press / art-book publishing target; useful for artist-book positioning after a finished object exists.",
        "why_this_fits_short": "Potential fit if her work is presented as a coherent printed project rather than loose portfolio images.",
        "quick_action": "Review recent titles and identify whether her work fits their publication style.",
        "source_url": "",
        "difficulty": "medium",
        "status": "research_next",
        "tier": 1,
        "confidence": 72,
        "three_bullets": [
            "Category: small press / art-book publisher.",
            "Best use: research comparable books and publication style.",
            "Next step: prepare one concise publication pitch after the zine prototype exists."
        ],
    },
    {
        "title": "twelvebooks",
        "organization": "twelvebooks",
        "opportunity_type": "art_book_distributor_publisher",
        "city": "Tokyo",
        "overall_score": 7.4,
        "one_sentence": "Art-book distribution and publishing ecosystem target; useful for understanding professional presentation standards.",
        "why_this_fits_short": "Relevant if the work develops into an artist-book object with strong sequencing and physical presentation.",
        "quick_action": "Research comparable books, pricing, size, binding, and presentation standards.",
        "source_url": "",
        "difficulty": "medium",
        "status": "ready_to_compare",
        "tier": 1,
        "confidence": 70,
        "three_bullets": [
            "Category: art-book distributor / publisher ecosystem.",
            "Best use: benchmark professional book presentation.",
            "Next step: compare 5 similar books before making contact."
        ],
    },
    {
        "title": "shashasha",
        "organization": "shashasha",
        "opportunity_type": "photobook_platform",
        "city": "Tokyo / Online",
        "overall_score": 7.2,
        "one_sentence": "Photobook-oriented platform; relevant if her work develops into book sequencing or editioned projects.",
        "why_this_fits_short": "Useful if her paintings are arranged as a visual sequence with mood, place, and atmosphere.",
        "quick_action": "Review listed artists/books and compare format, pricing, edition size, and tone.",
        "source_url": "",
        "difficulty": "medium",
        "status": "ready_to_compare",
        "tier": 1,
        "confidence": 68,
        "three_bullets": [
            "Category: photobook / art-book platform.",
            "Best use: compare book format and audience.",
            "Next step: identify 3 similar artists or books."
        ],
    },
    {
        "title": "Komiyama Tokyo",
        "organization": "Komiyama Tokyo",
        "opportunity_type": "art_photobook_store",
        "city": "Tokyo",
        "overall_score": 6.8,
        "one_sentence": "Art and photobook reference point; better as research and benchmarking than first outreach.",
        "why_this_fits_short": "Useful for understanding the upper end of art/photo book presentation and audience expectations.",
        "quick_action": "Use as a benchmark for book quality, subject matter, pricing, and presentation.",
        "source_url": "",
        "difficulty": "medium",
        "status": "benchmark",
        "tier": 2,
        "confidence": 60,
        "three_bullets": [
            "Category: art / photobook store.",
            "Best use: benchmark professional presentation.",
            "Next step: compare whether her work belongs in zine, photobook, or artist-book form."
        ],
    },
    {
        "title": "Book Obscura",
        "organization": "Book Obscura",
        "opportunity_type": "photobook_store",
        "city": "Kichijoji, Tokyo",
        "overall_score": 6.7,
        "one_sentence": "Photobook specialist; useful if the project becomes image-sequence or book-object focused.",
        "why_this_fits_short": "Relevant if the work is framed as visual sequencing rather than single-image exhibition.",
        "quick_action": "Research whether the work belongs closer to photobook or zine format.",
        "source_url": "https://bookobscura.com/",
        "difficulty": "medium",
        "status": "benchmark",
        "tier": 2,
        "confidence": 58,
        "three_bullets": [
            "Category: photobook store.",
            "Best use: benchmark sequencing and book-object presentation.",
            "Next step: review comparable photobooks."
        ],
    },
    {
        "title": "Books Ruhe",
        "organization": "Books Ruhe",
        "opportunity_type": "independent_bookstore",
        "city": "Kichijoji, Tokyo",
        "overall_score": 6.3,
        "one_sentence": "Independent bookstore reference and possible later placement target.",
        "why_this_fits_short": "Useful as part of the west-side book ecosystem, but less publishing-specific than the Tier 1 targets.",
        "quick_action": "Research stock and independent publication compatibility.",
        "source_url": "https://www.books-ruhe.co.jp/",
        "difficulty": "low",
        "status": "research_next",
        "tier": 2,
        "confidence": 55,
        "three_bullets": [
            "Category: independent bookstore.",
            "Best use: later placement or local publishing research.",
            "Next step: check whether zines, artist books, or small editions are represented."
        ],
    },
]

def load_json(path, fallback):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return fallback

def find_existing(path_list, fallback):
    for p in path_list:
        if p.exists():
            return p, load_json(p, fallback)
    return None, fallback

def title_key(opp):
    return (opp.get("title") or opp.get("name") or opp.get("organization") or "").strip().lower()

def to_opportunity(t):
    source = t.get("source_url", "")
    return {
        "title": t["title"],
        "name": t["title"],
        "organization": t.get("organization", t["title"]),
        "category": CATEGORY,
        "city": t.get("city", "Tokyo"),
        "overall_score": t.get("overall_score", 6.5),
        "one_sentence": t.get("one_sentence", ""),
        "suggested_display_summary": t.get("one_sentence", ""),
        "why_this_fits_short": t.get("why_this_fits_short", ""),
        "quick_action": t.get("quick_action", ""),
        "source_url": source,
        "source_link": source,
        "official_website": source,
        "submission_page": "",
        "deadline": "",
        "fees": t.get("fees", ""),
        "difficulty": t.get("difficulty", "medium"),
        "three_bullets": t.get("three_bullets", []),
        "career_category": "publishing",
        "opportunity_type": t.get("opportunity_type", "publishing_target"),
        "neighborhood": t.get("city", "Tokyo").replace(", Tokyo", ""),
        "tier": t.get("tier", 2),
        "confidence": t.get("confidence", 60),
        "status": t.get("status", "research_next"),
        "import_source": SOURCE_TAG,
        "imported_at": str(date.today()),
    }

def main():
    compact_path, existing = find_existing(COMPACT_PATHS, [])

    if not isinstance(existing, list):
        raise SystemExit("compact_opportunities.json is not a list. Aborting.")

    new_opps = [to_opportunity(t) for t in PUBLISHING_TARGETS]

    # repeated runs should replace prior publishing imports
    preserved = [o for o in existing if o.get("import_source") != SOURCE_TAG]
    existing_keys = {title_key(o) for o in preserved}

    added = []
    skipped = []

    for opp in new_opps:
        key = title_key(opp)
        if key in existing_keys:
            skipped.append(opp["title"])
            continue
        preserved.append(opp)
        existing_keys.add(key)
        added.append(opp["title"])

    OUT_MEMORY.parent.mkdir(exist_ok=True)
    OUT_DEPLOY.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)

    OUT_MEMORY.write_text(json.dumps(preserved, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_DEPLOY.write_text(json.dumps(preserved, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Publishing Opportunities Added To Existing Feed",
        "",
        f"- Existing compact source: {compact_path}",
        f"- Added publishing opportunities: {len(added)}",
        f"- Skipped duplicate titles: {len(skipped)}",
        "",
        "## Added",
    ]

    for title in added:
        lines.append(f"- {title}")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_MEMORY)
    print("Wrote", OUT_DEPLOY)
    print("Wrote", OUT_REPORT)
    print("Added:", len(added))

if __name__ == "__main__":
    main()
