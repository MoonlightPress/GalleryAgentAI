"""
discovery_sources.py — curated catalog of FREE discovery sources.

The free alternative to broad Tavily search: instead of searching the open web,
fetch a known set of source URLs directly (plain HTTP) and parse opportunities
out of them. Her niche is narrow enough that a curated list covers most real
inventory at ~$0. Tavily is reserved for occasional new-venue hunting.

LOCALITY (the key signal):
  - "global"  = open calls / competitions / juried societies she can enter REMOTELY
                from Tokyo (digital/mail-in submission). Geography is not a barrier.
  - "local"   = physical venues / relationships / consignment that require being
                there. Relevant only where she lives (Tokyo) or has ties (China).

This is a STARTING catalog — verify URLs and expand. The scraper engine (next
build) consumes SOURCES: fetch `url`, parse with the `kind`-appropriate strategy,
emit records in the compact_opportunities schema, dedupe against existing.

Schema per source:
  name      — human label
  region    — JP | CN | US | EU | GLOBAL
  lang      — ja | zh | en | fr | ...
  kind      — society | platform | aggregator | venue | magazine
  locality  — global | local
  url       — page to fetch (a calls/submissions index where possible)
  notes     — parsing hints / what it provides
"""

SOURCES = [
    # ─────────────────────────── JAPAN (where she lives) ───────────────────────
    {"name": "Japan Watercolour Society (日本水彩画会)", "region": "JP", "lang": "ja",
     "kind": "society", "locality": "global", "url": "https://www.nihonsuisai.or.jp/",
     "notes": "Annual 日本水彩展 (113th+). Her bullseye. 年月日 dates. Recurring (第N回)."},
    {"name": "公募ガイド (Koubo Guide)", "region": "JP", "lang": "ja",
     "kind": "aggregator", "locality": "global", "url": "https://compe.japandesign.ne.jp/",
     "notes": "Major JP open-call aggregator; filter by 絵画/水彩/イラスト."},
    {"name": "アートコンペ・公募 (artkoubo)", "region": "JP", "lang": "ja",
     "kind": "aggregator", "locality": "global", "url": "https://www.artkoubo.jp/",
     "notes": "Already a source in the corpus (アートオリンピア). Painting open calls."},
    {"name": "夢画材 koubo", "region": "JP", "lang": "ja",
     "kind": "aggregator", "locality": "global", "url": "https://koubo.yumegazai.com/",
     "notes": "Watercolor festival listings (水彩アートの祭典). Recurring annuals."},
    {"name": "二科会 (Nika-kai)", "region": "JP", "lang": "ja",
     "kind": "society", "locality": "global", "url": "https://www.nika.or.jp/",
     "notes": "Major annual public exhibition (二科展). Recurring."},
    {"name": "note.com art-call tags", "region": "JP", "lang": "ja",
     "kind": "aggregator", "locality": "global", "url": "https://note.com/hashtag/公募",
     "notes": "Tag pages for 公募 / 水彩 / イラスト募集. Individual organizer posts."},
    {"name": "美術手帖 (Bijutsu Techo)", "region": "JP", "lang": "ja",
     "kind": "magazine", "locality": "global", "url": "https://bijutsutecho.com/",
     "notes": "Art news + some call listings. Relationship/press target too."},

    # ─────────────────────────── CHINA (her home scene) ────────────────────────
    {"name": "中国美术家协会 (China Artists Association)", "region": "CN", "lang": "zh",
     "kind": "society", "locality": "global", "url": "https://www.caanet.org.cn/",
     "notes": "National 全国美展 + themed 征集. 年月日 dates parse already. Recurring (第N届)."},
    {"name": "雅昌艺术网 (Artron) 展览/征集", "region": "CN", "lang": "zh",
     "kind": "aggregator", "locality": "global", "url": "https://www.artron.net/",
     "notes": "Large CN art portal; exhibition + open-call listings."},
    {"name": "99艺术网 (99ys)", "region": "CN", "lang": "zh",
     "kind": "aggregator", "locality": "global", "url": "https://www.99ys.com/",
     "notes": "CN art news + calls."},
    {"name": "金风车国际青年插画家大赛 (Golden Pinwheel)", "region": "CN", "lang": "zh",
     "kind": "platform", "locality": "global", "url": "https://www.ccppg.com.cn/",
     "notes": "Already in corpus; major annual illustration competition."},
    # City art associations (local physical scene where she has ties):
    {"name": "北京 / 上海 / 广东 美术家协会", "region": "CN", "lang": "zh",
     "kind": "society", "locality": "local", "url": "https://www.caanet.org.cn/",
     "notes": "Provincial/municipal associations (Beijing/Shanghai/Guangdong). City shows."},

    # ─────────────────────────── USA (remote open calls) ───────────────────────
    {"name": "American Watercolor Society (AWS)", "region": "US", "lang": "en",
     "kind": "society", "locality": "global", "url": "https://americanwatercolorsociety.org/",
     "notes": "Annual International Exhibition; accepts non-members. Mail/digital entry."},
    {"name": "National Watercolor Society (NWS)", "region": "US", "lang": "en",
     "kind": "society", "locality": "global", "url": "https://www.nationalwatercolorsociety.org/",
     "notes": "Annual juried international open."},
    {"name": "Northwest Watercolor Society (NWWS)", "region": "US", "lang": "en",
     "kind": "society", "locality": "global", "url": "https://www.nwws.org/",
     "notes": "Already in corpus; open international, digital entry."},
    {"name": "CaFÉ (callforentry.org)", "region": "US", "lang": "en",
     "kind": "platform", "locality": "global", "url": "https://www.callforentry.org/",
     "notes": "THE big US art-call platform. Many painting/watercolor calls, remote-OK."},

    # ─────────────────────────── EUROPE / UK (remote open calls) ───────────────
    {"name": "Royal Watercolour Society (RWS)", "region": "EU", "lang": "en",
     "kind": "society", "locality": "global", "url": "https://www.royalwatercoloursociety.co.uk/",
     "notes": "UK. Open exhibitions accept non-members."},
    {"name": "Royal Institute of Painters in Water Colours (RI)", "region": "EU", "lang": "en",
     "kind": "society", "locality": "global", "url": "https://www.mallgalleries.org.uk/",
     "notes": "UK (Mall Galleries hosts several watercolour open calls)."},
    {"name": "CuratorSpace", "region": "EU", "lang": "en",
     "kind": "platform", "locality": "global", "url": "https://www.curatorspace.com/opportunities",
     "notes": "UK/EU art-call platform. NOTE: index pages were a listing-artifact source — parse the"
              " individual opportunity entries, not the index, per the listing-artifact guard."},
    {"name": "Société Française de l'Aquarelle", "region": "EU", "lang": "fr",
     "kind": "society", "locality": "global", "url": "https://www.societe-francaise-aquarelle.com/",
     "notes": "France. Watercolor society open calls."},

    # ─────────────────────────── GLOBAL aggregators ────────────────────────────
    {"name": "ArtConnect", "region": "GLOBAL", "lang": "en",
     "kind": "aggregator", "locality": "global", "url": "https://www.artconnect.com/opportunities",
     "notes": "Global open-call aggregator (Berlin-based). Filter for painting/remote."},
]


def by_region(region: str):
    return [s for s in SOURCES if s["region"] == region]


def global_open_call_sources():
    """Sources for opportunities she can act on remotely from Tokyo."""
    return [s for s in SOURCES if s["locality"] == "global"]


def local_venue_sources():
    """Physical/relationship sources tied to where she is (Tokyo) or has ties (China)."""
    return [s for s in SOURCES if s["locality"] == "local"]
