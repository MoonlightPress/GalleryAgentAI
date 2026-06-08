#!/usr/bin/env python3
"""Add all missing translation keys to translations.js"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

path = 'C:/ScottStuff/GalleryAgentAI/frontend/src/i18n/translations.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

def insert_after(text, target, insertion):
    idx = text.find(target)
    if idx == -1:
        print(f'WARNING: target not found: {target[:60]!r}')
        return text
    return text[:idx + len(target)] + insertion + text[idx + len(target):]

# ── ZH additions ──────────────────────────────────────────────────────────────

zh_cats = """
  'cat.gallery_small':               '小型画廊',
  'cat.book_publishing':             '图书出版',
  'cat.global_art_book_fair':        '国际艺术书展',
  'cat.global_artist_book_platform': '艺术家书籍平台',
  'cat.global_book_arts':            '书籍艺术（国际）',
  'cat.global_grant_fellowship':     '资助与奖学金',
  'cat.global_open_call':            '公开征集（国际）',
  'cat.global_photobook':            '摄影书（国际）',
  'cat.global_residency':            '驻留项目（国际）',
  'cat.global_watercolor_open_call': '水彩公开征集',
  'cat.grant':                       '资助',
  'cat.group_publication_open_call': '合集征稿',
  'cat.japan_watercolor_institution':'日本水彩机构',
  'cat.japan_watercolor_open_call':  '水彩公募（日本）',
  'cat.open_call_index':             '公开征集索引',
  'cat.photo_open_call':             '摄影公募',
  'cat.press_target':                '媒体目标',
  'cat.residency_beijing':           '驻留（北京）',
  'cat.zine_fair_booth':             '独立出版物书展摊位',
  'cat.zine_shop_consignment':       '独立出版物寄售',
"""
content = insert_after(content, "  'cat.gallery_event':       '画廊活动',", zh_cats)

zh_sf_extra = """
  'sf.tier.now':               '当下',
  'sf.tier.near_term':         '近期',
  'sf.tier.medium_term':       '中期',
  'sf.label.pitchColon':       '投稿：',
  'sf.label.contactColon':     '联系：',
  'sf.label.timelineColon':    '时间线：',
  'sf.label.eligibilityColon': '资格要求：',
  'sf.label.deadlineColon':    '截止日期：',
  'sf.label.competitionColon': '竞争情况：',
  'sf.label.tipColon':         '提示：',
  'sf.label.actionColon':      '行动：',
  'sf.label.assessmentTitle':  '综合评估',
  'sf.label.gapTag':           '缺口',
  'sf.label.posts':            '帖子',
  'sf.label.coExhibCount':     '{n}位共同参展者',
  'sf.label.onlineFeatures':   '{n}个线上报道',
  'sf.label.unknownDeadlines': '{n}个截止日期未知',
  'sf.label.primaryBase':      '主要：东京 / 北京',
"""
content = insert_after(content, "  'sf.barrier.high':         '高门槛',", zh_sf_extra)

zh_pp_extra = """  'pp.ex.generic.text':  '"我是一位水彩艺术家，探索记忆与城市空间的主题。"',
  'pp.ex.specific.text': '"我的画是对城市场所的缓慢观察——人来之前的街道，人离去之后的咖啡馆。我用水彩，因为它呈现的正是记忆对建筑的处理方式：模糊的边缘，会呼吸的色彩，几乎精确却又不那么精确的轮廓。"',
"""
content = insert_after(content, "  'pp.ex.specific':          '具体版',", "\n" + zh_pp_extra)

# ── JA additions ──────────────────────────────────────────────────────────────

ja_cats = """
  'cat.gallery_small':               '小規模ギャラリー',
  'cat.book_publishing':             '書籍出版',
  'cat.global_art_book_fair':        '国際アートブックフェア',
  'cat.global_artist_book_platform': 'アーティストブックプラットフォーム',
  'cat.global_book_arts':            '書籍アート（国際）',
  'cat.global_grant_fellowship':     'グラント・フェローシップ',
  'cat.global_open_call':            '公募（国際）',
  'cat.global_photobook':            'フォトブック（国際）',
  'cat.global_residency':            'レジデンシー（国際）',
  'cat.global_watercolor_open_call': '水彩公募',
  'cat.grant':                       'グラント',
  'cat.group_publication_open_call': 'グループ出版公募',
  'cat.japan_watercolor_institution':'日本水彩機関',
  'cat.japan_watercolor_open_call':  '水彩公募（日本）',
  'cat.open_call_index':             '公募インデックス',
  'cat.photo_open_call':             '写真公募',
  'cat.press_target':                'メディアターゲット',
  'cat.residency_beijing':           'レジデンシー（北京）',
  'cat.zine_fair_booth':             'ジンフェアブース',
  'cat.zine_shop_consignment':       'ジンショップ委託',
