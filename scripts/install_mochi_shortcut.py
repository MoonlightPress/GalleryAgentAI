"""
install_mochi_shortcut.py

Creates a Windows Start Menu shortcut for launching the Mochi Streamlit
dashboard with a custom icon. Run once to install.

Steps:
  1. Generate static/mochi_icon.ico (or use mochi_hero.png if present)
  2. Write launch_mochi.bat
  3. Create Start Menu shortcut via PowerShell WScript.Shell
"""
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
STATIC_DIR = ROOT / "static"
ICON_PATH = ROOT / "static" / "mochi_icon.ico"
HERO_PATH = ROOT / "static" / "assets" / "headers" / "mochi_hero.png"
BAT_PATH = ROOT / "launch_mochi.bat"
PROJECT_DIR = str(ROOT.resolve())
START_MENU_PATH = os.path.expandvars(
    r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Mochi Atelier.lnk"
)


# ── 1. Icon generation ─────────────────────────────────────────────────────────

def generate_icon() -> bool:
    """Generate mochi_icon.ico. Returns True on success."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("[icon] Pillow not installed — skipping icon generation.")
        print("       Run: pip install Pillow")
        print("       Shortcut will use default icon.")
        return False

    STATIC_DIR.mkdir(parents=True, exist_ok=True)

    # If mochi_hero.png exists, crop to square and use it
    if HERO_PATH.exists():
        print(f"[icon] Using existing mochi_hero.png from {HERO_PATH}")
        img = Image.open(HERO_PATH).convert("RGBA")
        # Crop to centered square
        w, h = img.size
        side = min(w, h)
        left = (w - side) // 2
        top = (h - side) // 2
        img = img.crop((left, top, left + side, top + side))
        img = img.resize((256, 256), Image.LANCZOS)
        # Convert to RGBA background for ICO
        background = Image.new("RGBA", (256, 256), (247, 239, 226, 255))
        background.paste(img, (0, 0), img)
        img = background
    else:
        print("[icon] mochi_hero.png not found — drawing fallback icon")
        img = Image.new("RGBA", (256, 256), (247, 239, 226, 255))
        draw = ImageDraw.Draw(img)

        # Warm amber filled circle (body)
        amber = (200, 149, 108, 255)
        draw.ellipse([28, 48, 228, 228], fill=amber)

        # Cat ears: two filled triangles at top of circle
        ear_color = (180, 125, 85, 255)
        # Left ear
        draw.polygon([(60, 80), (40, 30), (100, 60)], fill=ear_color)
        # Right ear
        draw.polygon([(196, 80), (216, 30), (156, 60)], fill=ear_color)

        # "M" monogram in cream
        cream = (247, 239, 226, 255)
        # Draw a bold M using rectangles (font-independent fallback)
        try:
            font = ImageFont.truetype("georgia.ttf", 96)
        except Exception:
            try:
                font = ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", 96)
            except Exception:
                font = ImageFont.load_default()

        # Center the M
        bbox = draw.textbbox((0, 0), "M", font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        x = (256 - text_w) // 2
        y = (256 - text_h) // 2 + 10
        draw.text((x, y), "M", fill=cream, font=font)

    # Save as ICO with multiple sizes
    sizes = [(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]
    icons = []
    for size in sizes:
        resized = img.resize(size, Image.LANCZOS).convert("RGBA")
        icons.append(resized)

    icons[0].save(
        str(ICON_PATH),
        format="ICO",
        sizes=[s for s in [(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)]],
        append_images=icons[1:],
    )
    print(f"[icon] Saved {ICON_PATH}")
    return True


# ── 2. Launcher batch file ─────────────────────────────────────────────────────

def write_bat():
    bat_content = (
        "@echo off\r\n"
        f'start "" cmd /c "cd /d {PROJECT_DIR} && python -m streamlit run app.py"\r\n'
    )
    BAT_PATH.write_text(bat_content, encoding="utf-8")
    print(f"[bat] Written {BAT_PATH}")


# ── 3. Start Menu shortcut ─────────────────────────────────────────────────────

def create_shortcut(icon_available: bool):
    target = str(BAT_PATH.resolve())
    working_dir = PROJECT_DIR
    shortcut_path = START_MENU_PATH
    description = "Mochi's Atelier — Nin's career assistant"

    icon_line = ""
    if icon_available and ICON_PATH.exists():
        icon_line = f'$shortcut.IconLocation = "{ICON_PATH.resolve()}"'

    ps_script = f"""
$wsh = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut("{shortcut_path}")
$shortcut.TargetPath = "{target}"
$shortcut.WorkingDirectory = "{working_dir}"
$shortcut.Description = "{description}"
{icon_line}
$shortcut.Save()
Write-Output "Shortcut created at: {shortcut_path}"
"""

    result = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_script],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print(f"[shortcut] {result.stdout.strip()}")
    else:
        print(f"[shortcut error] {result.stderr.strip()}")
        print(f"  (stdout: {result.stdout.strip()})")


# ── main ───────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Mochi Atelier — Windows Start Menu Installer")
    print("=" * 60)

    icon_ok = generate_icon()
    write_bat()
    create_shortcut(icon_available=icon_ok)

    print()
    print("=" * 60)
    print("Mochi Atelier has been added to your Start Menu.")
    print("Search for 'Mochi' to find it, then right-click")
    print("-> Pin to taskbar.")
    print("=" * 60)


if __name__ == "__main__":
    main()
