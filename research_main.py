from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime
import os
import json


# =========================
# LOAD ENVIRONMENT
# =========================

load_dotenv(dotenv_path=".env")

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

MODEL = "claude-sonnet-4-5"


# =========================
# LOAD MEMORY
# =========================

def load_json_file(path, fallback):
    if not os.path.exists(path):
        return fallback

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


verified_galleries = load_json_file(
    "memory/verified_galleries.json",
    []

artist_preferences = load_json_file(
    "memory/artist_preferences.json",
    {}

)


# =========================
# LOAD ARTIST DOSSIER
# =========================

with open("artist_dossier.md", "r", encoding="utf-8") as f:
    ARTIST_PROFILE = f.read()


# =========================
# CLAUDE HELPER
# =========================

def call_claude(prompt, max_tokens=2000):

    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.content[0].text


# =========================
# RESEARCH AGENT
# =========================

def run_agent(agent_name, agent_instructions):

    prompt = f"""
You are {agent_name}.

Your task:
{agent_instructions}

Artist profile:
{ARTIST_PROFILE}

Known verified gallery memory:
{json.dumps(verified_galleries, indent=2, ensure_ascii=False)}

Artist preferences:
{json.dumps(artist_preferences, indent=2, ensure_ascii=False)}

Rules:
- Do not invent facts.
- If uncertain, say "needs verification."
- Prefer concrete gallery names, locations, and reasons.
- Rank recommendations.
- Explain why each gallery fits.
- Mention what information should be verified manually.

You MUST use:
- the artist dossier
- the artist preferences
- favorite artists
- emotional keywords
- career goals
- desired collaborators
- cities of interest

Use these to:
- refine recommendations
- avoid mismatched galleries
- identify likely aesthetic ecosystems
- identify collaborators and group show compatibility
- identify opportunities aligned with the artist's actual emotional and artistic interests
"""

    return call_claude(prompt, max_tokens=2200)


# =========================
# AGENT PROMPTS
# =========================

agent_a_instructions = """
Act as a traditional gallery researcher.

Focus on:
- Tokyo galleries with serious contemporary painting programs
- galleries that show painters, not just installation/conceptual work
- galleries with credibility among collectors
- galleries where atmospheric urban painting would not seem out of place

Output:
1. Top 5 Tokyo galleries
2. Why each fits
3. Possible weakness/risk for each
4. What to verify manually
"""


agent_b_instructions = """
Act as an emerging-scene researcher.

Focus on:
- smaller galleries
- alternative spaces
- young artist programs
- spaces open to poetic, melancholic, urban, or narrative work
- places where an emerging or mid-career painter might realistically get attention

Output:
1. Top 5 emerging/alternative Tokyo spaces
2. Why each fits
3. How approachable each seems
4. What to verify manually
"""


agent_c_instructions = """
Act as a commercial strategy researcher.

Focus on:
- galleries or spaces likely to sell prints, paintings, or collectible works
- audience fit
- collector appeal
- price-positioning
- whether the artist's work could appeal to international buyers
- crossover between fine art, illustration, books, and design

Output:
1. Top 5 commercially promising opportunities
2. Why each fits the market
3. Likely buyer type
4. What to verify manually
"""


# =========================
# RUN AGENTS
# =========================

print("Running Agent A...")
report_a = run_agent(
    "Agent A: Traditional Gallery Researcher",
    agent_a_instructions
)

print("Running Agent B...")
report_b = run_agent(
    "Agent B: Emerging Scene Researcher",
    agent_b_instructions
)

print("Running Agent C...")
report_c = run_agent(
    "Agent C: Commercial Strategy Researcher",
    agent_c_instructions
)


# =========================
# COMBINE REPORTS
# =========================

combined_report = f"""
# Artist Gallery Intelligence Report

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

# Artist Profile

{ARTIST_PROFILE}

---

# Agent A Report: Traditional Gallery Researcher

{report_a}

---

# Agent B Report: Emerging Scene Researcher

{report_b}

---

# Agent C Report: Commercial Strategy Researcher

{report_c}
"""


with open("agent_reports.md", "w", encoding="utf-8") as f:
    f.write(combined_report)

print("\nSaved report to agent_reports.md")


# =========================
# SYNTHESIZER AGENT
# =========================

synthesizer_prompt = f"""
You are Agent D: Senior Art Strategy Synthesizer.

You have received reports from:
- Traditional Gallery Researcher
- Emerging Scene Researcher
- Commercial Strategy Researcher

Your task:
- Identify strongest opportunities
- Remove weak recommendations
- Rank realistic targets
- Identify commercial opportunities
- Identify institutional limitations
- Create a practical strategy

Reports:

{combined_report}
"""

print("Running Synthesizer Agent...")

synthesized_report = call_claude(
    synthesizer_prompt,
    max_tokens=2600
)


# =========================
# FINAL REPORT
# =========================

final_report = f"""
{combined_report}

---

# Agent D Report: Synthesized Strategic Report

{synthesized_report}
"""


with open("final_gallery_report.md", "w", encoding="utf-8") as f:
    f.write(final_report)

print("\nSaved final report to final_gallery_report.md")


# =========================
# ACTION PLANNER
# =========================

action_agent_prompt = f"""
You are Agent E: Verification and Action Planner.

Take the strategy report below and convert it into a practical action plan.

For each recommendation produce:
1. Name
2. Type
3. Priority (A/B/C)
4. Why it fits
5. What must be verified manually
6. Exact Google search query
7. What page to look for
8. Suggested next action
9. Confidence level
10. Risk level

Rules:
- Remove weak recommendations
- Be concise
- Be practical
- Output as markdown table

Report:

{final_report}
"""

print("Running Action Planner Agent...")

action_plan = call_claude(
    action_agent_prompt,
    max_tokens=3000
)


with open("action_plan.md", "w", encoding="utf-8") as f:
    f.write(action_plan)

print("\nSaved action plan to action_plan.md")


# =========================
# SAVE MEMORY ENTRY
# =========================

os.makedirs("memory", exist_ok=True)

memory_entry = {
    "date_created": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "artist_dossier_file": "artist_dossier.md",
    "final_report_file": "final_gallery_report.md",
    "action_plan_file": "action_plan.md",
    "status": "prototype_run"
}

with open("memory/latest_run.json", "w", encoding="utf-8") as f:
    json.dump(memory_entry, f, indent=2, ensure_ascii=False)

print("\nSaved memory entry to memory/latest_run.json")

print("\nDONE")