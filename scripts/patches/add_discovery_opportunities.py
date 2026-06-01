import json
import sys
from datetime import date

sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('deploy_data/compact_opportunities.json', encoding='utf-8'))
today = date.today().isoformat()

NEW_ENTRIES = [

    # ── CURRENTLY OPEN WATERCOLOR CALL ───────────────────────────────────────
    {
        'title': 'Northwest Watercolor Society 2026 Annual International Open Exhibition',
        'organization': 'Northwest Watercolor Society (NWWS)',
        'category': 'global_watercolor_open_call',
        'city': 'Online / Seattle',
        'country': 'USA',
        'overall_score': 8.2,
        'visual_fit_score': 3.5,
        'source_url': 'https://www.nwws.org/annual-international-open/',
        'submission_page': 'https://www.nwws.org/2026-open-prospectus_final/',
        'deadline': 'July 8, 2026',
        'fees': 'Member reduced / non-member — check prospectus',
        'one_sentence': 'Prestigious annual international watercolor exhibition open to all artists worldwide, $15,000+ in awards, juror Dongfeng Li (Chinese-American watercolor painter). Deadline July 8 2026.',
        'why_this_fits_short': 'Direct medium match, international eligibility, currently open. Juror Dongfeng Li is a Chinese-American watercolor painter — unusually apt cultural fit for GEGYjiji.',
        'quick_action': 'Download 2026 prospectus from nwws.org, confirm entry fee and size requirements, submit before July 8 2026.',
        'three_bullets': [
            'Currently open — deadline July 8, 2026.',
            'Juror is Dongfeng Li, a Chinese-American watercolor painter.',
            'Over $15,000 in awards; international artists explicitly welcome.',
        ],
        'tags': ['global', 'watercolor', 'open_call', 'currently_open', 'prestige'],
        'verification_status': 'partial',
        'url_verification_status': 'ok',
        'research_priority': 'high',
        'manual_review_needed': True,
        'added_at': today,
        'source_type': 'discovery_search',
    },

    # ── WATERCOLOR SOCIETIES — WATCH NEXT CYCLE ──────────────────────────────
    {
        'title': 'National Watercolor Society International Open Exhibition',
        'organization': 'National Watercolor Society (NWS)',
        'category': 'global_watercolor_open_call',
        'city': 'California / Online',
        'country': 'USA',
        'overall_score': 6.5,
        'visual_fit_score': 3.5,
        'source_url': 'https://nationalwatercolorsociety.org/exhibits',
        'submission_page': 'https://artist.callforentry.org/festivals_unique_info.php?ID=17030',
        'deadline': 'Annual — 2026 cycle closed May 22. Watch January 2027.',
        'fees': '$70 non-member, $45 member',
        'one_sentence': 'Major annual international watercolor exhibition, $40,000+ in awards, open to non-members worldwide — 2026 cycle closed.',
        'why_this_fits_short': 'One of the most prestigious watercolor exhibitions globally. 2026 deadline passed but recurs annually. $70 non-member entry, $40,000+ awards.',
        'quick_action': 'Add to 2027 calendar. Check nationalwatercolorsociety.org from January 2027.',
        'three_bullets': [
            '$40,000+ in awards including a $6,000 permanent collection purchase.',
            'Non-member accepted: $70 entry fee.',
            '2026 deadline passed (May 22). Annual — watch January 2027.',
        ],
        'tags': ['global', 'watercolor', 'open_call', 'prestige', 'watch_next_cycle'],
        'status': 'closed',
        'recommendation_visibility': 'hidden',
        'exclusive_primary_bucket': 'reject',
        'cycle_note': '2026 deadline was May 22 — passed. Annual exhibition.',
        'next_cycle_check': '2027-01-01',
        'added_at': today,
        'source_type': 'discovery_search',
    },

    {
        'title': 'Japan International Watercolor Institute Online Exhibition',
        'organization': 'Japan International Watercolor Institute',
        'category': 'japan_watercolor_open_call',
        'city': 'Online / Niigata',
        'country': 'Japan',
        'overall_score': 6.5,
        'visual_fit_score': 4.0,
        'source_url': 'https://iwf.iacn.jp/international-watercolor-exhibition-japan/',
        'submission_page': 'https://iwf.iacn.jp/international-watercolor-exhibition-japan/',
        'deadline': 'Annual — 2026 deadlines March-April. Watch January 2027.',
        'fees': '2000 JPY (approx. $13)',
        'contact_email': 'jiwi2026@iacn.jp',
        'one_sentence': 'Annual Japan-based international watercolor exhibition open to anyone worldwide — very low entry fee, no restrictions on age or nationality.',
        'why_this_fits_short': 'Japan-based, accessible entry fee (2000 yen), open to anyone. Good annual entry point into the Japanese watercolor exhibition ecosystem.',
        'quick_action': 'Apply January 2027. Submit JPG to jiwi2027@iacn.jp with artwork details and pay 2000 yen via PayPal.',
        'three_bullets': [
            'Japan-based, 2000 yen entry — very accessible.',
            'Open to anyone worldwide, no restrictions.',
            '2026 deadlines passed. Annual — apply January 2027.',
        ],
        'tags': ['japan', 'watercolor', 'open_call', 'accessible', 'watch_next_cycle'],
        'status': 'closed',
        'recommendation_visibility': 'hidden',
        'exclusive_primary_bucket': 'reject',
        'cycle_note': '2026 deadlines passed (March-April). Annual exhibition.',
        'next_cycle_check': '2027-01-15',
        'added_at': today,
        'source_type': 'discovery_search',
    },

    {
        'title': 'CSPWC Annual Open Water International Exhibition',
        'organization': 'Canadian Society of Painters in Water Colour',
        'category': 'global_watercolor_open_call',
        'city': 'Toronto',
        'country': 'Canada',
        'overall_score': 7.0,
        'visual_fit_score': 3.0,
        'source_url': 'https://cspwc.ca/',
        'submission_page': 'https://cspwc.ca/',
        'deadline': 'Check cspwc.ca — exhibition September 1-19 2026; deadline likely June-July',
        'fees': 'Unknown — check site',
        'one_sentence': "Canadian Society of Painters in Water Colour annual international juried exhibition in transparent watercolour — exhibition September 2026, submission deadline may still be open.",
        'why_this_fits_short': 'International juried show specifically in transparent watercolour. Exhibition is September 2026 so submission window may still be open — check cspwc.ca urgently.',
        'quick_action': 'Check cspwc.ca immediately for 2026 submission deadline and entry requirements.',
        'three_bullets': [
            'International juried exhibition specifically in transparent watercolour.',
            'Exhibition September 1-19 2026 — submission deadline may still be open.',
            'Verify urgently at cspwc.ca.',
        ],
        'tags': ['global', 'watercolor', 'open_call', 'check_deadline'],
        'verification_status': 'partial',
        'research_priority': 'high',
        'manual_review_needed': True,
        'added_at': today,
        'source_type': 'discovery_search',
    },

    # ── TOKYO RELATIONSHIP TARGETS ────────────────────────────────────────────
    {
        'title': 'Clouds Art + Coffee',
        'organization': 'Clouds Art + Coffee',
        'category': 'cafe_gallery',
        'city': 'Tokyo',
        'country': 'Japan',
        'overall_score': 7.0,
        'visual_fit_score': 3.7,
        'source_url': 'https://www.instagram.com/clouds_koenji/',
        'submission_page': 'https://www.instagram.com/clouds_koenji/',
        'deadline': '',
        'fees': '',
        'one_sentence': 'Koenji cafe-gallery showing rotating work from local and international emerging artists — no censorship, intimate space, strong community fit.',
        'why_this_fits_short': 'Rotating exhibitions, welcomes emerging local and international artists, Koenji neighbourhood. Tier 1 ambient visibility — café prints and wall display.',
        'quick_action': 'DM @clouds_koenji on Instagram or visit in person: 2-25-4 Koenji-kita, Suginami, Tokyo.',
        'three_bullets': [
            'Koenji cafe-gallery, rotating shows, welcomes emerging artists.',
            'No censorship — artists encouraged to represent themselves freely.',
            'Local and international mix — good community fit.',
        ],
        'tags': ['tokyo', 'cafe_gallery', 'koenji', 'relationship_target', 'tier_1'],
        'opportunity_type': 'relationship_target',
        'action_type': 'contact_and_propose',
        'relationship_note': 'Koenji cafe-gallery. Rotating exhibitions, welcomes emerging artists. DM @clouds_koenji or visit in person.',
        'draft_introduction_ja': (
            '件名：水彩画の展示についてのご相談\n\n'
            'はじめまして。東京在住の水彩画家、GEGYjijiと申します。\n'
            '都市の静けさや、光と影、猋といった日常のテーマを水彩で描いています。\n'
            'Cloudsさんのような、アートとコーヒーが共存する空間に作品を展示できれば大変嫌しく思い、'
            'ご連絡いたしました。\n'
            'ご興味がありましたら、ぜひお話しできれば幸いです。'
        ),
        'draft_introduction_en': (
            'Subject: Inquiry about showing watercolor work\n\n'
            'Hello, my name is GEGYjiji, a watercolor artist based in Tokyo.\n'
            'I paint everyday themes in watercolor — the quietness of the city, light and shadow, cats.\n'
            'I reached out hoping there might be an opportunity to show work in a space like Clouds '
            'where art and coffee exist together.\n'
            'If you are interested, I would love to talk.'
        ),
        'url_verification_status': 'ok',
        'added_at': today,
        'source_type': 'discovery_search',
    },

    {
        'title': 'Shimokitazawa Arts',
        'organization': 'Shimokitazawa Arts',
        'category': 'gallery_small',
        'city': 'Tokyo',
        'country': 'Japan',
        'overall_score': 7.2,
        'visual_fit_score': 3.5,
        'source_url': 'https://shimokitazawaarts.tokyo/en/home-english/',
        'submission_page': 'https://shimokitazawaarts.tokyo/en/home-english/',
        'deadline': '',
        'fees': '',
        'contact_email': 'info@shimokitazawaarts.tokyo',
        'one_sentence': 'Shimokitazawa gallery presenting monthly solo exhibitions by younger contemporary Japanese artists — direct email proposal required, no public open call.',
        'why_this_fits_short': 'Monthly solo exhibitions by younger Japanese artists. Shimokitazawa location. No public open call — direct email inquiry. Good Tier 2 networking target.',
        'quick_action': 'Email info@shimokitazawaarts.tokyo with introduction, portfolio PDF, and proposal for a solo or group show.',
        'three_bullets': [
            'Monthly solo exhibitions — active programme, real slots.',
            'Shimokitazawa location, younger artists — culturally aligned.',
            'No public open call; direct email inquiry required.',
        ],
        'tags': ['tokyo', 'gallery', 'shimokitazawa', 'relationship_target', 'tier_2'],
        'opportunity_type': 'relationship_target',
        'action_type': 'contact_and_propose',
        'relationship_note': 'Small gallery in Shimokitazawa showing younger Japanese artists monthly. Direct proposal by email to info@shimokitazawaarts.tokyo.',
        'draft_introduction_ja': (
            '件名：水彩画作品の展示についてのご相談\n\n'
            'はじめまして。東京在住の水彩画家、GEGYjijiと申します。\n'
            '都市の大気感、室内の光、猋などをテーマに、静かで親密な水彩作品を制作しています。\n'
            '下北沢アーツさんで作品をご紹介できる機会について、ご相談できれば大変嫌しく思います。\n'
            'ポートフォリオをお送りすることも可能ですので、どうぞよろしくお願いいたします。'
        ),
        'draft_introduction_en': (
            'Subject: Inquiry about a watercolor exhibition\n\n'
            'Hello, my name is GEGYjiji, a watercolor artist based in Tokyo.\n'
            'I make quiet, intimate watercolor paintings focused on urban atmosphere, interior light, and cats.\n'
            'I would love to discuss the possibility of showing work at Shimokitazawa Arts.\n'
            'I am happy to send a portfolio PDF — thank you for your consideration.'
        ),
        'url_verification_status': 'ok',
        'added_at': today,
        'source_type': 'discovery_search',
    },

    {
        'title': 'Sunny Boy Books',
        'organization': 'Sunny Boy Books',
        'category': 'bookstore_gallery',
        'city': 'Tokyo',
        'country': 'Japan',
        'overall_score': 7.0,
        'visual_fit_score': 3.7,
        'source_url': 'https://www.instagram.com/sunnyboybooks/',
        'submission_page': 'https://www.instagram.com/sunnyboybooks/',
        'deadline': '',
        'fees': '',
        'one_sentence': 'Intimate indie bookshop near Gakugei-Daigaku with 4,000 titles, its own small publishing imprint, and regular artist events — strong Tier 1 consignment target.',
        'why_this_fits_short': 'Tokyo indie bookshop stocking handmade, small-run, and foreign books with its own publishing arm. Strong fit for artist-book and print consignment.',
        'quick_action': 'DM @sunnyboybooks on Instagram or visit near Gakugeidaigaku station to inquire about consignment.',
        'three_bullets': [
            '4,000 books in 16.5m2 — genuine indie curation.',
            'Has its own small publishing imprint — potential collaboration.',
            'Regular author and artist events — community access.',
        ],
        'tags': ['tokyo', 'bookstore', 'zine', 'relationship_target', 'tier_1', 'gakugeidaigaku'],
        'opportunity_type': 'relationship_target',
        'action_type': 'contact_and_propose',
        'relationship_note': 'Indie bookshop near Gakugei-Daigaku. DM @sunnyboybooks. Consignment for artist books or prints.',
        'draft_introduction_ja': (
            '件名：水彩画作品のお取り扱いについてのご相談\n\n'
            'はじめまして。東京を拠点に活動している水彩画家のGEGYjijiと申します。\n'
            '都市の風景や光、猋をテーマに水彩で制作しており、アーティストブックやプリントも制作しています。\n'
            'SUNNY BOY BOOKSさんのような場所で作品をお取り扱いいただける可能性について、'
            'ご相談できれば幸いです。\n'
            'どうぞよろしくお願いいたします。'
        ),
        'draft_introduction_en': (
            'Subject: Inquiry about stocking watercolor work\n\n'
            'Hello, I am GEGYjiji, a watercolor artist based in Tokyo.\n'
            'I paint the city, light, and cats in watercolor, and also make artist books and prints.\n'
            'I would love to discuss the possibility of stocking work at Sunny Boy Books.\n'
            'Thank you for your time.'
        ),
        'url_verification_status': 'ok',
        'added_at': today,
        'source_type': 'discovery_search',
    },

    # ── BEIJING / CHINA ───────────────────────────────────────────────────────
    {
        'title': 'Shangyuan International Residency Programme',
        'organization': 'Shangyuan Art Museum',
        'category': 'residency_beijing',
        'city': 'Beijing',
        'country': 'China',
        'overall_score': 6.5,
        'visual_fit_score': 2.5,
        'source_url': 'http://www.syartmuseum.com/english/',
        'submission_page': 'http://www.syartmuseum.com/english/',
        'deadline': 'Annual — 2026 results announced January. Watch October 2026 for 2027 cycle.',
        'fees': 'Unknown',
        'contact_email': 'shangyuanart@gmail.com',
        'one_sentence': 'Prestigious annual Beijing artist residency selecting 15-30 artists per year, April-November, no age or location restrictions, additional Huangshan studio available.',
        'why_this_fits_short': 'Beijing-based residency directly relevant to Chinese identity and home country. Prestigious, no restrictions. Apply October for next year cycle.',
        'quick_action': 'Apply October 2026 for 2027 cycle. Send portfolio images to shangyuanart@gmail.com.',
        'three_bullets': [
            'Beijing residency — connects to Chinese identity and home country.',
            'No restrictions on age, education, or location.',
            '2026 cycle passed. Apply October 2026 for 2027.',
        ],
        'tags': ['beijing', 'residency', 'china', 'stretch_target', 'tier_4'],
        'status': 'closed',
        'recommendation_visibility': 'hidden',
        'exclusive_primary_bucket': 'reject',
        'cycle_note': '2026 residency results announced January 2026. Apply October 2026 for 2027 cycle.',
        'next_cycle_check': '2026-10-01',
        'added_at': today,
        'source_type': 'discovery_search',
    },

    {
        'title': 'Platform China BIAP Artist Residency',
        'organization': 'Platform China Contemporary Art Institute',
        'category': 'residency_beijing',
        'city': 'Beijing',
        'country': 'China',
        'overall_score': 7.0,
        'visual_fit_score': 2.5,
        'source_url': 'https://www.transartists.org/en/air/platform-china',
        'submission_page': 'https://www.transartists.org/en/air/platform-china',
        'deadline': 'Rolling applications — contact directly',
        'fees': 'Unknown',
        'one_sentence': "Caochangdi Art District Beijing residency, 8-12 weeks, open platform for emerging to established international artists with gallery exhibition opportunity.",
        'why_this_fits_short': 'Beijing open residency in Caochangdi — relevant for when GEGYjiji travels to China. Rolling applications, no fixed deadline. Exhibition opportunity included.',
        'quick_action': 'Email Platform China BIAP directly: No. 319-1 East End Art-A, Caochangdi Village, Chaoyang District, Beijing. Tel: +86-10-6432-0091.',
        'three_bullets': [
            'Caochangdi Art District — Beijing experimental art hub.',
            'Rolling applications — no fixed annual deadline.',
            'Exhibition opportunity at BIAP gallery included.',
        ],
        'tags': ['beijing', 'residency', 'china', 'research_needed', 'tier_3'],
        'verification_status': 'partial',
        'research_priority': 'medium',
        'manual_review_needed': True,
        'added_at': today,
        'source_type': 'discovery_search',
    },

]

existing_titles = {(o.get('title') or o.get('name') or '').strip().lower() for o in data}

added = 0
for e in NEW_ENTRIES:
    t = (e.get('title') or '').strip().lower()
    if t in existing_titles:
        print(f'SKIP (already exists): {e["title"]}')
        continue
    e.setdefault('verification_status', 'partial')
    e.setdefault('manual_review_needed', True)
    e.setdefault('url_verification_status', 'unknown')
    data.append(e)
    existing_titles.add(t)
    added += 1
    print(f'ADDED: {e["title"]}')

json.dump(data, open('deploy_data/compact_opportunities.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print(f'\nTotal added: {added}. Total opportunities: {len(data)}')
