"""
fix_medium_tags.py
------------------
Reclassifies native_medium for all entries in deploy_data/compact_opportunities.json
based on text content analysis.

Priority order: watercolor > painting > illustration > book_arts > printmaking
               > photography > digital > mixed > unknown

Also adjusts watercolor_adjusted_score for newly classified entries.
"""

import sys
import json
import re
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

# ---------------------------------------------------------------------------
# Keyword patterns (case-insensitive, checked against lowercased text)
# ---------------------------------------------------------------------------

WATERCOLOR_KEYWORDS = [
    'watercolor', 'watercolour', 'aquarelle', '水彩', 'acuarela', 'aquarela',
    'transparent painting', 'wet-on-wet', '透明水彩',
]

PAINTING_KEYWORDS = [
    'painting', 'oil paint', 'oil on', 'acrylic', 'gouache', 'tempera',
    '油彩', '絵画', '画展', 'fine art', 'visual art',
]

ILLUSTRATION_KEYWORDS = [
    'illustration', 'illustrator', 'イラスト', '插画', "children's book",
    'editorial illustration', 'illustrative',
]

BOOK_ARTS_KEYWORDS = [
    'book art', 'book fair', 'zine', 'publication', 'small press', 'bookshop',
    'artist book', 'printed matter', 'book shop', 'zines', 'publishing',
    '本の', '本展', 'book making', 'bookmaking', 'handmade book',
]

PRINTMAKING_KEYWORDS = [
    'printmaking', 'print making', 'etching', 'lithograph', 'woodblock',
    'screenprint', 'screen print', 'silkscreen', '版画', 'intaglio', 'relief print',
    'monotype', 'monoprint', 'linocut',
]

PHOTOGRAPHY_KEYWORDS = [
    'photo', 'photography', 'photographer', 'camera', 'lens', 'darkroom',
    'film photography', 'digital photography', '写真',
]

DIGITAL_KEYWORDS = [
    'digital art', 'nft', 'generative art', 'generative', 'computational art',
    'pixel art', 'digital illustration', 'ai art', 'new media art',
]

MIXED_KEYWORDS = [
    'open to all media', 'any medium', 'all mediums', 'all media',
    'mixed media', 'multimedia', 'multi-media', 'interdisciplinary',
    'cross-disciplinary',
]


def build_text(entry: dict) -> str:
    """Combine relevant text fields into a single lowercased string for matching."""
    parts = []
    for field in ('title', 'name', 'one_sentence', 'category', 'opportunity_type',
                  'why_it_fits', 'why_this_fits_short', 'category_label',
                  'organization'):
        val = entry.get(field)
        if val and isinstance(val, str):
            parts.append(val)
    # watercolor_fit_hits is a very reliable existing signal
    for hit in entry.get('watercolor_fit_hits', []):
        if isinstance(hit, str):
            parts.append(hit)
    # three_bullets often mention the medium explicitly
    for bullet in entry.get('three_bullets', []):
        if isinstance(bullet, str):
            parts.append(bullet)
    return ' '.join(parts).lower()


def keyword_hits(text: str, keywords: list) -> list:
    """Return list of matched keywords found in text."""
    return [kw for kw in keywords if kw.lower() in text]


def classify(entry: dict) -> tuple:
    """
    Return (medium_label, hits_dict) for an entry.
    hits_dict maps medium names to matched keyword lists.
    """
    text = build_text(entry)

    hits = {}

    wc_hits = keyword_hits(text, WATERCOLOR_KEYWORDS)
    if wc_hits:
        hits['watercolor'] = wc_hits

    paint_hits = keyword_hits(text, PAINTING_KEYWORDS)
    if paint_hits:
        hits['painting'] = paint_hits

    illus_hits = keyword_hits(text, ILLUSTRATION_KEYWORDS)
    if illus_hits:
        hits['illustration'] = illus_hits

    book_hits = keyword_hits(text, BOOK_ARTS_KEYWORDS)
    if book_hits:
        hits['book_arts'] = book_hits

    print_hits = keyword_hits(text, PRINTMAKING_KEYWORDS)
    if print_hits:
        hits['printmaking'] = print_hits

    photo_hits = keyword_hits(text, PHOTOGRAPHY_KEYWORDS)
    if photo_hits:
        hits['photography'] = photo_hits

    digital_hits = keyword_hits(text, DIGITAL_KEYWORDS)
    if digital_hits:
        hits['digital'] = digital_hits

    mixed_hits = keyword_hits(text, MIXED_KEYWORDS)
    if mixed_hits:
        hits['mixed'] = mixed_hits

    # Category field as a strong structural hint (supplement, not override)
    cat = (entry.get('category') or '').lower()
    if any(kw in cat for kw in ('book', 'zine', 'publishing', 'press')):
        hits.setdefault('book_arts', []).append(f'category:{cat}')
    if 'photo' in cat:
        hits.setdefault('photography', []).append(f'category:{cat}')
    if 'print' in cat and 'printmaking' not in cat:
        hits.setdefault('printmaking', []).append(f'category:{cat}')
    if 'illus' in cat:
        hits.setdefault('illustration', []).append(f'category:{cat}')

    # Apply priority order
    priority = ['watercolor', 'painting', 'illustration', 'book_arts',
                'printmaking', 'photography', 'digital', 'mixed']
    for medium in priority:
        if medium in hits:
            return medium, hits

    return 'unknown', hits


