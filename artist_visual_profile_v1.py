
import json
from pathlib import Path

PROFILE = {
  "visual_profile_version": 2,
  "artist_name": "GEGYjiji",
  "artist_handle": "GEGYjiji",
  "age": 26,
  "nationality": "Chinese",
  "hometown": "Changsha, China",
  "current_city": "Tokyo, Japan",
  "japanese_proficiency": "JLPT N2",
  "primary_language": "Chinese (Simplified)",
  "working_language": "Japanese",
  "medium": "watercolor (primary), occasional ink",
  "summary": "GEGYjiji is a 26-year-old Chinese watercolor artist based in Tokyo. Originally from Changsha, she paints urban atmosphere, domestic stillness, cats, interior light, and the quiet accumulation of memory. Her work is intimate in scale and emotionally precise. She has N2 Japanese and 90k Twitter followers, and is actively seeking gallery exhibition opportunities and publishing collaborations. She needs a mix of prestigious international opportunities and intimate local Tokyo venues.",
  "dominant_subjects": [
    "urban atmosphere and streetscapes",
    "domestic interiors and interior light",
    "cats in lived-in spaces",
    "city corners and quiet architecture",
    "ordinary Tokyo neighborhoods",
    "windows, light through curtains, shadow play",
    "human presence through absence",
    "memory-soaked domestic objects"
  ],
  "recurring_motifs": [
    "cats as anchors of stillness",
    "interior light falling across surfaces",
    "the threshold between inside and outside",
    "quiet architectural detail",
    "layered atmosphere through watercolor transparency",
    "the texture of daily life in Tokyo",
    "cross-cultural seeing — Chinese sensibility applied to Japanese space"
  ],
  "composition_patterns": [
    "intimate scale — personal rather than monumental",
    "atmospheric layering through watercolor transparency",
    "soft-edged observation, not hard-line illustration",
    "color as emotional register, not literal description",
    "stillness as compositional value",
    "sequence and accumulation of small moments"
  ],
  "color_palette": [
    "warm greys and soft neutrals",
    "pale washes of blue and sage",
    "amber and ochre interior warmth",
    "deep ink shadows in thin washes",
    "muted rose and dusty lavender",
    "the specific grey-green of Tokyo rainy days"
  ],
  "emotional_tone": [
    "still",
    "intimate",
    "nostalgic without sentimentality",
    "attentive",
    "quietly melancholic",
    "warm but never saccharine",
    "precise emotional observation"
  ],
  "pace": "slow and deliberate",
  "scale": "intimate — small to medium works",
  "best_formats": [
    "gallery group exhibitions with atmospheric or quiet-life themes",
    "solo exhibitions in intimate Tokyo venues",
    "art book and zine publication",
    "artist-run space exhibitions",
    "residency programs (international, prestigious)",
    "small press and independent publishing",
    "open calls — watercolor or works on paper",
    "bookshop gallery exhibitions in Tokyo"
  ],
  "bad_fit_contexts": [
    "photography-dominated calls",
    "commercial illustration markets",
    "anime or manga or character art events",
    "high-volume craft fairs and markets",
    "tech or AI or NFT art contexts",
    "brand activation partnerships",
    "spectacle-driven or large-scale installation contexts"
  ],
  "artist_statement_phrases": [
    "stillness as subject",
    "the atmosphere of ordinary places",
    "interior light and the texture of daily life",
    "memory held in domestic space",
    "the city seen through quiet attention",
    "watercolor as a medium of slow observation",
    "cross-cultural seeing — Chinese artist in Tokyo"
  ],
  "curatorial_keywords": [
    "watercolor",
    "urban atmosphere",
    "domestic interior",
    "stillness",
    "cats",
    "interior light",
    "memory",
    "quiet life",
    "contemporary watercolor",
    "East Asian urban painting",
    "intimate scale",
    "artist book",
    "small press",
    "Tokyo-based",
    "Chinese artist",
    "atmospheric painting"
  ],
  "portfolio_bodies_to_create": [
    {
      "id": "tokyo_still_life",
      "title": "Tokyo Still Life",
      "description": "Interiors, cats, light through windows — the quiet architecture of daily life in a Tokyo apartment and neighborhood."
    },
    {
      "id": "urban_atmosphere",
      "title": "Urban Atmosphere",
      "description": "Streetscapes, corners, rain-wet pavement, the particular grey-green light of Tokyo. Place as emotional subject."
    },
    {
      "id": "memory_and_distance",
      "title": "Memory and Distance",
      "description": "Work that holds both China (Changsha, origin) and Japan (Tokyo, present) — the feeling of being between two cities, two languages, two versions of ordinary life."
    }
  ],
  "opportunity_weighting": {
    "gallery_exhibition_international": 1.4,
    "gallery_exhibition_tokyo": 1.3,
    "residency_prestigious": 1.4,
    "residency_japan": 1.2,
    "artist_book": 1.5,
    "zine": 1.3,
    "small_press": 1.3,
    "bookshop_gallery_tokyo": 1.3,
    "open_call_watercolor": 1.5,
    "open_call_general": 1.0,
    "artist_run_space": 1.1,
    "cafe_wall": 0.5,
    "craft_market": -0.8,
    "photography_call": -0.5,
    "commercial_illustration": -1.0,
    "character_art": -1.5,
    "tech_art": -2.0,
    "nft": -2.0
  }
}

OUT_PATHS = [
    "artist_visual_profile_template.json",
    "memory/artist_visual_profile.json",
    "Memory/artist_visual_profile.json",
]

def write_json(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

def main():
    for path in OUT_PATHS:
        write_json(path, PROFILE)

    print("Wrote visual profile:")
    for path in OUT_PATHS:
        print("-", path)

if __name__ == "__main__":
    main()
