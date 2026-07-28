"""
Japanese & Chinese Discovery Engine

Searches Japanese and Chinese-language art communities for open calls,
exhibitions, and publication opportunities relevant to GEGYjiji's practice
(watercolor, illustration, urban observation, Tokyo-based).

Source groups:
  JP — Twitter/X (公募 水彩 イラスト), note.com (公募展), bijutsutecho.com,
       Japanese gallery and art magazine sites, Tokyo open call aggregators
  CN — Weibo (征稿 展览 插画), Lofter, Zcool, Chinese art magazines
  DIASPORA — Chinese artist communities in Tokyo, Singapore, Vancouver, Toronto

Flow:
  1. Run Tavily queries against each source group
  2. Ask Claude to extract structured opportunities from the snippets
  3. Deduplicate against existing compact_opportunities.json
  4. Append new finds, save report + discovery log

Output:
  deploy_data/compact_opportunities.json  (appends new items)
  memory/jc_discovery_log.json            (query cache + run history)
  reports/jc_discovery_report.md          (human-readable summary)
"""

import sys
import json
import os
import re
import time
import argparse
from pathlib import Path
from datetime import datetime

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

import anthropic
from tavily import TavilyClient

ROOT        = Path(__file__).parent.parent
MEM         = ROOT / "memory"
OPP_PATH    = ROOT / "deploy_data" / "compact_opportunities.json"
LOG_PATH    = MEM / "jc_discovery_log.json"
REPORT_PATH = ROOT / "reports" / "jc_discovery_report.md"

CACHE_DAYS    = 7
QUERY_PAUSE   = 3.5
SNIPPET_CHARS = 600
MAX_SNIPPETS  = 6

tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
claude = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

TODAY = datetime.now().strftime("%Y-%m-%d")


# ── Query catalogue ────────────────────────────────────────────────────────────

