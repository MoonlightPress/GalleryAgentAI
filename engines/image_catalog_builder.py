
import json
from pathlib import Path

IMAGE_EXTS = {".jpg",".jpeg",".png",".webp",".tif",".tiff"}
OUT_PATH = "memory/image_catalog.json"

def main():
    root = Path("artist_images")

    images = []

    if root.exists():
        for p in root.rglob("*"):
            if p.suffix.lower() in IMAGE_EXTS:
                images.append({
                    "filename": p.name,
                    "path": str(p),
                    "folder": str(p.parent.name),
                })

    Path("memory").mkdir(exist_ok=True)

    with open(OUT_PATH,"w",encoding="utf-8") as f:
        json.dump(images,f,indent=2,ensure_ascii=False)

    print(f"Cataloged {len(images)} images.")

if __name__ == "__main__":
    main()
