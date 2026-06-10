from anthropic import Anthropic
from dotenv import load_dotenv
import os
import json

load_dotenv(dotenv_path=".env")

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = "claude-sonnet-4-5"


def load_text(path, fallback=""):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_json(path, fallback):
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


artist_dossier = load_text("artist_dossier.md")
artist_graph = load_json("memory/artist_graph.json", {})
artist_preferences = load_json("memory/artist_preferences.json", {})


query = input("Ask the artist graph a question: ")

prompt = f"""
You are Agent I: Artist Graph Query Agent.

Answer the user's question using the artist graph.

User question:
{query}

Artist dossier:
{artist_dossier}

Artist preferences:
{json.dumps(artist_preferences, indent=2, ensure_ascii=False)}

Artist graph:
{json.dumps(artist_graph, indent=2, ensure_ascii=False)}

Rules:
- Use the graph data directly.
- Do not invent certainty.
- If something needs verification, say so.
- Prefer practical recommendations.
- If the user asks for collaborators, rank them.
- If the user asks for a group show, propose a coherent lineup and concept.
- If the user asks for a city, explain why that city matters.
- Be concise but useful.
"""

response = client.messages.create(
    model=MODEL,
    max_tokens=2500,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

answer = response.content[0].text

print("\n" + answer)

with open("graph_query_response.md", "w", encoding="utf-8") as f:
    f.write(answer)

print("\nSaved graph_query_response.md")