QUERIES = [

    # ── Japanese: Twitter/X ───────────────────────────────────────────────────
    {
        "id": "jp_twitter_koubo_watercolor",
        "group": "JP",
        "lang": "ja",
        "q": "公募 水彩 イラスト 2026 締切",
        "domains": ["x.com", "twitter.com"],
    },
    {
        "id": "jp_twitter_gallery_koubo",
        "group": "JP",
        "lang": "ja",
        "q": "ギャラリー 公募 展示 絵画 水彩 東京 2026",
        "domains": ["x.com", "twitter.com"],
    },
    {
        "id": "jp_twitter_artist_recruit",
        "group": "JP",
        "lang": "ja",
        "q": "アーティスト募集 公募展 水彩 イラスト",
        "domains": ["x.com", "twitter.com"],
    },

    # ── Japanese: note.com ────────────────────────────────────────────────────
    {
        "id": "jp_note_koubo_artist",
        "group": "JP",
        "lang": "ja",
        "q": "公募展 アーティスト募集 水彩 2026",
        "domains": ["note.com"],
    },
    {
        "id": "jp_note_gallery_open",
        "group": "JP",
        "lang": "ja",
        "q": "ギャラリー 公募 展覧会 イラスト 締切 2026",
        "domains": ["note.com"],
    },

    # ── Japanese: bijutsutecho.com ────────────────────────────────────────────
    {
        "id": "jp_bijutsutecho_koubo",
        "group": "JP",
        "lang": "ja",
        "q": "公募 展覧会 水彩 絵画 2026 東京",
        "domains": ["bijutsutecho.com"],
    },
    {
        "id": "jp_bijutsutecho_open_call",
        "group": "JP",
        "lang": "ja",
        "q": "アーティスト 公募 絵画 水彩 イラスト 募集 2026",
        "domains": ["bijutsutecho.com"],
    },

    # ── Japanese: broad gallery search ───────────────────────────────────────
    {
        "id": "jp_tokyo_gallery_watercolor",
        "group": "JP",
        "lang": "ja",
        "q": "東京 ギャラリー 公募 水彩画 イラスト 2026 締切",
        "domains": [],
    },
    {
        "id": "jp_watercolor_open_call",
        "group": "JP",
        "lang": "ja",
        "q": "水彩 公募展 2026 日本",
        "domains": [],
    },
    {
        "id": "jp_illustration_open_call",
        "group": "JP",
        "lang": "ja",
        "q": "イラスト 公募 展示 募集 2026 東京 大阪",
        "domains": [],
    },
    {
        "id": "jp_zine_fair_artist",
        "group": "JP",
        "lang": "ja",
        "q": "アートブックフェア 出展者 募集 東京 2026",
        "domains": [],
    },
    {
        "id": "jp_cafe_gallery_recruit",
        "group": "JP",
        "lang": "ja",
        "q": "カフェ ギャラリー 展示 募集 イラスト 水彩 東京 2026",
        "domains": [],
    },

    # ── Chinese: Weibo ────────────────────────────────────────────────────────
    {
        "id": "cn_weibo_zhengao_watercolor",
        "group": "CN",
        "lang": "zh",
        "q": "征稿 水彩 插画 2026 截止日期",
        "domains": ["weibo.com"],
    },
    {
        "id": "cn_weibo_exhibition_open",
        "group": "CN",
        "lang": "zh",
        "q": "展览 征集 水彩画 艺术家 2026",
        "domains": ["weibo.com"],
    },
    {
        "id": "cn_weibo_illustration_call",
        "group": "CN",
        "lang": "zh",
        "q": "插画 征稿 展览 公开征集 2026",
        "domains": ["weibo.com"],
    },

    # ── Chinese: Lofter ───────────────────────────────────────────────────────
    {
        "id": "cn_lofter_watercolor",
        "group": "CN",
        "lang": "zh",
        "q": "水彩 插画 征稿 展览 2026",
        "domains": ["lofter.com"],
    },
    {
        "id": "cn_lofter_art_recruit",
        "group": "CN",
        "lang": "zh",
        "q": "艺术家 水彩 绘画 插画 征集 展示 2026",
        "domains": ["lofter.com"],
    },

    # ── Chinese: Zcool ────────────────────────────────────────────────────────
    {
        "id": "cn_zcool_illustration_call",
        "group": "CN",
        "lang": "zh",
        "q": "插画 征稿 设计 展览 水彩 2026",
        "domains": ["zcool.com.cn"],
    },
    {
        "id": "cn_zcool_open_call",
        "group": "CN",
        "lang": "zh",
        "q": "水彩 插画 绘画 公开征集 展示 2026 截止",
        "domains": ["zcool.com.cn"],
    },

    # ── Chinese: broad art magazine / community search ────────────────────────
    {
        "id": "cn_broad_watercolor_exhibition",
        "group": "CN",
        "lang": "zh",
        "q": "水彩画 征稿 展览 2026 截止日期 申请",
        "domains": [],
    },
    {
        "id": "cn_illustration_magazine_call",
        "group": "CN",
        "lang": "zh",
        "q": "插画 绘画 展览 征稿 艺术家 2026",
        "domains": [],
    },
    {
        "id": "cn_art_competition",
        "group": "CN",
        "lang": "zh",
        "q": "水彩 插画 比赛 艺术大赛 2026 国际",
        "domains": [],
    },

    # ── Chinese diaspora: Tokyo ───────────────────────────────────────────────
    {
        "id": "diaspora_tokyo_chinese_art",
        "group": "DIASPORA",
        "lang": "mixed",
        "q": "在日华人 水彩 绘画 插画 展览 公募 东京 2026",
        "domains": [],
    },
    {
        "id": "diaspora_tokyo_chinese_gallery",
        "group": "DIASPORA",
        "lang": "mixed",
        "q": "Tokyo Chinese artist watercolor illustration exhibition open call gallery 2026",
        "domains": [],
    },
    {
        "id": "diaspora_tokyo_illustration",
        "group": "DIASPORA",
        "lang": "mixed",
        "q": "东京 华人 插画 水彩 艺术家 展示 2026",
        "domains": [],
    },

    # ── Chinese diaspora: Singapore ───────────────────────────────────────────
    {
        "id": "diaspora_sg_art_call",
        "group": "DIASPORA",
        "lang": "mixed",
        "q": "Singapore Chinese artist open call exhibition watercolor illustration 2026",
        "domains": [],
    },
    {
        "id": "diaspora_sg_chinese",
        "group": "DIASPORA",
        "lang": "mixed",
        "q": "新加坡 华人 水彩 插画 艺术家 征稿 展览 2026",
        "domains": [],
    },

    # ── Chinese diaspora: Vancouver ───────────────────────────────────────────
    {
        "id": "diaspora_van_open_call",
        "group": "DIASPORA",
        "lang": "mixed",
        "q": "Vancouver Chinese artist open call watercolor illustration 2026",
        "domains": [],
    },
    {
        "id": "diaspora_van_chinese",
        "group": "DIASPORA",
        "lang": "mixed",
        "q": "温哥华 华人艺术家 水彩 插画 征稿 展览 2026",
        "domains": [],
    },

    # ── Chinese diaspora: Toronto ─────────────────────────────────────────────
    {
        "id": "diaspora_tor_open_call",
        "group": "DIASPORA",
        "lang": "mixed",
        "q": "Toronto Chinese artist open call exhibition watercolor 2026",
        "domains": [],
    },
    {
        "id": "diaspora_tor_chinese",
        "group": "DIASPORA",
        "lang": "mixed",
        "q": "多伦多 华人艺术家 征稿 展览 水彩 2026",
        "domains": [],
    },

    # ── Publications & Editorial — Japanese ──────────────────────────────────
    {
        "id": "jp_editorial_magazine_call",
        "group": "JP_EDITORIAL",
        "lang": "ja",
        "q": "イラスト 挿絵 雑誌 掲載 募集 水彩 2026 イラストレーター",
        "domains": [],
    },
    {
        "id": "jp_art_magazine_contributor",
        "group": "JP_EDITORIAL",
        "lang": "ja",
        "q": "美術手帖 pen magazine アーティスト 寄稿 掲載 水彩 イラスト 募集",
        "domains": ["bijutsutecho.com"],
    },
    {
        "id": "jp_book_cover_illustration",
        "group": "JP_EDITORIAL",
        "lang": "ja",
        "q": "ブックカバー 表紙 挿絵 イラスト 依頼 募集 2026 出版社",
        "domains": [],
    },
    {
        "id": "jp_editorial_twitter",
        "group": "JP_EDITORIAL",
        "lang": "ja",
        "q": "イラスト 挿絵 雑誌 約稿 募集 水彩 イラストレーター 2026",
        "domains": ["x.com", "twitter.com"],
    },

    # ── Publications & Editorial — Chinese ───────────────────────────────────
    {
        "id": "cn_editorial_illustration",
        "group": "CN_EDITORIAL",
        "lang": "zh",
        "q": "插画 杂志 约稿 编辑插画 封面插画 2026 征稿 水彩",
        "domains": [],
    },
    {
        "id": "cn_book_cover_call",
        "group": "CN_EDITORIAL",
        "lang": "zh",
        "q": "书封插画 封面设计 出版社 约稿 水彩 插画师 2026",
        "domains": [],
    },

    # ── Competitions & Awards — Japanese ─────────────────────────────────────
    {
        "id": "jp_watercolor_competition",
        "group": "JP_COMPETITION",
        "lang": "ja",
        "q": "水彩 コンクール 大賞 入賞 公募 2026 応募",
        "domains": [],
    },
    {
        "id": "jp_illustration_award",
        "group": "JP_COMPETITION",
        "lang": "ja",
        "q": "イラストレーション 大賞 コンテスト 新人賞 公募 2026 応募",
        "domains": [],
    },
    {
        "id": "jp_emerging_artist_prize",
        "group": "JP_COMPETITION",
        "lang": "ja",
        "q": "若手アーティスト 賞 コンクール 絵画 水彩 イラスト 新人 2026",
        "domains": [],
    },
    {
        "id": "jp_competition_bijutsutecho",
        "group": "JP_COMPETITION",
        "lang": "ja",
        "q": "コンクール 大賞 水彩 絵画 イラスト 新人 2026",
        "domains": ["bijutsutecho.com"],
    },

    # ── Competitions & Awards — Chinese ──────────────────────────────────────
    {
        "id": "cn_watercolor_competition",
        "group": "CN_COMPETITION",
        "lang": "zh",
        "q": "水彩 插画 比赛 大赛 奖项 新人奖 2026 国际",
        "domains": [],
    },
    {
        "id": "cn_illustration_prize",
        "group": "CN_COMPETITION",
        "lang": "zh",
        "q": "插画 绘画 大赛 征集 奖励 2026 水彩 艺术家",
        "domains": [],
    },

    # ── Expanded 2026-07-28: discovery was capped at 43+10 queries,
    #    which was the ceiling on how much NEW work the system could find.
    #    Re-milling known items produced 0 new opportunities per credit;
    #    these produce ~2.7. Breadth is pinned by tests/test_discovery_queries.py.
    {
        "id": 'jp_city_koubo_0',
        "group": 'JP',
        "lang": 'ja',
        "q": "東京 公募 展示 水彩 絵画 2026 募集",
        "domains": [],
    },
    {
        "id": 'jp_city_gallery_0',
        "group": 'JP',
        "lang": 'ja',
        "q": "東京 ギャラリー 作家募集 展示 イラスト 2026",
        "domains": [],
    },
    {
        "id": 'jp_city_koubo_1',
        "group": 'JP',
        "lang": 'ja',
        "q": "大阪 公募 展示 水彩 絵画 2026 募集",
        "domains": [],
    },
    {
        "id": 'jp_city_gallery_1',
        "group": 'JP',
        "lang": 'ja',
        "q": "大阪 ギャラリー 作家募集 展示 イラスト 2026",
        "domains": [],
    },
    {
        "id": 'jp_city_koubo_2',
        "group": 'JP',
        "lang": 'ja',
        "q": "京都 公募 展示 水彩 絵画 2026 募集",
        "domains": [],
    },
    {
        "id": 'jp_city_gallery_2',
        "group": 'JP',
        "lang": 'ja',
        "q": "京都 ギャラリー 作家募集 展示 イラスト 2026",
        "domains": [],
    },
    {
        "id": 'jp_city_koubo_3',
        "group": 'JP',
        "lang": 'ja',
        "q": "名古屋 公募 展示 水彩 絵画 2026 募集",
        "domains": [],
    },
    {
        "id": 'jp_city_gallery_3',
        "group": 'JP',
        "lang": 'ja',
        "q": "名古屋 ギャラリー 作家募集 展示 イラスト 2026",
        "domains": [],
    },
    {
        "id": 'jp_city_koubo_4',
        "group": 'JP',
        "lang": 'ja',
        "q": "横浜 公募 展示 水彩 絵画 2026 募集",
        "domains": [],
    },
    {
        "id": 'jp_city_gallery_4',
        "group": 'JP',
        "lang": 'ja',
        "q": "横浜 ギャラリー 作家募集 展示 イラスト 2026",
        "domains": [],
    },
    {
        "id": 'jp_city_koubo_5',
        "group": 'JP',
        "lang": 'ja',
        "q": "福岡 公募 展示 水彩 絵画 2026 募集",
        "domains": [],
    },
    {
        "id": 'jp_city_gallery_5',
        "group": 'JP',
        "lang": 'ja',
        "q": "福岡 ギャラリー 作家募集 展示 イラスト 2026",
        "domains": [],
    },
    {
        "id": 'jp_city_koubo_6',
        "group": 'JP',
        "lang": 'ja',
        "q": "神戸 公募 展示 水彩 絵画 2026 募集",
        "domains": [],
    },
    {
        "id": 'jp_city_gallery_6',
        "group": 'JP',
        "lang": 'ja',
        "q": "神戸 ギャラリー 作家募集 展示 イラスト 2026",
        "domains": [],
    },
    {
        "id": 'jp_city_koubo_7',
        "group": 'JP',
        "lang": 'ja',
        "q": "札幌 公募 展示 水彩 絵画 2026 募集",
        "domains": [],
    },
    {
        "id": 'jp_city_gallery_7',
        "group": 'JP',
        "lang": 'ja',
        "q": "札幌 ギャラリー 作家募集 展示 イラスト 2026",
        "domains": [],
    },
    {
        "id": 'jp_city_koubo_8',
        "group": 'JP',
        "lang": 'ja',
        "q": "仙台 公募 展示 水彩 絵画 2026 募集",
        "domains": [],
    },
    {
        "id": 'jp_city_gallery_8',
        "group": 'JP',
        "lang": 'ja',
        "q": "仙台 ギャラリー 作家募集 展示 イラスト 2026",
        "domains": [],
    },
    {
        "id": 'jp_city_koubo_9',
        "group": 'JP',
        "lang": 'ja',
        "q": "金沢 公募 展示 水彩 絵画 2026 募集",
        "domains": [],
    },
    {
        "id": 'jp_city_gallery_9',
        "group": 'JP',
        "lang": 'ja',
        "q": "金沢 ギャラリー 作家募集 展示 イラスト 2026",
        "domains": [],
    },
    {
        "id": 'jp_venue_0',
        "group": 'JP',
        "lang": 'ja',
        "q": "貸しギャラリー 作家募集 展示 水彩 イラスト 2026",
        "domains": [],
    },
    {
        "id": 'jp_venue_1',
        "group": 'JP',
        "lang": 'ja',
        "q": "カフェギャラリー 作家募集 展示 水彩 イラスト 2026",
        "domains": [],
    },
    {
        "id": 'jp_venue_2',
        "group": 'JP',
        "lang": 'ja',
        "q": "書店 ギャラリー 作家募集 展示 水彩 イラスト 2026",
        "domains": [],
    },
    {
        "id": 'jp_venue_3',
        "group": 'JP',
        "lang": 'ja',
        "q": "アートスペース 作家募集 展示 水彩 イラスト 2026",
        "domains": [],
    },
    {
        "id": 'jp_venue_4',
        "group": 'JP',
        "lang": 'ja',
        "q": "画廊 作家募集 展示 水彩 イラスト 2026",
        "domains": [],
    },
    {
        "id": 'jp_venue_5',
        "group": 'JP',
        "lang": 'ja',
        "q": "レンタルスペース 作家募集 展示 水彩 イラスト 2026",
        "domains": [],
    },
    {
        "id": 'jp_format_0',
        "group": 'JP',
        "lang": 'ja',
        "q": "個展 募集 水彩 絵画 締切 2026 2027",
        "domains": [],
    },
    {
        "id": 'jp_format_1',
        "group": 'JP',
        "lang": 'ja',
        "q": "グループ展 募集 水彩 絵画 締切 2026 2027",
        "domains": [],
    },
    {
        "id": 'jp_format_2',
        "group": 'JP',
        "lang": 'ja',
        "q": "二人展 募集 水彩 絵画 締切 2026 2027",
        "domains": [],
    },
    {
        "id": 'jp_format_3',
        "group": 'JP',
        "lang": 'ja',
        "q": "公募展 募集 水彩 絵画 締切 2026 2027",
        "domains": [],
    },
    {
        "id": 'jp_format_4',
        "group": 'JP',
        "lang": 'ja',
        "q": "企画展 募集 水彩 絵画 締切 2026 2027",
        "domains": [],
    },
    {
        "id": 'jp_format_5',
        "group": 'JP',
        "lang": 'ja',
        "q": "小作品展 募集 水彩 絵画 締切 2026 2027",
        "domains": [],
    },
    {
        "id": 'jp_medium_0',
        "group": 'JP',
        "lang": 'ja',
        "q": "水彩 展覧会 出展者募集 2026 応募要項",
        "domains": [],
    },
    {
        "id": 'jp_medium_1',
        "group": 'JP',
        "lang": 'ja',
        "q": "透明水彩 展覧会 出展者募集 2026 応募要項",
        "domains": [],
    },
    {
        "id": 'jp_medium_2',
        "group": 'JP',
        "lang": 'ja',
        "q": "水彩画 展覧会 出展者募集 2026 応募要項",
        "domains": [],
    },
    {
        "id": 'jp_medium_3',
        "group": 'JP',
        "lang": 'ja',
        "q": "ドローイング 展覧会 出展者募集 2026 応募要項",
        "domains": [],
    },
    {
        "id": 'jp_medium_4',
        "group": 'JP',
        "lang": 'ja',
        "q": "原画 展覧会 出展者募集 2026 応募要項",
        "domains": [],
    },
    {
        "id": 'jp_medium_5',
        "group": 'JP',
        "lang": 'ja',
        "q": "絵画 展覧会 出展者募集 2026 応募要項",
        "domains": [],
    },
    {
        "id": 'jp_medium_6',
        "group": 'JP',
        "lang": 'ja',
        "q": "イラスト 展覧会 出展者募集 2026 応募要項",
        "domains": [],
    },
    {
        "id": 'jp_residency_0',
        "group": 'JP_RESIDENCY',
        "lang": 'ja',
        "q": "アーティスト・イン・レジデンス 募集 2026 2027 美術",
        "domains": [],
    },
    {
        "id": 'jp_residency_1',
        "group": 'JP_RESIDENCY',
        "lang": 'ja',
        "q": "レジデンス プログラム 公募 アーティスト 日本 2026",
        "domains": [],
    },
    {
        "id": 'jp_residency_2',
        "group": 'JP_RESIDENCY',
        "lang": 'ja',
        "q": "滞在制作 募集 アーティスト 2026 絵画",
        "domains": [],
    },
    {
        "id": 'jp_residency_3',
        "group": 'JP_RESIDENCY',
        "lang": 'ja',
        "q": "スタジオ 公募 若手作家 支援 2026",
        "domains": [],
    },
    {
        "id": 'jp_editorial_x_0',
        "group": 'JP_EDITORIAL',
        "lang": 'ja',
        "q": "イラストレーター 募集 雑誌 挿絵 2026",
        "domains": [],
    },
    {
        "id": 'jp_editorial_x_1',
        "group": 'JP_EDITORIAL',
        "lang": 'ja',
        "q": "作品集 画集 出版 公募 イラスト 2026",
        "domains": [],
    },
    {
        "id": 'jp_editorial_x_2',
        "group": 'JP_EDITORIAL',
        "lang": 'ja',
        "q": "書籍 装画 イラスト 募集 2026",
        "domains": [],
    },
    {
        "id": 'jp_editorial_x_3',
        "group": 'JP_EDITORIAL',
        "lang": 'ja',
        "q": "web連載 イラスト 寄稿 募集 2026",
        "domains": [],
    },
    {
        "id": 'jp_editorial_x_4',
        "group": 'JP_EDITORIAL',
        "lang": 'ja',
        "q": "アートブック 出展募集 2026 2027",
        "domains": [],
    },
    {
        "id": 'jp_editorial_x_5',
        "group": 'JP_EDITORIAL',
        "lang": 'ja',
        "q": "ZINE 即売会 出展 募集 2026",
        "domains": [],
    },
    {
        "id": 'jp_book_0',
        "group": 'JP_BOOK',
        "lang": 'ja',
        "q": "アートブックフェア 出展募集 2026 2027",
        "domains": [],
    },
    {
        "id": 'jp_book_1',
        "group": 'JP_BOOK',
        "lang": 'ja',
        "q": "リトルプレス 委託販売 募集 書店",
        "domains": [],
    },
    {
        "id": 'jp_book_2',
        "group": 'JP_BOOK',
        "lang": 'ja',
        "q": "独立系書店 委託 作品 販売 募集",
        "domains": [],
    },
    {
        "id": 'jp_book_3',
        "group": 'JP_BOOK',
        "lang": 'ja',
        "q": "文学フリマ アート 出展 2026",
        "domains": [],
    },
    {
        "id": 'jp_book_4',
        "group": 'JP_BOOK',
        "lang": 'ja',
        "q": "紙もの 雑貨 作家 委託 募集 2026",
        "domains": [],
    },
    {
        "id": 'jp_season_0',
        "group": 'JP',
        "lang": 'ja',
        "q": "公募 展覧会 2027 募集開始 絵画",
        "domains": [],
    },
    {
        "id": 'jp_season_1',
        "group": 'JP',
        "lang": 'ja',
        "q": "2026年秋 公募展 水彩 締切",
        "domains": [],
    },
    {
        "id": 'jp_season_2',
        "group": 'JP',
        "lang": 'ja',
        "q": "2027年度 助成 展示 公募 美術",
        "domains": [],
    },
    {
        "id": 'jp_season_3',
        "group": 'JP',
        "lang": 'ja',
        "q": "年間スケジュール 公募展 絵画 2026 2027",
        "domains": [],
    },
    {
        "id": 'jp_x_extra_0',
        "group": 'JP',
        "lang": 'ja',
        "q": "公募 展示 募集 水彩 締切間近",
        "domains": ['x.com', 'twitter.com'],
    },
    {
        "id": 'jp_x_extra_1',
        "group": 'JP',
        "lang": 'ja',
        "q": "作家募集 ギャラリー 空き 2026",
        "domains": ['x.com', 'twitter.com'],
    },
    {
        "id": 'jp_x_extra_2',
        "group": 'JP',
        "lang": 'ja',
        "q": "個展 募集 ギャラリー 貸し",
        "domains": ['x.com', 'twitter.com'],
    },
    {
        "id": 'jp_note_extra_0',
        "group": 'JP',
        "lang": 'ja',
        "q": "公募 レポート 展示 応募 水彩 2026",
        "domains": ['note.com'],
    },
    {
        "id": 'jp_note_extra_1',
        "group": 'JP',
        "lang": 'ja',
        "q": "ギャラリー 個展 費用 募集 2026",
        "domains": ['note.com'],
    },
    {
        "id": 'jp_note_extra_2',
        "group": 'JP',
        "lang": 'ja',
        "q": "コンペ 受賞 水彩 イラスト 2026",
        "domains": ['note.com'],
    },
    {
        "id": 'cn_city_0',
        "group": 'CN',
        "lang": 'zh',
        "q": "北京 画廊 征集 水彩 插画 展览 2026",
        "domains": [],
    },
    {
        "id": 'cn_city_1',
        "group": 'CN',
        "lang": 'zh',
        "q": "上海 画廊 征集 水彩 插画 展览 2026",
        "domains": [],
    },
    {
        "id": 'cn_city_2',
        "group": 'CN',
        "lang": 'zh',
        "q": "广州 画廊 征集 水彩 插画 展览 2026",
        "domains": [],
    },
    {
        "id": 'cn_city_3',
        "group": 'CN',
        "lang": 'zh',
        "q": "深圳 画廊 征集 水彩 插画 展览 2026",
        "domains": [],
    },
    {
        "id": 'cn_city_4',
        "group": 'CN',
        "lang": 'zh',
        "q": "杭州 画廊 征集 水彩 插画 展览 2026",
        "domains": [],
    },
    {
        "id": 'cn_city_5',
        "group": 'CN',
        "lang": 'zh',
        "q": "成都 画廊 征集 水彩 插画 展览 2026",
        "domains": [],
    },
    {
        "id": 'cn_city_6',
        "group": 'CN',
        "lang": 'zh',
        "q": "南京 画廊 征集 水彩 插画 展览 2026",
        "domains": [],
    },
    {
        "id": 'cn_city_7',
        "group": 'CN',
        "lang": 'zh',
        "q": "重庆 画廊 征集 水彩 插画 展览 2026",
        "domains": [],
    },
    {
        "id": 'cn_term_0',
        "group": 'CN',
        "lang": 'zh',
        "q": "水彩 作品 征集 展览 投稿 2026 截止",
        "domains": [],
    },
    {
        "id": 'cn_term_1',
        "group": 'CN',
        "lang": 'zh',
        "q": "插画 作品 征集 展览 投稿 2026 截止",
        "domains": [],
    },
    {
        "id": 'cn_term_2',
        "group": 'CN',
        "lang": 'zh',
        "q": "绘画 作品 征集 展览 投稿 2026 截止",
        "domains": [],
    },
    {
        "id": 'cn_term_3',
        "group": 'CN',
        "lang": 'zh',
        "q": "纸本 作品 征集 展览 投稿 2026 截止",
        "domains": [],
    },
    {
        "id": 'cn_term_4',
        "group": 'CN',
        "lang": 'zh',
        "q": "水彩画 作品 征集 展览 投稿 2026 截止",
        "domains": [],
    },
    {
        "id": 'cn_extra_0',
        "group": 'CN_COMPETITION',
        "lang": 'zh',
        "q": "水彩画 双年展 征稿 2026 2027",
        "domains": [],
    },
    {
        "id": 'cn_extra_1',
        "group": 'CN_COMPETITION',
        "lang": 'zh',
        "q": "青年艺术家 扶持计划 征集 2026",
        "domains": [],
    },
    {
        "id": 'cn_extra_2',
        "group": 'CN_COMPETITION',
        "lang": 'zh',
        "q": "插画师 约稿 出版 征集 2026",
        "domains": [],
    },
    {
        "id": 'cn_extra_3',
        "group": 'CN_COMPETITION',
        "lang": 'zh',
        "q": "artbook 艺术书展 参展 征集 2026",
        "domains": [],
    },
    {
        "id": 'cn_extra_4',
        "group": 'CN_COMPETITION',
        "lang": 'zh',
        "q": "驻地计划 艺术家 申请 2026 2027",
        "domains": [],
    },
    {
        "id": 'cn_extra_5',
        "group": 'CN_COMPETITION',
        "lang": 'zh',
        "q": "美术馆 公开征集 作品 2026 绘画",
        "domains": [],
    },
    {
        "id": 'tw_hk_0',
        "group": 'CN',
        "lang": 'zh',
        "q": "台灣 水彩 徵件 展覽 2026 截止",
        "domains": [],
    },
    {
        "id": 'tw_hk_1',
        "group": 'CN',
        "lang": 'zh',
        "q": "台北 畫廊 徵選 藝術家 2026",
        "domains": [],
    },
    {
        "id": 'tw_hk_2',
        "group": 'CN',
        "lang": 'zh',
        "q": "香港 水彩 插畫 徵集 展覽 2026",
        "domains": [],
    },
    {
        "id": 'tw_hk_3',
        "group": 'CN',
        "lang": 'zh',
        "q": "台灣 藝術家 駐村 申請 2026 2027",
        "domains": [],
    },
    {
        "id": 'tw_hk_4',
        "group": 'CN',
        "lang": 'zh',
        "q": "插畫 比賽 徵件 2026 台灣 水彩",
        "domains": [],
    },
    {
        "id": 'tw_hk_5',
        "group": 'CN',
        "lang": 'zh',
        "q": "獨立書店 寄售 作品 徵集 台灣",
        "domains": [],
    },
    {
        "id": 'diaspora_x_0',
        "group": 'DIASPORA',
        "lang": 'mixed',
        "q": "在日中国人 艺术家 展览 征集 2026",
        "domains": [],
    },
    {
        "id": 'diaspora_x_1',
        "group": 'DIASPORA',
        "lang": 'mixed',
        "q": "华人 艺术家 东京 画廊 展览 2026",
        "domains": [],
    },
    {
        "id": 'diaspora_x_2',
        "group": 'DIASPORA',
        "lang": 'mixed',
        "q": "亚洲 艺术家 交流展 征集 日本 2026",
        "domains": [],
    },
    {
        "id": 'diaspora_x_3',
        "group": 'DIASPORA',
        "lang": 'mixed',
        "q": "国際交流 展覧会 アジア 作家募集 2026",
        "domains": [],
    },
    {
        "id": 'diaspora_x_4',
        "group": 'DIASPORA',
        "lang": 'mixed',
        "q": "asian artist open call Tokyo 2026 watercolour",
        "domains": [],
    },
    {
        "id": 'diaspora_x_5',
        "group": 'DIASPORA',
        "lang": 'mixed',
        "q": "japan based artist open call painting 2026 deadline",
        "domains": [],
    },

    # ── Expanded 2026-07-28: discovery was capped at 43+10 queries,
    #    which was the ceiling on how much NEW work the system could find.
    #    Re-milling known items produced 0 new opportunities per credit;
    #    these produce ~2.7. Breadth is pinned by tests/test_discovery_queries.py.

    # ── Expanded 2026-07-28: discovery was capped at 43+10 queries,
    #    which was the ceiling on how much NEW work the system could find.
    #    Re-milling known items produced 0 new opportunities per credit;
    #    these produce ~2.7. Breadth is pinned by tests/test_discovery_queries.py.
    {
        "id": 'jp_city2_0',
        "group": 'JP',
        "lang": 'ja',
        "q": "広島 展示 公募 作家募集 絵画 2026",
        "domains": [],
    },
    {
        "id": 'jp_city2_1',
        "group": 'JP',
        "lang": 'ja',
        "q": "岡山 展示 公募 作家募集 絵画 2026",
        "domains": [],
    },
    {
        "id": 'jp_city2_2',
        "group": 'JP',
        "lang": 'ja',
        "q": "静岡 展示 公募 作家募集 絵画 2026",
        "domains": [],
    },
    {
        "id": 'jp_city2_3',
        "group": 'JP',
        "lang": 'ja',
        "q": "新潟 展示 公募 作家募集 絵画 2026",
        "domains": [],
    },
    {
        "id": 'jp_city2_4',
        "group": 'JP',
        "lang": 'ja',
        "q": "熊本 展示 公募 作家募集 絵画 2026",
        "domains": [],
    },
    {
        "id": 'jp_city2_5',
        "group": 'JP',
        "lang": 'ja',
        "q": "松山 展示 公募 作家募集 絵画 2026",
        "domains": [],
    },
    {
        "id": 'jp_city2_6',
        "group": 'JP',
        "lang": 'ja',
        "q": "高松 展示 公募 作家募集 絵画 2026",
        "domains": [],
    },
    {
        "id": 'jp_city2_7',
        "group": 'JP',
        "lang": 'ja',
        "q": "長野 展示 公募 作家募集 絵画 2026",
        "domains": [],
    },
    {
        "id": 'jp_city2_8',
        "group": 'JP',
        "lang": 'ja',
        "q": "鎌倉 展示 公募 作家募集 絵画 2026",
        "domains": [],
    },
    {
        "id": 'jp_city2_9',
        "group": 'JP',
        "lang": 'ja',
        "q": "吉祥寺 展示 公募 作家募集 絵画 2026",
        "domains": [],
    },
    {
        "id": 'jp_theme_0',
        "group": 'JP',
        "lang": 'ja',
        "q": "風景画 公募 展覧会 2026 水彩 募集",
        "domains": [],
    },
    {
        "id": 'jp_theme_1',
        "group": 'JP',
        "lang": 'ja',
        "q": "建築 絵画 展示 公募 2026 スケッチ",
        "domains": [],
    },
    {
        "id": 'jp_theme_2',
        "group": 'JP',
        "lang": 'ja',
        "q": "街並み 都市 風景 絵画 公募 2026",
        "domains": [],
    },
    {
        "id": 'jp_theme_3',
        "group": 'JP',
        "lang": 'ja',
        "q": "旅 スケッチ 展示 募集 2026 水彩",
        "domains": [],
    },
    {
        "id": 'jp_theme_4',
        "group": 'JP',
        "lang": 'ja',
        "q": "日常 風景 イラスト 展示 公募 2026",
        "domains": [],
    },
    {
        "id": 'jp_surface_0',
        "group": 'JP',
        "lang": 'ja',
        "q": "百貨店 美術画廊 公募 作家 2026",
        "domains": [],
    },
    {
        "id": 'jp_surface_1',
        "group": 'JP',
        "lang": 'ja',
        "q": "カフェ 展示 募集 イラスト 絵画 2026",
        "domains": [],
    },
    {
        "id": 'jp_surface_2',
        "group": 'JP',
        "lang": 'ja',
        "q": "ホテル アート 作品 募集 展示 2026",
        "domains": [],
    },
    {
        "id": 'jp_surface_3',
        "group": 'JP',
        "lang": 'ja',
        "q": "商業施設 アート 展示 公募 2026",
        "domains": [],
    },
    {
        "id": 'jp_surface_4',
        "group": 'JP',
        "lang": 'ja',
        "q": "美術館 市民ギャラリー 公募 2026 絵画",
        "domains": [],
    },
    {
        "id": 'jp_society_0',
        "group": 'JP_COMPETITION',
        "lang": 'ja',
        "q": "画材メーカー コンペ 水彩 応募 2026",
        "domains": [],
    },
    {
        "id": 'jp_society_1',
        "group": 'JP_COMPETITION',
        "lang": 'ja',
        "q": "水彩連盟 公募展 2026 出品",
        "domains": [],
    },
    {
        "id": 'jp_society_2',
        "group": 'JP_COMPETITION',
        "lang": 'ja',
        "q": "日本水彩画会 公募 2026 応募要項",
        "domains": [],
    },
    {
        "id": 'jp_society_3',
        "group": 'JP_COMPETITION',
        "lang": 'ja',
        "q": "透明水彩 コンクール 2026 募集",
        "domains": [],
    },
    {
        "id": 'jp_society2_0',
        "group": 'JP',
        "lang": 'ja',
        "q": "水彩 写生 大会 公募 2026 入選",
        "domains": [],
    },
    {
        "id": 'jp_society2_1',
        "group": 'JP',
        "lang": 'ja',
        "q": "学生 若手 公募展 絵画 2026 応募",
        "domains": [],
    },
]


