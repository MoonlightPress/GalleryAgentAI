from anthropic import Anthropic
from dotenv import load_dotenv
import os
import base64
import mimetypes

load_dotenv(dotenv_path=".env")

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MODEL = "claude-sonnet-4-5"
IMAGE_FOLDER = "artist_images"


def image_to_content_block(path):
    mime_type, _ = mimetypes.guess_type(path)

    if mime_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise ValueError(f"Unsupported image type: {path}")

    with open(path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": mime_type,
            "data": image_data,
        },
    }


image_blocks = []

for filename in os.listdir(IMAGE_FOLDER):
    if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        path = os.path.join(IMAGE_FOLDER, filename)
        image_blocks.append(image_to_content_block(path))

if not image_blocks:
    raise Exception("No images found in artist_images folder.")


prompt = """
You are an art critic, curator, and market analyst.

Analyze these artworks as a coherent body of work.

Your job:
1. Identify major visual themes.
2. Identify emotional tone.
3. Identify recurring subjects and motifs.
4. Identify color palette tendencies.
5. Identify compositional habits.
6. Identify likely contemporary art categories.
7. Identify possible collector appeal.
8. Identify comparable artists or movements.
9. Identify useful gallery-search keywords.
10. Identify strengths and weaknesses in the current art market.
11. Write a concise artist dossier that can be reused by gallery research agents.

Be precise.
Do not flatter.
Do not invent biographical facts.
If something is uncertain, say so.
"""

message_content = image_blocks + [
    {
        "type": "text",
        "text": prompt,
    }
]

response = client.messages.create(
    model=MODEL,
    max_tokens=3000,
    messages=[
        {
            "role": "user",
            "content": message_content,
        }
    ],
)

analysis = response.content[0].text

print(analysis)

with open("artist_dossier.md", "w", encoding="utf-8") as f:
    f.write(analysis)

print("\nSaved analysis to artist_dossier.md")