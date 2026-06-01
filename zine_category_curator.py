
import json
from pathlib import Path
from collections import Counter

NORMALIZED = "memory/normalized_opportunities.json"
OUT_JSON = "memory/zine_category_targets.json"
OUT_REPORT = "reports/zine_category_targets.md"

# These are the strong known zine / artist-book ecosystem targets discovered so far.
# The point of this file is to stop letting article titles pollute the website.
ALLOWLIST = {
    "Tacoche": {
        "career_category": "zines",
        "opportunity_type": "zine_shop",
        "display_name": "Tacoche",
        "neighborhood": "Nakano",
        "tier": 1,
        "why_it_matters": "Major Tokyo independent/self-publishing shop. Strong first target for zines, artist books, and small printed works.",
        "first_action": "Review shop/site and confirm whether they accept consignment or submissions.",
    },
    "LOCAL Gallery・Books": {
        "career_category": "zines",
        "opportunity_type": "bookstore_gallery",
        "display_name": "LOCAL Gallery・Books",
        "neighborhood": "Koenji",
        "tier": 1,
        "why_it_matters": "Local Koenji book/gallery target; useful for a quiet works-on-paper artist and local relationship building.",
        "first_action": "Verify current location/contact and visit with a sample zine.",
    },
    "Dig A Hole Zines": {
        "career_category": "zines",
        "opportunity_type": "zine_shop",
        "display_name": "Dig A Hole Zines",
        "neighborhood": "Koenji",
        "tier": 1,
        "why_it_matters": "Direct zine-shop target in/near Koenji. Strong match for a first local distribution attempt.",
        "first_action": "Check Instagram, confirm hours/location, and prepare a sample copy.",
    },
    "本店・本屋の実験室": {
        "career_category": "zines",
        "opportunity_type": "independent_bookstore_event_space",
        "display_name": "本店・本屋の実験室",
        "neighborhood": "Koenji",
        "tier": 1,
        "why_it_matters": "Bookstore/lab context with zine-event signal. Good fit for local zine events and experimental printed work.",
        "first_action": "Check event/submission pages and whether zine participation is possible.",
    },
    "ZINE FARM TOKYO": {
        "career_category": "zines",
        "opportunity_type": "zine_shop",
        "display_name": "ZINE FARM TOKYO",
        "neighborhood": "Kichijoji",
        "tier": 1,
        "why_it_matters": "Zine-focused Kichijoji target. Strong place to benchmark presentation and potential placement.",
        "first_action": "Confirm current activity and whether they sell/accept outside zines.",
    },
    "Book Culture Club": {
        "career_category": "zines",
        "opportunity_type": "zine_fair_book_community",
        "display_name": "Book Culture Club",
        "neighborhood": "Kichijoji",
        "tier": 1,
        "why_it_matters": "Book/zine community and event signal. Useful for fairs, local network, and creator-to-creator visibility.",
        "first_action": "Review upcoming zine fair/event schedule.",
    },
    "tata bookshop/gallery": {
        "career_category": "zines",
        "opportunity_type": "bookstore_gallery",
        "display_name": "tata bookshop/gallery",
        "neighborhood": "Koenji",
        "tier": 2,
        "why_it_matters": "Bookshop/gallery hybrid in Koenji; good bridge between books, prints, and exhibition context.",
        "first_action": "Visit/research fit and see whether quiet works-on-paper books would sit naturally there.",
    },
    "そぞろ書房": {
        "career_category": "zines",
        "opportunity_type": "independent_bookstore",
        "display_name": "そぞろ書房",
        "neighborhood": "Koenji",
        "tier": 2,
        "why_it_matters": "Small local bookstore target. Useful for building a compact Koenji route.",
        "first_action": "Verify current stock, hours, and whether they handle self-published work.",
    },
    "loneliness books": {
        "career_category": "zines",
        "opportunity_type": "independent_books_zines",
        "display_name": "loneliness books",
        "neighborhood": "Nakano",
        "tier": 2,
        "why_it_matters": "Independent book/zine signal near Nakano. Possible secondary local target after Tacoche.",
        "first_action": "Verify whether it is active and whether it has a physical sales route.",
    },
    "日記屋 月日": {
        "career_category": "zines",
        "opportunity_type": "independent_bookstore",
        "display_name": "日記屋 月日",
        "neighborhood": "Shimokitazawa",
        "tier": 2,
        "why_it_matters": "Independent bookstore with quiet writing/book culture. Potential fit for intimate printed work.",
        "first_action": "Research whether visual zines are appropriate or whether it is more text-focused.",
    },
    "Book Obscura": {
        "career_category": "zines",
        "opportunity_type": "photobook_store",
        "display_name": "Book Obscura",
        "neighborhood": "Kichijoji",
        "tier": 2,
        "why_it_matters": "Photobook specialist. Useful benchmark if her work moves toward photobook/artist-book sequencing.",
        "first_action": "Use as reference and possible later target, not first placement.",
    },
    "Books Ruhe": {
        "career_category": "zines",
        "opportunity_type": "independent_bookstore",
        "display_name": "Books Ruhe",
        "neighborhood": "Kichijoji",
        "tier": 3,
        "why_it_matters": "Independent bookstore in Kichijoji. More general than zine-specific, but useful for local bookstore mapping.",
        "first_action": "Research stock and whether zines/artist books are represented.",
    },
}

