
import json
import os
from pathlib import Path
from statistics import mean

from PIL import Image, ImageStat

IMAGE_ROOT = Path("artist_images")
OUT_DIR = Path("memory/artist_image_analysis")
THUMB_DIR = OUT_DIR / "thumbnails"
CATALOG_PATH = OUT_DIR / "image_catalog.json"
SUMMARY_PATH = OUT_DIR / "image_summary.json"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}


def safe_open(path):
    try:
        img = Image.open(path)
        img.thumbnail((1200, 1200))
        return img.convert("RGB")
    except Exception:
        return None


def brightness(rgb):
    r, g, b = rgb
    return (0.2126 * r) + (0.7152 * g) + (0.0722 * b)


def temperature(rgb):
    r, g, b = rgb
    if b == 0:
        b = 1
    return round(r / b, 3)


def analyze_image(path):
    img = safe_open(path)

    if img is None:
        return None

    stat = ImageStat.Stat(img)
    avg = tuple(round(x, 2) for x in stat.mean[:3])

    w, h = img.size

    b = brightness(avg)
    temp = temperature(avg)

    if b < 70:
        light_key = "dark"
    elif b < 140:
        light_key = "muted"
    else:
        light_key = "bright"

    if temp > 1.12:
        temp_key = "warm"
    elif temp < 0.9:
        temp_key = "cool"
    else:
        temp_key = "neutral"

    aspect = "square"
    if w > h * 1.2:
        aspect = "landscape"
    elif h > w * 1.2:
        aspect = "portrait"

    thumb_path = THUMB_DIR / path.name
    THUMB_DIR.mkdir(parents=True, exist_ok=True)

    thumb = img.copy()
    thumb.thumbnail((360, 360))
    thumb.save(thumb_path)

    return {
        "filename": path.name,
        "path": str(path),
        "folder": path.parent.name,
        "width": w,
        "height": h,
        "aspect": aspect,
        "average_rgb": avg,
        "brightness": round(b, 2),
        "brightness_class": light_key,
        "temperature": temp,
        "temperature_class": temp_key,
        "thumbnail": str(thumb_path),
    }


def summarize(catalog):
    if not catalog:
        return {}

    folders = {}

    for item in catalog:
        folders.setdefault(item["folder"], 0)
        folders[item["folder"]] += 1

    brightness_values = [x["brightness"] for x in catalog]
    warm = len([x for x in catalog if x["temperature_class"] == "warm"])
    cool = len([x for x in catalog if x["temperature_class"] == "cool"])
    neutral = len([x for x in catalog if x["temperature_class"] == "neutral"])

    aspects = {}
    for item in catalog:
        aspects.setdefault(item["aspect"], 0)
        aspects[item["aspect"]] += 1

    brightness_classes = {}
    for item in catalog:
        brightness_classes.setdefault(item["brightness_class"], 0)
        brightness_classes[item["brightness_class"]] += 1

    return {
        "image_count": len(catalog),
        "folders": folders,
        "average_brightness": round(mean(brightness_values), 2),
        "temperature_distribution": {
            "warm": warm,
            "cool": cool,
            "neutral": neutral,
        },
        "aspect_distribution": aspects,
        "brightness_distribution": brightness_classes,
    }


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if not IMAGE_ROOT.exists():
        raise SystemExit("artist_images folder not found. Create artist_images/ and put images inside.")

    catalog = []

    for path in IMAGE_ROOT.rglob("*"):
        if path.suffix.lower() not in IMAGE_EXTS:
            continue

        item = analyze_image(path)

        if item:
            catalog.append(item)

    summary = summarize(catalog)

    CATALOG_PATH.write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    SUMMARY_PATH.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    print(f"Analyzed {len(catalog)} images.")
    print(f"Wrote {CATALOG_PATH}")
    print(f"Wrote {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