# ── Tavily search ──────────────────────────────────────────────────────────────

_QUOTA_ERROR = object()


def run_query(q: str, domains: list) -> str | object:
    """Return snippets string, empty string (no results), or _QUOTA_ERROR."""
    kwargs: dict = {"search_depth": "basic", "max_results": MAX_SNIPPETS}
    if domains:
        kwargs["include_domains"] = domains

    for attempt in range(3):
        try:
            res = tavily.search(q, **kwargs)
            parts = [
                f"[{r.get('url', '')}]\n{r.get('content', '')[:SNIPPET_CHARS]}"
                for r in res.get("results", [])
                if r.get("content", "").strip()
            ]
            time.sleep(QUERY_PAUSE)
            return "\n\n".join(parts)
        except Exception as exc:
            msg = str(exc)
            if "usage limit" in msg.lower() or "plan" in msg.lower():
                print("    Tavily quota exhausted — stopping.")
                return _QUOTA_ERROR
            if "rate" in msg.lower() or "excessive" in msg.lower():
                wait = 20 * (attempt + 1)
                print(f"    rate-limited — waiting {wait}s")
                time.sleep(wait)
            else:
                print(f"    Tavily error: {exc}")
                return ""
    return ""


# ── Claude extraction ──────────────────────────────────────────────────────────