PRIORITY_RANK = {
    'watercolor': 0, 'painting': 1, 'illustration': 2,
    'book_arts': 3, 'printmaking': 4, 'photography': 5,
    'digital': 6, 'mixed': 7, 'unknown': 8,
}


def should_update(existing: str, new_medium: str) -> bool:
    """
    Decide whether to replace the existing classification.

    Rules:
    - Never downgrade to 'unknown'.
    - Never overwrite 'watercolor'.
    - Never overwrite 'photography' with a weaker classification.
    - Always update from 'unknown'.
    - Update 'mixed' to any specific medium.
    - Otherwise only upgrade along the priority order.
    """
    if existing == new_medium:
        return False
    if new_medium == 'unknown':
        return False  # never downgrade to unknown
    if existing == 'watercolor':
        return False  # protected
    if existing == 'unknown':
        return True   # always improve from unknown
    if existing == 'mixed' and new_medium != 'unknown':
        return True   # specific > mixed
    return PRIORITY_RANK.get(new_medium, 99) < PRIORITY_RANK.get(existing, 99)


def adjust_score(entry: dict, new_medium: str) -> float:
    """
    Return the adjusted watercolor_adjusted_score.
    Only modifies score when the medium was previously 'unknown'.
    """
    current_score = float(entry.get('watercolor_adjusted_score') or
                          entry.get('overall_score') or 5.0)
    original_medium = entry.get('native_medium', 'unknown')

    if original_medium != 'unknown':
        return current_score  # don't re-adjust already-classified entries

    if new_medium == 'watercolor':
        return min(current_score * 1.2, 10.0)
    elif new_medium in ('photography', 'digital'):
        return current_score * 0.6
    return current_score


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    root = Path(__file__).resolve().parents[2]  # repo root
    target = root / 'deploy_data' / 'compact_opportunities.json'

    print(f'Loading {target}')
    with open(target, encoding='utf-8') as f:
        data = json.load(f)

    total = len(data)
    print(f'Total entries: {total}')

    # Baseline counts
    baseline = Counter(e.get('native_medium', 'missing') for e in data)
    print('\nBaseline distribution:')
    for k, v in sorted(baseline.items(), key=lambda x: -x[1]):
        print(f'  {k}: {v}')

    # Reclassify
    changed_count = 0
    changes_by_medium: Counter = Counter()
    previous_medium_of_changed: Counter = Counter()
    watercolor_samples = []

    for entry in data:
        existing = entry.get('native_medium', 'unknown')
        new_medium, hits = classify(entry)

        if should_update(existing, new_medium):
            old_medium = existing
            entry['native_medium'] = new_medium
            entry['native_medium_hits'] = hits

            # Adjust score
            new_score = adjust_score(entry, new_medium)
            old_score = float(entry.get('watercolor_adjusted_score') or 0)
            if abs(new_score - old_score) > 0.001:
                entry['watercolor_adjusted_score'] = round(new_score, 2)

            changed_count += 1
            changes_by_medium[new_medium] += 1
            previous_medium_of_changed[old_medium] += 1

            if new_medium == 'watercolor':
                watercolor_samples.append({
                    'title': entry.get('title') or entry.get('name', ''),
                    'hits': hits.get('watercolor', []),
                    'score': entry.get('watercolor_adjusted_score'),
                    'was': old_medium,
                })

    # Write back
    with open(target, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Final counts
    final = Counter(e.get('native_medium', 'missing') for e in data)

    print(f'\n{"="*50}')
    print(f'CHANGES MADE: {changed_count} / {total}')
    print(f'{"="*50}')

    print('\nChanged FROM (what was replaced):')
    for k, v in sorted(previous_medium_of_changed.items(), key=lambda x: -x[1]):
        print(f'  {k}: {v}')

    print('\nChanged TO (new classifications):')
    for k, v in sorted(changes_by_medium.items(), key=lambda x: -x[1]):
        print(f'  {k}: {v}')

    print('\nFinal distribution:')
    for k, v in sorted(final.items(), key=lambda x: -x[1]):
        delta = v - baseline.get(k, 0)
        arrow = f'(+{delta})' if delta > 0 else (f'({delta})' if delta < 0 else '')
        print(f'  {k}: {v} {arrow}')

    print(f'\nWatercolor entries: {final.get("watercolor", 0)}')
    if watercolor_samples:
        print(f'\nSample watercolor-tagged entries (up to 20 of {len(watercolor_samples)}):')
        for s in watercolor_samples[:20]:
            print(f"  [{s['was']} -> watercolor] {s['title']}")
            print(f"    matched: {s['hits']}")
            print(f"    score: {s['score']}")
    else:
        wc_entries = [e for e in data if e.get('native_medium') == 'watercolor']
        if wc_entries:
            print('\nNote: no new watercolor entries were added (all watercolor entries pre-existed or no new ones found).')
            print('Existing watercolor entries:')
            for e in wc_entries[:10]:
                print(f"  {e.get('title') or e.get('name','')}")

    print(f'\nWrote updated data to {target}')


if __name__ == '__main__':
    main()