def load(path, fallback):
    p = Path(path)
    if p.exists():
        return json.load(open(p, encoding="utf-8"))
    return fallback

def main():
    normalized = load(NORMALIZED, {"opportunities": []})
    by_name = {o.get("canonical_name"): o for o in normalized.get("opportunities", [])}

    targets = []
    for name, meta in ALLOWLIST.items():
        source = by_name.get(name, {})
        target = {
            **meta,
            "canonical_name": name,
            "confidence": source.get("confidence", 70 if meta["tier"] == 1 else 55),
            "source_count": source.get("source_count", 0),
            "websites": source.get("websites", []),
            "article_references": source.get("article_references", []),
            "status": "needs_review",
            "show_on_website": True,
        }
        targets.append(target)

    targets.sort(key=lambda x: (x["tier"], -x["confidence"], x["display_name"]))

    result = {
        "career_category": "zines",
        "title": "Zines / Artist Books",
        "target_count": len(targets),
        "targets": targets,
        "excluded_note": "Article-only results, listicles, generic guides, and vague event references are excluded from the website-facing list.",
    }

    Path("memory").mkdir(exist_ok=True)
    json.dump(result, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    by_neighborhood = Counter(t["neighborhood"] for t in targets)
    by_type = Counter(t["opportunity_type"] for t in targets)

    lines = [
        "# Zine Category Targets",
        "",
        f"- Website-ready targets: {len(targets)}",
        "",
        "## By Neighborhood",
    ]

    for k, v in by_neighborhood.most_common():
        lines.append(f"- {k}: {v}")

    lines += ["", "## By Type"]
    for k, v in by_type.most_common():
        lines.append(f"- {k}: {v}")

    lines += ["", "## Targets"]
    for t in targets:
        lines.append(f"### {t['display_name']}")
        lines.append(f"- Tier: {t['tier']}")
        lines.append(f"- Neighborhood: {t['neighborhood']}")
        lines.append(f"- Type: {t['opportunity_type']}")
        lines.append(f"- Confidence: {t['confidence']}")
        lines.append(f"- Why it matters: {t['why_it_matters']}")
        lines.append(f"- First action: {t['first_action']}")
        if t.get("websites"):
            lines.append("- Websites:")
            for w in t["websites"][:3]:
                lines.append(f"  - {w}")
        lines.append("")

    Path("reports").mkdir(exist_ok=True)
    Path(OUT_REPORT).write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)
    print("Targets:", len(targets))

if __name__ == "__main__":
    main()
