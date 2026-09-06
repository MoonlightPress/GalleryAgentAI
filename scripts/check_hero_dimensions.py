# -*- coding: utf-8 -*-
"""Fail if any companion hero is too small for a desktop viewport.

Why this exists: on 2026-09-06 Scott reported the heroes reading "too zoomed in
on PC, great on the phone". The cause was not CSS. The art was being generated
at 1280x427 while the hero band is full-bleed, so on a 1920px monitor every
image was upscaled ~1.5x — which looks exactly like a tighter crop. 96 of 98
files were affected across all three companions, and nobody noticed for weeks
because nothing ever checked.

So: check. Run it after generating hero art, before committing it.

    python scripts/check_hero_dimensions.py

Exits non-zero and names the offenders if any hero is under MIN_WIDTH, or if a
pool would come up empty because the day/night filenames are wrong.
"""
import glob
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HEROES = os.path.join(ROOT, 'frontend', 'src', 'assets', 'heroes')

# The hero is full-bleed, so the binding constraint is the widest common
# desktop viewport rather than anything about the layout. 1920 is the intended
# size for the whole set; anything under it is being upscaled somewhere.
MIN_WIDTH = 1920
COMPANIONS = ('mochi', 'peppercorn', 'saffron')

# heroImages.js splits each companion's pool on the "_night" token in the path.
# A file that lands in the wrong pool is as broken as one that is too small,
# and just as invisible, so it is checked here too.
NIGHT_TOKEN = '_night'


def dimensions(path):
    """Width/height for PNG and the three WebP chunk layouts, header only."""
    with open(path, 'rb') as fh:
        d = fh.read(64)
    if d[:8] == b'\x89PNG\r\n\x1a\n':
        return struct.unpack('>II', d[16:24])
    if d[:4] == b'RIFF' and d[8:12] == b'WEBP':
        chunk = d[12:16]
        if chunk == b'VP8X':
            return (int.from_bytes(d[24:27], 'little') + 1,
                    int.from_bytes(d[27:30], 'little') + 1)
        if chunk == b'VP8L':
            bits = int.from_bytes(d[21:25], 'little')
            return ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
        if chunk == b'VP8 ':
            return (struct.unpack('<H', d[26:28])[0] & 0x3FFF,
                    struct.unpack('<H', d[28:30])[0] & 0x3FFF)
    return None


def main():
    problems = []
    for who in COMPANIONS:
        files = sorted(glob.glob(os.path.join(HEROES, who, '*')))
        day = [f for f in files if NIGHT_TOKEN not in os.path.basename(f)]
        night = [f for f in files if NIGHT_TOKEN in os.path.basename(f)]
        small = []
        for path in files:
            dim = dimensions(path)
            if dim is None:
                problems.append(f'{who}: unreadable image header — {os.path.basename(path)}')
            elif dim[0] < MIN_WIDTH:
                small.append((os.path.basename(path), dim))
        print(f'{who:11} {len(files):3} files  ({len(day)} day / {len(night)} night)  '
              f'{len(small)} under {MIN_WIDTH}px')
        for name, dim in small:
            problems.append(f'{who}: {name} is {dim[0]}x{dim[1]}, under {MIN_WIDTH}px wide')
        # An empty pool means the page falls back to a blank hero at that time
        # of day — silent, and only visible after dark.
        if not day:
            problems.append(f'{who}: no DAY heroes (every filename carries "{NIGHT_TOKEN}")')
        if not night:
            problems.append(f'{who}: no NIGHT heroes (no filename carries "{NIGHT_TOKEN}")')

    if problems:
        print(f'\nFAIL — {len(problems)} problem(s):')
        for p in problems:
            print('  ' + p)
        print('\nRegenerate the offenders at 1920x640 or wider. Upscaled hero art '
              'reads as a tighter crop on desktop and is fine on a phone, which is '
              'why it goes unnoticed.')
        return 1

    print('\nOK — every hero is at least '
          f'{MIN_WIDTH}px wide and both pools are populated.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
