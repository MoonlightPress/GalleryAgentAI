
import json
from pathlib import Path

OUT_JSON = Path("memory/multi_ingress_seed_queries.json")
OUT_REPORT = Path("reports/multi_ingress_seed_queries.md")

QUERY_GROUPS = {
    "open_calls_contests": {
        "career_category": "contests",
        "category": "gallery_event",
        "why": "Best structured data: deadlines, fees, eligibility, forms.",
        "queries": [
            "Tokyo art open call 2026 artist submission",
            "Japan illustration contest 2026 open call",
            "Japan art competition 2026 submission",
            "Tokyo gallery open call artist submission",
            "公募 展覧会 東京 アーティスト 募集 2026",
            "イラスト コンテスト 公募 2026",
            "アート 公募 東京 2026",
            "絵画 公募 展覧会 2026",
            "gallery artist open call Japan",
            "artist call for entries Japan 2026",
        ],
    },
    "art_book_zine_fairs": {
        "career_category": "zines",
        "category": "fair_popup",
        "why": "Direct extension of zine crawl; finite list; application windows and booth fees matter.",
        "queries": [
            "Tokyo zine fair 2026 application",
            "Tokyo art book fair application exhibitor",
            "Japan zine fair exhibitor application",
            "artist book fair Japan 2026 exhibitor",
            "ZINE フェス 出展 募集 東京",
            "アートブック フェア 出展 募集",
            "ZINE イベント 出展者募集",
            "independent publishing fair Tokyo exhibitor",
            "book fair artist book Tokyo application",
            "risograph zine fair Tokyo application",
        ],
    },
    "residencies": {
        "career_category": "residencies",
        "category": "residency",
        "why": "Usually structured: duration, deadline, cost, location, eligibility.",
        "queries": [
            "Japan artist residency open call 2026",
            "Tokyo artist residency application 2026",
            "Japan art residency call for applications",
            "アーティスト イン レジデンス 公募 日本 2026",
            "アーティスト レジデンス 募集 東京",
            "artist residency Japan visual artist open call",
            "international artist residency Japan deadline",
            "AIR Japan open call artist",
        ],
    },
    "publishing_small_press": {
        "career_category": "publishing",
        "category": "book_publishing",
        "why": "Best continuation of zines; publishers, art-book platforms, photobook publishers.",
        "queries": [
            "Tokyo small press artist book publisher submission",
            "Japan art book publisher submission",
            "photobook publisher Japan submission",
            "artist book publisher Tokyo contact",
            "リトルプレス 出版社 東京 アートブック",
            "写真集 出版社 持ち込み アーティスト",
            "アートブック 出版社 東京",
            "risograph publisher Japan zine",
            "independent publisher Tokyo artist book",
        ],
    },
}

def main():
    OUT_JSON.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)

    json.dump(QUERY_GROUPS, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    lines = ["# Multi-Ingress Seed Queries", ""]
    for group, data in QUERY_GROUPS.items():
        lines.append(f"## {group}")
        lines.append(f"- Career category: {data['career_category']}")
        lines.append(f"- Card category: {data['category']}")
        lines.append(f"- Why: {data['why']}")
        lines.append("")
        for q in data["queries"]:
            lines.append(f"- {q}")
        lines.append("")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUT_JSON)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
