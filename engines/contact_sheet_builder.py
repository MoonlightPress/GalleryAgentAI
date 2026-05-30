
import json
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

CATALOG_PATH = Path("memory/artist_image_analysis/image_catalog.json")
OUT_DIR = Path("reports/contact_sheets")


def load_json(path, fallback):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return fallback


def make_sheet(items, out_path, title):
    thumb_size = 220
    label_height = 42
    cols = 5
    rows = max(1, (len(items) + cols - 1) // cols)

    w = cols * thumb_size
    h = 70 + rows * (thumb_size + label_height)

    sheet = Image.new("RGB", (w, h), "#f7efe2")
    draw = ImageDraw.Draw(sheet)

    draw.text((18, 18), title, fill="#3f3027")

    for idx, item in enumerate(items):
        x = (idx % cols) * thumb_size
        y = 60 + (idx // cols) * (thumb_size + label_height)

        thumb_path = item.get("thumbnail")

        if thumb_path and os.path.exists(thumb_path):
            img = Image.open(thumb_path).convert("RGB")
            img.thumbnail((thumb_size - 16, thumb_size - 16))

            px = x + (thumb_size - img.width) // 2
            py = y + (thumb_size - img.height) // 2

            sheet.paste(img, (px, py))

        label = item.get("filename", "")[:28]
        draw.text((x + 8, y + thumb_size + 4), label, fill="#6f5d4c")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path)


def main():
    catalog = load_json(CATALOG_PATH, [])

    if not catalog:
        raise SystemExit("No image catalog found. Run python local_image_processor.py first.")

    by_folder = {}

    for item in catalog:
        by_folder.setdefault(item["folder"], [])
        by_folder[item["folder"]].append(item)

    make_sheet(catalog[:50], OUT_DIR / "all_top_50.jpg", "All Images — Top 50")

    for folder, items in by_folder.items():
        safe = folder.replace("/", "_").replace("\\", "_")
        make_sheet(items[:50], OUT_DIR / f"{safe}.jpg", folder)

    print(f"Wrote contact sheets to {OUT_DIR}")


if __name__ == "__main__":
    main()