_SYSTEM = """\
You are a research assistant extracting art opportunity listings from web search snippets.
The artist is GEGYjiji — a watercolor and illustration artist based in Tokyo. She works with
urban observation, architecture, memory, and quiet spaces. Her work fits: watercolor open calls,
illustration exhibitions, artist books, zine fairs, café galleries, art book fairs.

Extract ONLY real, concrete opportunities that are explicitly described in the text.
Do NOT invent, infer, or hallucinate venues or deadlines. If a snippet only mentions a past
event, skip it. Return null for any field not found in the source text.
"""

_EXTRACT_PROMPT = """\
Source group: {group}
Language context: {lang}
Search query used: {query}

Web search snippets:
---
{text}
---

Extract all distinct art opportunities visible in these snippets. For each one, return:
  "name"           — full name of the opportunity / exhibition / open call
  "organization"   — gallery, publisher, institution, or community running it
  "category"       — one of: gallery, cafe_gallery, artist_space, fair_popup, bookstore_gallery,
                     bookstore_event, zine_print, market_event, residency, institutional,
                     global_open_call, global_watercolor_open_call, japan_watercolor_open_call,
                     zine_fair_booth, group_publication_open_call, global_residency, event_space,
                     editorial_illustration, magazine_call, book_cover_call,
                     competition_award, illustration_prize, watercolor_competition
  "city"           — city (use "Tokyo" if Japan, "Online" if digital, "International" if unclear)
  "country"        — country name (e.g. "Japan", "China", "Singapore", "Canada", "International")
  "deadline"       — deadline text or date if given, null otherwise
  "fee"            — entry fee text if given, null otherwise
  "submission_url" — direct URL to application/submission page, null if not found
  "contact"        — contact email or URL, null if not found
  "source_url"     — URL of the page where this opportunity was found
  "why_fits"       — one sentence: why this fits a Tokyo-based watercolor/illustration artist
  "source_lang"    — "ja", "zh", or "en"
  "confidence"     — "high" (explicit listing), "medium" (likely current), or "low" (uncertain)

Return a JSON object with key "opportunities" containing an array.
If no real opportunities are found, return {{"opportunities": []}}.
Return only valid JSON, no code fences, no commentary.\
"""