"""
content = insert_after(content, "  'cat.gallery_event':       'ギャラリーイベント',", ja_cats)

ja_sf_extra = """
  'sf.tier.now':               '今すぐ',
  'sf.tier.near_term':         '近い将来',
  'sf.tier.medium_term':       '中期',
  'sf.label.pitchColon':       '投稿先：',
  'sf.label.contactColon':     '連絡先：',
  'sf.label.timelineColon':    'タイムライン：',
  'sf.label.eligibilityColon': '応募資格：',
  'sf.label.deadlineColon':    '締切：',
  'sf.label.competitionColon': '競争状況：',
  'sf.label.tipColon':         'ヒント：',
  'sf.label.actionColon':      'アクション：',
  'sf.label.assessmentTitle':  '総合評価',
  'sf.label.gapTag':           'ギャップ',
  'sf.label.posts':            '投稿',
  'sf.label.coExhibCount':     '{n}人の共同出展者',
  'sf.label.onlineFeatures':   '{n}件のオンライン掲載',
  'sf.label.unknownDeadlines': '{n}件締切不明',
  'sf.label.primaryBase':      '主拠点：東京 / 北京',
"""
content = insert_after(content, "  'sf.barrier.high':         '高障壁',", ja_sf_extra)

ja_pp_extra = """  'pp.ex.generic.text':  '"水彩を使い、記憶と都市空間をテーマに制作するアーティストです。"',
  'pp.ex.specific.text': '"私の絵は、都市の場所を静かに観察したものです——人が来る前の路地、みんなが去ったあとのカフェ。水彩を選ぶのは、記憶が建築に対して行うことを写し取れるから。やわらかな輪郭、息づく色彩、あやふやだけど確かな形。"',
"""
content = insert_after(content, "  'pp.ex.specific':          '具体的な例',", "\n" + ja_pp_extra)

# ── EN additions ──────────────────────────────────────────────────────────────

en_cats = """
  'cat.gallery_small':               'Small Gallery',
  'cat.book_publishing':             'Book Publishing',
  'cat.global_art_book_fair':        'Art Book Fair',
  'cat.global_artist_book_platform': 'Artist Book Platform',
  'cat.global_book_arts':            'Book Arts (International)',
  'cat.global_grant_fellowship':     'Grant / Fellowship',
  'cat.global_open_call':            'Open Call (International)',
  'cat.global_photobook':            'Photobook (International)',
  'cat.global_residency':            'Residency (International)',
  'cat.global_watercolor_open_call': 'Watercolor Open Call',
  'cat.grant':                       'Grant',
  'cat.group_publication_open_call': 'Group Publication',
  'cat.japan_watercolor_institution':'Watercolor Institution (JP)',
  'cat.japan_watercolor_open_call':  'Watercolor Open Call (JP)',
  'cat.open_call_index':             'Open Call Index',
  'cat.photo_open_call':             'Photography Open Call',
  'cat.press_target':                'Press Target',
  'cat.residency_beijing':           'Residency (Beijing)',
  'cat.zine_fair_booth':             'Zine Fair Booth',
  'cat.zine_shop_consignment':       'Zine Shop Consignment',
"""
content = insert_after(content, "  'cat.gallery_event':       'Gallery Event',", en_cats)

en_sf_extra = """
  'sf.tier.now':               'Now',
  'sf.tier.near_term':         'Near term',
  'sf.tier.medium_term':       'Medium term',
  'sf.label.pitchColon':       'Pitch: ',
  'sf.label.contactColon':     'Contact: ',
  'sf.label.timelineColon':    'Timeline: ',
  'sf.label.eligibilityColon': 'Eligibility: ',
  'sf.label.deadlineColon':    'Deadline: ',
  'sf.label.competitionColon': 'Competition: ',
  'sf.label.tipColon':         'Tip: ',
  'sf.label.actionColon':      'Action: ',
  'sf.label.assessmentTitle':  'Assessment',
  'sf.label.gapTag':           'gap',
  'sf.label.posts':            'posts',
  'sf.label.coExhibCount':     '{n} co-exhibitors',
  'sf.label.onlineFeatures':   '{n} online features',
  'sf.label.unknownDeadlines': '{n} unknown deadlines',
  'sf.label.primaryBase':      'Primary: Tokyo / Beijing',
"""
content = insert_after(content, "  'sf.barrier.high':         'high barrier',", en_sf_extra)

en_pp_extra = """  'pp.ex.generic.text':  '"I am an artist working with watercolor, exploring themes of memory and urban space."',
  'pp.ex.specific.text': '"My paintings are slow observations of urban places between moments — the alley before anyone arrives, the café after everyone has left. I work in watercolor because it captures what memory does to architecture: softened edges, color that breathes, forms that are almost but not quite precise."',
"""
content = insert_after(content, "  'pp.ex.specific':          'Specific',", "\n" + en_pp_extra)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify all keys appear exactly 3 times
checks = [
    'cat.global_open_call', 'cat.press_target', 'cat.zine_shop_consignment',
    'sf.tier.now', 'sf.label.pitchColon', 'sf.label.gapTag',
    'pp.ex.generic.text', 'pp.ex.specific.text',
    'sf.tier.medium_term', 'cat.book_publishing',
]
all_ok = True
for c in checks:
    count = content.count(c)
    ok = count == 3
    if not ok:
        all_ok = False
    print(f"  {c}: {count}x {'OK' if ok else 'PROBLEM'}")

print()
print('All checks passed!' if all_ok else 'SOME CHECKS FAILED')
