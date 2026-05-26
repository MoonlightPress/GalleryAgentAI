from anthropic import Anthropic
from dotenv import load_dotenv
import os
import json

load_dotenv(dotenv_path=".env")

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

MODEL = "claude-sonnet-4-5"


def load_json_file(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


artist_preferences = load_json_file(
    "memory/artist_preferences.json",
    {}
)


with open("artist_dossier.md", "r", encoding="utf-8") as f:
    artist_dossier = f.read()


prompt = f"""
You are an expert contemporary art curator.

Your task:
Identify the kinds of artists this artist should collaborate with.

You are NOT identifying identical artists.

You ARE identifying:
- complementary artists
- emotionally compatible artists
- artists suitable for group shows
- artists likely to share audiences
- artists likely to create meaningful aesthetic dialogue

Artist dossier:
{artist_dossier}

Artist preferences:
{json.dumps(artist_preferences, indent=2, ensure_ascii=False)}

Output sections:

1. Ideal collaborator archetypes
2. Ideal group show themes
3. Artists likely to share collectors
4. Artists likely to share emotional tone
5. Artists likely to fit in the same exhibition
6. Cities/scenes where these artists are concentrated
7. What kinds of artists should be avoided
8. Keywords useful for discovering collaborators
9. What makes this artist socially/aesthetically distinct

Be precise.
Avoid generic art-world language.
"""


response = client.messages.create(
    model=MODEL,
    max_tokens=3000,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

output = response.content[0].text

print(output)

with open("collaboration_report.md", "w", encoding="utf-8") as f:
    f.write(output)

print("\nSaved collaboration report.")