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

# Two different faults, and only one of them is fatal. The first pass of this
# script treated width as the whole story; measuring the hero band proved that
# wrong, so the rule is split:
#
#   ASPECT is the hard failure. `.hero` is 56vh tall and full-bleed, so the band
#   is ~3.17:1 on every common desktop (1920x1080, 1600x900, 2560x1440 all land
#   there; a 1440x900 laptop is 2.86:1). Art at 3:1 therefore loses ~5% off the
#   sides — invisible. Art at 4:1 loses ~29%, which is what "too zoomed in"
#   actually looks like. No amount of resolution fixes it; the picture has to be
#   redrawn or recomposed.
#
#   WIDTH is a warning. Art narrower than the band gets upscaled by the browser
#   and reads soft on a desktop monitor while looking perfectly fine on a phone,
#   where 1280 already exceeds the device pixels. Worth knowing, not worth
#   blocking a deploy over, and NOT worth "fixing" by upscaling the file — a
#   Lanczos pass to 1920 invents no detail, it only doubles the bytes.
TARGET_RATIO = 3.0
RATIO_TOLERANCE = 0.25      # 2.75-3.25 sits inside the band on every desktop
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
    problems = []      # fatal: wrong shape, or an empty pool
    warnings = []      # soft: correct shape, not enough pixels
    for who in COMPANIONS:
        files = sorted(glob.glob(os.path.join(HEROES, who, '*')))
        day = [f for f in files if NIGHT_TOKEN not in os.path.basename(f)]
        night = [f for f in files if NIGHT_TOKEN in os.path.basename(f)]
        wrong_shape, soft = [], []
        for path in files:
            dim = dimensions(path)
            name = os.path.basename(path)
            if dim is None:
                problems.append(f'{who}: unreadable image header — {name}')
                continue
            ratio = dim[0] / dim[1]
            if abs(ratio - TARGET_RATIO) > RATIO_TOLERANCE:
                wrong_shape.append((name, dim, ratio))
            elif dim[0] < MIN_WIDTH:
                soft.append((name, dim))
        print(f'{who:11} {len(files):3} files  ({len(day)} day / {len(night)} night)  '
              f'{len(wrong_shape)} wrong shape, {len(soft)} soft')
        for name, dim, ratio in wrong_shape:
            problems.append(
                f'{who}: {name} is {dim[0]}x{dim[1]} ({ratio:.2f}:1). The band is ~3.17:1, '
                f'so roughly {round((1 - (TARGET_RATIO / ratio)) * 100)}% is cropped off the '
                f'sides on a desktop. Recompose it — resolution will not help.')
        for name, dim in soft:
            warnings.append(f'{who}: {name} is {dim[0]}x{dim[1]} — right shape, upscaled '
                            f'to {MIN_WIDTH}px by the browser, so it reads soft on a monitor '
                            f'and fine on a phone.')
        # An empty pool means the page falls back to a blank hero at that time
        # of day — silent, and only visible after dark.
        if not day:
            problems.append(f'{who}: no DAY heroes (every filename carries "{NIGHT_TOKEN}")')
        if not night:
            problems.append(f'{who}: no NIGHT heroes (no filename carries "{NIGHT_TOKEN}")')

    if warnings:
        print(f'\n{len(warnings)} soft (not blocking — regenerate at {MIN_WIDTH} wide '
              f'when convenient; do NOT upscale the existing files):')
        for w in warnings[:6]:
            print('  ' + w)
        if len(warnings) > 6:
            print(f'  ... and {len(warnings) - 6} more')

    if problems:
        print(f'\nFAIL — {len(problems)} problem(s):')
        for p in problems:
            print('  ' + p)
        return 1

    print('\nOK — every hero is the right shape and both pools are populated.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
