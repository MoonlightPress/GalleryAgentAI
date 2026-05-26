from anthropic import Anthropic
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv(dotenv_path=".env")

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MODEL = "claude-sonnet-4-5"


ARTIST_PROFILE = """
The artist primarily paints quiet city streets and urban environments.

Her work has a melancholic, atmospheric, emotionally reflective quality.
The imagery is not mainly figurative. The focus is often architecture, streets,
light, mood, solitude, memory, and poetic urban loneliness.

Useful descriptors:
- quiet urban scenes
- melancholic city streets
- atmospheric architecture
- dreamlike realism
- subdued color palettes
- East Asian contemporary painting
- poetic urban loneliness
- emotional cityscape painting
- quiet contemporary realism
"""


def call_claude(prompt, max_tokens=1800):
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    return response.content[0].text

with open("artist_dossier.md", "r", encoding="utf-8") as f:
    ARTIST_PROFILE = f.read()
    
def run_research_agent(agent_name, agent_focus, output_requirements):
    prompt = f"""
You are {agent_name}.



Artist profile:
{ARTIST_PROFILE}

Your specific focus:
{agent_focus}

Output requirements:
{output_requirements}

Rules:
- Do not invent facts.
- If something may be outdated or uncertain, write "needs verification."
- Prefer concrete names of galleries, art spaces, curators, contests, magazines, fairs, or programs.
- Explain why each recommendation fits this artist.
- Include what should be manually checked later.
- Do not send emails or write outreach yet.
"""

    return call_claude(prompt)


agent_a_focus = """
Traditional gallery research.

Find Tokyo galleries with serious contemporary painting programs.
Prioritize galleries with credibility, collector visibility, and a history of showing painters.
Avoid places that are mainly installation-only, performance-only, or too conceptual for quiet urban painting.
"""

agent_a_output = """
Create a ranked list of 8–12 Tokyo galleries.

For each:
1. Name
2. Location/neighborhood if known
3. Why it fits
4. Risk or mismatch
5. What to verify manually
"""


agent_b_focus = """
Emerging and alternative scene research.

Find smaller galleries, project spaces, artist-run spaces, young artist programs,
and spaces that might be open to poetic, melancholic, urban, atmospheric, or narrative painting.
Prioritize realistic approachability.
"""

agent_b_output = """
Create a ranked list of 8–12 emerging or alternative opportunities in Tokyo.

For each:
1. Name
2. Location/neighborhood if known
3. Why it fits
4. How approachable it seems
5. What to verify manually
"""


agent_c_focus = """
Commercial and international strategy research.

Find opportunities where the artist's work might connect with buyers,
collectors, print buyers, book/illustration audiences, international audiences,
or design-adjacent art spaces.

Think beyond galleries:
- art fairs
- print fairs
- illustration fairs
- art book fairs
- magazines
- online galleries
- collector-facing platforms
- cafes/design spaces that sell art
"""

agent_c_output = """
Create a ranked list of 8–12 commercially promising opportunities.

For each:
1. Name
2. Type of opportunity
3. Why it fits commercially
4. Likely buyer/audience type
5. What to verify manually
"""


print("Running Agent A...")
report_a = run_research_agent(
    "Agent A: Traditional Gallery Researcher",
    agent_a_focus,
    agent_a_output
)

print("Running Agent B...")
report_b = run_research_agent(
    "Agent B: Emerging Scene Researcher",
    agent_b_focus,
    agent_b_output
)

print("Running Agent C...")
report_c = run_research_agent(
    "Agent C: Commercial Strategy Researcher",
    agent_c_focus,
    agent_c_output
)


combined_reports = f"""
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


synthesizer_prompt = f"""
You are Agent D: Senior Art Strategy Synthesizer.

You have received three reports:
1. Traditional Gallery Researcher
2. Emerging Scene Researcher
3. Commercial Strategy Researcher

Your task:
Create a final strategic report.

You must include:

1. Executive Summary
A short plain-English summary of the overall opportunity landscape.

2. Strongest Overall Matches
Rank the 10 strongest opportunities across all three reports.

For each:
- Name
- Type
- Why it fits
- Confidence level: High / Medium / Low
- What must be verified manually

3. Best Near-Term Targets
List the 5 most realistic places to research first.

4. Highest-Prestige Targets
List the most ambitious but potentially valuable targets.

5. Commercial Opportunities
List the best print, collector, fair, publication, or design-adjacent opportunities.

6. Contradictions / Weak Recommendations
Identify any recommendations from the agents that seem questionable, risky, too vague, or mismatched.

7. Research To-Do List
Make a clear manual research checklist for the human user.

8. Suggested Next Move
Tell the user what to do next in practical order.

Rules:
- Do not invent certainty.
- If a recommendation needs verification, say so.
- Be blunt and useful.
- Assume this is an early prototype report.

Reports to synthesize:

{combined_reports}
"""

print("Running Synthesizer Agent...")
synthesized_report = call_claude(synthesizer_prompt, max_tokens=2600)


final_report = f"""
{combined_reports}

---

# Agent D Report: Synthesized Strategic Report

{synthesized_report}
"""


with open("final_gallery_report.md", "w", encoding="utf-8") as f:
    f.write(final_report)

print(final_report)
print("\n\nSaved final report to final_gallery_report.md")