def extract_opportunities(group: str, lang: str, query: str, text: str) -> list[dict]:
    if not text.strip():
        return []

    prompt = _EXTRACT_PROMPT.format(
        group=group, lang=lang, query=query,
        text=text[:5000],
    )
    try:
        resp = claude.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2000,
            system=[{
                "type": "text", "text": _SYSTEM,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": prompt}],
        )
        raw = resp.content[0].text.strip()
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        data = json.loads(raw)
        return data.get("opportunities", [])
    except Exception as exc:
        print(f"    Claude error: {exc}")
        return []


# ── Opportunity normaliser ─────────────────────────────────────────────────────

_VALID_CATS = {
    "gallery", "cafe_gallery", "artist_space", "fair_popup",
    "bookstore_gallery", "bookstore_event", "zine_print", "market_event",
    "residency", "institutional", "global_open_call", "global_watercolor_open_call",
    "japan_watercolor_open_call", "zine_fair_booth", "group_publication_open_call",
    "global_residency", "event_space",
    "editorial_illustration", "magazine_call", "book_cover_call",
    "competition_award", "illustration_prize", "watercolor_competition",
}


def base_score(opp: dict) -> float:
    cat     = opp.get("category", "")
    country = str(opp.get("country", "")).lower()
    conf    = opp.get("confidence", "medium")
    group   = opp.get("_group", "")

    score = 6.5
    if cat in {"japan_watercolor_open_call", "global_watercolor_open_call"}:
        score += 1.2
    if cat in {"cafe_gallery", "bookstore_gallery", "zine_print", "zine_fair_booth"}:
        score += 0.6
    if cat in {"gallery", "artist_space", "institutional"}:
        score += 0.3
    if cat in {"editorial_illustration", "magazine_call", "book_cover_call"}:
        score += 0.8
    if cat in {"competition_award", "illustration_prize", "watercolor_competition"}:
        score += 0.7
    if "japan" in country or country == "":
        score += 0.4
    if group == "DIASPORA":
        score += 0.2
    if conf == "high":
        score += 0.3
    elif conf == "low":
        score -= 0.8
    if opp.get("deadline"):
        score += 0.2
    if opp.get("submission_url"):
        score += 0.2
    return round(min(9.0, max(4.0, score)), 2)


def normalise(raw: dict, query_meta: dict) -> dict | None:
    name = (raw.get("name") or "").strip()
    if not name or len(name) < 4:
        return None

    cat = raw.get("category", "global_open_call")
    if cat not in _VALID_CATS:
        cat = "global_open_call"

    raw["_group"] = query_meta["group"]
    score = base_score(raw)

    org = (raw.get("organization") or name).strip()
    why = (raw.get("why_fits") or f"{org} is an opportunity for watercolor / illustration artists.").strip()

    return {
        "name":                     name,
        "title":                    name,
        "organization":             org,
        "category":                 cat,
        "city":                     (raw.get("city") or "Unknown").strip(),
        "country":                  (raw.get("country") or "Unknown").strip(),
        "source_url":               raw.get("source_url") or raw.get("submission_url") or "",
        "submission_page":          raw.get("submission_url") or "",
        "official_website":         raw.get("source_url") or "",
        "deadline":                 raw.get("deadline") or None,
        "fees":                     raw.get("fee") or None,
        "contact":                  raw.get("contact") or None,
        "overall_score":            score,
        "differentiated_score":     score,
        "watercolor_adjusted_score": score,
        "source_purity_score":      score,
        "one_sentence":             why,
        "why_this_fits_short":      why,
        "quick_action":             "Verify submission page and deadline before applying.",
        "verification_status":      "partial",
        "verification_bucket":      "needs_research",
        "recommendation_visibility": "show",
        "manual_review_needed":     True,
        "deadline_verified":        bool(raw.get("deadline")),
        "fees_verified":            bool(raw.get("fee")),
        "submission_process_known": bool(raw.get("submission_url")),
        "contact_verified":         bool(raw.get("contact")),
        "source_lang":              raw.get("source_lang", "en"),
        "discovery_group":          query_meta["group"],
        "source_type":              "japanese_chinese_discovery",
        "added_by":                 "japanese_chinese_discovery_engine",
        "added_at":                 TODAY,
        "research_priority":        "high" if raw.get("deadline") else "medium",
        "confidence_level":         raw.get("confidence", "medium").capitalize(),
        "tags":                     _make_tags(raw, query_meta["group"]),
    }


def _make_tags(raw: dict, group: str) -> list[str]:
    tags = [group.lower()]
    lang = raw.get("source_lang", "")
    if lang == "ja":
        tags.append("japanese_source")
    elif lang == "zh":
        tags.append("chinese_source")
    if raw.get("deadline"):
        tags.append("has_deadline")
    if raw.get("submission_url"):
        tags.append("has_submission_url")
    cat = raw.get("category", "")
    if "watercolor" in cat:
        tags.append("watercolor_ok")
    country = str(raw.get("country", "")).lower()
    if "japan" in country:
        tags.append("japan")
    if group == "DIASPORA":
        tags.append("diaspora_community")
    return tags


# ── Deduplication ──────────────────────────────────────────────────────────────

def name_key(item: dict) -> str:
    n = (item.get("title") or item.get("name") or "").lower().strip()
    return re.sub(r"\s+", " ", n)


# ── I/O helpers ────────────────────────────────────────────────────────────────

def load_json(path: Path, fallback):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return fallback


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def query_cache_fresh(qid: str, log: dict) -> bool:
    entry = log.get("queries", {}).get(qid, {})
    ts = entry.get("last_run")
    if not ts:
        return False
    try:
        age = (datetime.now() - datetime.fromisoformat(ts)).days
        return age < CACHE_DAYS
    except Exception:
        return False


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Japanese & Chinese Discovery Engine")
    parser.add_argument("--force",   action="store_true",  help="Ignore 7-day query cache")
    parser.add_argument("--max",     type=int, default=0,  help="Max queries to run (0=all)")
    parser.add_argument("--group",   type=str, default="", help="Only run queries for this group: JP, CN, DIASPORA")
    args = parser.parse_args()

    print("=== Japanese & Chinese Discovery Engine ===")
    print(f"Started: {datetime.now().isoformat()}\n")

    existing_opps = load_json(OPP_PATH, [])
    existing_keys = {name_key(o) for o in existing_opps}
    log           = load_json(LOG_PATH, {"queries": {}, "runs": []})

    queries = QUERIES
    if args.group:
        queries = [q for q in queries if q["group"] == args.group.upper()]
    print(f"Queries planned: {len(queries)} | Existing opportunities: {len(existing_opps)}\n")

    all_found: list[dict]  = []
    added:     list[dict]  = []
    run_count: int         = 0
    quota_hit: bool        = False
    group_counts: dict     = {}

    for qmeta in queries:
        qid = qmeta["id"]

        if not args.force and query_cache_fresh(qid, log):
            cached = log["queries"][qid].get("last_run", "?")[:10]
            print(f"  [{qmeta['group']}] {qid} — cached {cached}")
            continue

        if args.max and run_count >= args.max:
            print(f"\nLimit of {args.max} queries reached — stopping.")
            break

        run_count += 1
        print(f"  [{qmeta['group']}] {qid}")
        print(f"    query: {qmeta['q'][:70]}")

        text = run_query(qmeta["q"], qmeta.get("domains", []))
        if text is _QUOTA_ERROR:
            quota_hit = True
            print("  Stopping — Tavily quota exhausted.\n")
            break

        if not text:
            log["queries"][qid] = {"last_run": datetime.now().isoformat(), "found": 0}
            print(f"    no results\n")
            continue

        opps = extract_opportunities(qmeta["group"], qmeta["lang"], qmeta["q"], text)
        print(f"    Claude extracted: {len(opps)} items")

        new_this_query = 0
        for raw in opps:
            norm = normalise(raw, qmeta)
            if not norm:
                continue
            all_found.append(norm)
            key = name_key(norm)
            if key not in existing_keys:
                existing_keys.add(key)
                added.append(norm)
                new_this_query += 1
                g = qmeta["group"]
                group_counts[g] = group_counts.get(g, 0) + 1
                print(f"    + {norm['name'][:60]} [{norm['country']}] score={norm['overall_score']}")

        log["queries"][qid] = {
            "last_run": datetime.now().isoformat(),
            "found":    len(opps),
            "added":    new_this_query,
        }
        print()

    # ── Write results ──────────────────────────────────────────────────────────
    if added:
        existing_opps.extend(added)
        existing_opps.sort(
            key=lambda x: float(x.get("overall_score", 0) or 0),
            reverse=True,
        )
        save_json(OPP_PATH, existing_opps)
        print(f"Wrote {OPP_PATH}")

    log["runs"].append({
        "run_at":    datetime.now().isoformat(),
        "queries_run": run_count,
        "new_opps":  len(added),
        "quota_hit": quota_hit,
        "group_breakdown": group_counts,
    })
    save_json(LOG_PATH, log)

    # ── Report ─────────────────────────────────────────────────────────────────
    lines = [
        "# Japanese & Chinese Discovery Report",
        f"",
        f"Run: {TODAY}  |  Queries run: {run_count}  |  New opportunities: {len(added)}",
        f"",
    ]
    if quota_hit:
        lines += ["**Note:** Tavily quota exhausted — run was cut short.", ""]

    for group in ["JP", "CN", "DIASPORA"]:
        group_opps = [o for o in added if o.get("discovery_group") == group]
        if not group_opps:
            continue
        group_label = {"JP": "Japanese Sources", "CN": "Chinese Sources", "DIASPORA": "Chinese Diaspora"}[group]
        lines += [f"## {group_label} ({len(group_opps)} new)", ""]
        for o in group_opps:
            dl  = f" · {o['deadline']}" if o.get("deadline") else ""
            fee = f" · {o['fees']}" if o.get("fees") else ""
            lines.append(f"- **{o['name']}** [{o['city']}, {o['country']}]{dl}{fee}")
            lines.append(f"  {o['why_this_fits_short']}")
            if o.get("submission_page"):
                lines.append(f"  → {o['submission_page']}")
            lines.append("")

    if not added:
        lines += ["No new opportunities found in this run.", ""]

    lines += [
        "## Stats",
        f"- JP: {group_counts.get('JP', 0)} new",
        f"- CN: {group_counts.get('CN', 0)} new",
        f"- DIASPORA: {group_counts.get('DIASPORA', 0)} new",
        f"- Total in pipeline: {len(existing_opps)}",
        "",
    ]

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

    print(f"\n=== Summary ===")
    print(f"Queries run:       {run_count}")
    print(f"New JP:            {group_counts.get('JP', 0)}")
    print(f"New CN:            {group_counts.get('CN', 0)}")
    print(f"New Diaspora:      {group_counts.get('DIASPORA', 0)}")
    print(f"Total new:         {len(added)}")
    print(f"Pipeline total:    {len(existing_opps)}")
    print(f"Wrote {REPORT_PATH}")
    print(f"Wrote {LOG_PATH}")
    print("\nDone.")


if __name__ == "__main__":
    main()
