
from pathlib import Path

path = Path("strategy_homepage_components.py")

if not path.exists():
    raise SystemExit("strategy_homepage_components.py not found.")

text = path.read_text(encoding="utf-8")

if '"global_targets":' not in text:
    text = text.replace(
        '"community_builders": ("Community Builders", "Useful for local connection, peers, low-pressure visibility, and creative confidence.", "⌂"),',
        '"community_builders": ("Community Builders", "Useful for local connection, peers, low-pressure visibility, and creative confidence.", "⌂"),\n    "global_targets": ("Global Targets", "International opportunities that expand her reach beyond local Tokyo/Japan options.", "◎"),\n    "publication_targets": ("Publication Targets", "Photobook, zine, artist-book, and magazine opportunities that build visible career evidence.", "▣"),'
    )

text = text.replace(
    'for key in ["featured", "easy_wins", "career_changing", "portfolio_builders", "community_builders"]:',
    'for key in ["featured", "easy_wins", "global_targets", "publication_targets", "career_changing", "portfolio_builders", "community_builders"]:'
)

path.write_text(text, encoding="utf-8")

print("Patched strategy homepage with global sections.")
