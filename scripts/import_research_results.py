"""
Two-pass research import for opportunities.json:

Pass 1 — Match & apply from existing research_results.json (best-effort name match)
Pass 2 — Live Tavily search on the actual opportunities.json records to fill
         any still-missing deadline / fees / submission_page / contact_email

Fields applied only when the current value is blank, None, or a placeholder
("Check source", "Check current schedule", "TBD", "Unknown", etc.).

Writes: memory/opportunities.json (in place)
"""
import sys, json, re, os, time
from pathlib import Path
from difflib import SequenceMatcher

sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")
MEM = ROOT / "memory"

from tavily import TavilyClient
tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

PLACEHOLDER = {"check source", "check current schedule", "tbd", "unknown",
               "n/a", "none", "", "see website", "varies", "check site"}

EMAIL_RE   = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')
FEE_RE     = re.compile(r'(?:¥|USD|\$|€|£|JPY|entry fee|submission fee|application fee)[^\n.]{0,80}',
                        re.IGNORECASE)
SUBMIT_RE  = re.compile(r'https?://[^\s"\'<>]+(?:submit|apply|entry|entries|application|form)[^\s"\'<>]*',
                        re.IGNORECASE)
CLOSED_RE  = re.compile(r'\b(closed|no longer accepting|submissions? closed|deadline passed|ended)\b',
                        re.IGNORECASE)
DATE_PATS  = [
    r'\b(January|February|March|April|May|June|July|August|September|October|November|December)'
    r'\s+\d{1,2},?\s+202[5-9]\b',
    r'\b\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)'
    r'\s+202[5-9]\b',
    r'\b202[5-9][-/]\d{2}[-/]\d{2}\b',
]


def is_blank(val):
    return not val or str(val).strip().lower() in PLACEHOLDER


def extract(text: str, source_url: str = "") -> dict:
    found = {}
    for pat in DATE_PATS:
        m = re.search(pat, text)
        if m:
            found["deadline"] = m.group(0)
            break
    for m in EMAIL_RE.finditer(text):
        e = m.group(0)
        if not any(skip in e for skip in ["@example", "@your", "@email", "@sentry"]):
            found["contact_email"] = e
            break
    m = FEE_RE.search(text)
    if m:
        found["fees"] = m.group(0).strip()
    for m in SUBMIT_RE.finditer(text):
        u = m.group(0)
        if u != source_url:
            found["submission_page"] = u
            break
    if CLOSED_RE.search(text):
        found["is_active"] = False
    return found


def tavily_search(query: str, url: str = "") -> str:
    q = url if url.startswith("http") else query
    for attempt in range(3):
        try:
            res = tavily.search(q, search_depth="basic", max_results=3)
            text = ""
            for r in res.get("results", []):
                text += f"\n{r.get('url','')}\n{r.get('content','')[:600]}\n"
            time.sleep(3.0)
            return text
        except Exception as e:
            msg = str(e)
            if "excessive" in msg or "rate" in msg.lower() or "blocked" in msg.lower():
                wait = 20 * (attempt + 1)
                print(f"    Rate limited — waiting {wait}s …")
                time.sleep(wait)
            else:
                print(f"    Tavily error: {e}")
                return ""
    return ""


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def similarity(a, b):
    return SequenceMatcher(None, slugify(a), slugify(b)).ratio()


def main():
    rr   = json.loads((MEM / "research_results.json").read_text(encoding="utf-8"))
    opps = json.loads((MEM / "opportunities.json").read_text(encoding="utf-8"))
    if isinstance(opps, dict):
        opps = opps.get("opportunities", opps.get("items", []))

    # ── Pass 1: apply from existing research_results ──────────────────────
    print("Pass 1 — applying from research_results.json")
    print("─" * 60)

    rr_index = {r["name"]: r.get("extracted", {}) for r in rr.get("results", []) if r.get("extracted")}

    pass1_applied = 0
    for opp in opps:
        name = opp.get("name", "")
        # Best fuzzy match from rr_index
        best_score, best_ext = 0.0, {}
        for rname, ext in rr_index.items():
            s = similarity(name, rname)
            if s > best_score:
                best_score, best_ext = s, ext

        if best_score < 0.75:
            continue

        applied = []
        for src, dst in [("deadline","deadline"),("fees","fees"),
                         ("submission_page","submission_page"),("contact_email","contact_email")]:
            if best_ext.get(src) and is_blank(opp.get(dst)):
                opp[dst] = best_ext[src]
                applied.append(dst)
                pass1_applied += 1
        if best_ext.get("is_active") is False and opp.get("status") != "permanently_closed":
            opp["status"] = "permanently_closed"
            applied.append("status→closed")
            pass1_applied += 1
        if applied:
            print(f"  {name[:40]:<40} score={best_score:.2f}  applied: {applied}")

    print(f"  Fields applied from cache: {pass1_applied}")
    print()

    # ── Pass 2: live Tavily search on still-missing opportunities ──────────
    NEED_FIELDS = ["deadline", "fees", "submission_page", "contact_email"]

    targets = []
    for opp in opps:
        if opp.get("status") == "permanently_closed":
            continue
        missing = [f for f in NEED_FIELDS if is_blank(opp.get(f))]
        if missing:
            targets.append((opp, missing))

    print(f"Pass 2 — live Tavily search on {len(targets)} opportunities with missing fields")
    print("─" * 60)

    pass2_applied = 0
    for i, (opp, missing) in enumerate(targets):
        name     = opp.get("name", "")
        url      = opp.get("official_website", "") or opp.get("source_url", "")
        print(f"[{i+1}/{len(targets)}] {name}  missing={missing}")

        text = tavily_search(f'"{name}" open call deadline submission fee 2026', url)
        if not text.strip():
            print(f"  no results")
            continue

        found = extract(text, url)
        applied = []
        for src, dst in [("deadline","deadline"),("fees","fees"),
                         ("submission_page","submission_page"),("contact_email","contact_email")]:
            if found.get(src) and is_blank(opp.get(dst)):
                opp[dst] = found[src]
                applied.append(f"{dst}={str(found[src])[:40]}")
                pass2_applied += 1
        if found.get("is_active") is False and opp.get("status") != "permanently_closed":
            opp["status"] = "permanently_closed"
            applied.append("status→closed")
            pass2_applied += 1

        print(f"  {'applied: ' + ', '.join(applied) if applied else 'nothing new'}")

    print()
    print(f"Pass 2 fields applied: {pass2_applied}")
    print()

    (MEM / "opportunities.json").write_text(
        json.dumps(opps, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Saved opportunities.json  (pass1={pass1_applied}, pass2={pass2_applied},"
          f" total={pass1_applied+pass2_applied})")


if __name__ == "__main__":
    main()
