"""Regenerate frontend/src/utils/heroPoemTone.js.

Run after adding or replacing Mochi hero art:

    python scripts/gen_hero_poem_tone.py

The hero poem is white-on-image, and whether it reads depends entirely on what
happens to be behind it. That used to be decided by the clock — night heroes got
cream, day heroes got ink — which held only because the first night illustration
had a dim brown wall behind the verse. Twelve of the fifteen night paintings
added 2026-09-04 are pale in that same corner, so the cream verse disappeared.

So measure it instead: sample the exact rectangle the poem occupies (left 9%,
width 30%, top 12%, height 64% — see HeroSection.css) and pick the tone from its
mean luminance.
"""

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageStat

ROOT = Path(__file__).resolve().parent.parent
HERO_DIR = ROOT / "frontend" / "src" / "assets" / "heroes" / "mochi"
OUT = ROOT / "frontend" / "src" / "utils" / "heroPoemTone.js"

# Above this the patch is pale enough for dark ink; below it, cream reads better.
LUMINANCE_SPLIT = 150


def poem_region_luminance(path: Path) -> float:
    im = Image.open(path).convert("L")
    w, h = im.size
    box = (int(0.09 * w), int(0.12 * h), int(0.39 * w), int(0.76 * h))
    return ImageStat.Stat(im.crop(box)).mean[0]


def focal_y(path: Path) -> int:
    """Where the subject actually sits vertically, as a percent.

    The hero box is far squarer than a 3:1 painting, so object-fit: cover throws
    away the top and bottom. Mobile had this pinned at 28% — tuned for the first
    illustration, where the cat sits mid-frame on a desk. The paintings added
    2026-09-04 put their subjects low, so a 28% focal point cropped them off at
    the feet. Edge detail marks where the subject is (empty wash and sky have
    none), sampled on the right where these compositions place it.
    """
    im = Image.open(path).convert("L")
    w, h = im.size
    right = im.crop((int(0.45 * w), 0, w, h)).filter(ImageFilter.FIND_EDGES)
    rows = np.asarray(right, dtype=float).sum(axis=1)
    centroid = float((rows * np.arange(h)).sum() / max(rows.sum(), 1)) / h
    return int(round(max(0.35, min(0.75, centroid)) * 100))


def main() -> None:
    tone, focal = {}, {}
    for f in sorted(HERO_DIR.glob("*.webp")):
        lum = poem_region_luminance(f)
        tone[f.name] = "ink" if lum > LUMINANCE_SPLIT else "cream"
        focal[f.name] = focal_y(f)
        print(f"  {lum:6.1f}  {tone[f.name]:5}  focal {focal[f.name]:3}%  {f.name}")

    header = (
        "// GENERATED - do not hand-edit. Regenerate with scripts/gen_hero_poem_tone.py\n"
        "//\n"
        "// Which colour the hero poem needs, measured per image rather than assumed\n"
        "// from the clock. The poem sits at left 9%/width 30%, top 12%/height 64%\n"
        "// (see HeroSection.css); that exact rectangle is sampled for mean luminance.\n"
    )
    fn = (
        "\n\nfunction stemOf(url) {\n"
        "  const file = String(url || '').split('/').pop()?.split('?')[0] || ''\n"
        "  // Vite fingerprints filenames (mochi_day_03-B7XEVwCF.webp); match the stem.\n"
        "  return { file, stem: file.replace(/-[A-Za-z0-9_]{8,}\\.webp$/, '.webp') }\n"
        "}\n\n"
        "export function poemToneFor(url) {\n"
        "  const { file, stem } = stemOf(url)\n"
        "  return HERO_POEM_TONE[stem] || HERO_POEM_TONE[file] || 'ink'\n"
        "}\n\n"
        "// object-position Y for the hero crop, so a subject low in the frame is not\n"
        "// cut off at the feet by a box far squarer than the painting.\n"
        "export function focalYFor(url) {\n"
        "  const { file, stem } = stemOf(url)\n"
        "  return HERO_FOCAL_Y[stem] ?? HERO_FOCAL_Y[file] ?? 50\n"
        "}\n"
    )
    OUT.write_text(
        header
        + "export const HERO_POEM_TONE = " + json.dumps(tone, indent=2) + "\n\n"
        + "export const HERO_FOCAL_Y = " + json.dumps(focal, indent=2) + fn,
        encoding="utf-8",
    )
    ink = sum(1 for v in tone.values() if v == "ink")
    print(f"\nwrote {OUT.relative_to(ROOT)} - {ink} ink, {len(tone) - ink} cream")


if __name__ == "__main__":
    main()
