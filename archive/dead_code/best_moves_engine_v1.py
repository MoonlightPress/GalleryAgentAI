import json
from pathlib import Path

OUT_MEMORY = Path("memory/best_moves.json")
OUT_DEPLOY = Path("deploy_data/best_moves.json")
OUT_REPORT = Path("reports/best_moves.md")

SOURCES = {
    "gallery_fit": Path("memory/gallery_fit_analysis.json"),
    "gallery_profiles": Path("memory/gallery_profiles.json"),
    "verified_competitions": Path("memory/verified_competitions.json"),
    "fair_ecosystem": Path("memory/fair_ecosystem.json"),
    "verified_open_calls": Path("memory/verified_open_calls.json"),
    "category_context": Path("memory/category_context.json"),
    "ecosystem_summary": Path("memory/ecosystem_summary_v2.json"),
    "verified_fields": Path("memory/verified_opportunity_fields.json"),
}

def load(path, fallback):
    if path.exists():
        return json.load(open(path, encoding="utf-8"))
    return fallback

def clean_title(s):
    s = str(s or "").strip()
    # remove clipped ellipsis titles only lightly; keep original enough to trace source
    return s[:140]

def is_bad_title(title):
    t = title.lower()
    bad = [
        "instagram",
        "jimttof", "jimtof",
        "tokyo artist visa",
        "clone of japan fair",
        "booth - the international indie art marketplace",
        "guide to", "best contemporary", "top opportunities",
        "50 best", "artist opportunities 2026",
        "calls for entry | artwork archive",
        "art jobs in japan",
        "trade shows worldwide",
        "machine tool",
    ]
    return any(x in t for x in bad)

def move(name, category, score, reason, action, url="", confidence=70, deadline="", fee="", source=""):
    return {
        "name": clean_title(name),
        "category": category,
        "score": int(round(score or 0)),
        "confidence": int(round(confidence or 0)),
        "reason": reason,
        "next_action": action,
        "url": url or "",
        "deadline": deadline or "",
        "fee": fee or "",
        "source": source or "",
    }

def top_unique(items, limit=3):
    out = []
    seen = set()
    for item in items:
        name = item.get("name", "")
        key = name.lower().replace("｜", "|").split("|")[0].strip()
        if not name or key in seen or is_bad_title(name):
            continue
        seen.add(key)
        out.append(item)
        if len(out) >= limit:
            break
    return out

def build_galleries():
    data = load(SOURCES["gallery_fit"], {"records": []})
    profiles = load(SOURCES["gallery_profiles"], {"profiles": []}).get("profiles", [])
    records = data.get("records", [])
    profile_count = len(profiles)
    direct = len([p for p in profiles if p.get("submission_signal")])
    emerging = len([p for p in profiles if "emerging-friendly" in p.get("gallery_type", [])])

    candidates = []
    for r in records:
        name = r.get("name", "")
        if is_bad_title(name):
            continue
        score = r.get("fit_score", 0)
        risk = r.get("risk_score", 50)
        tags = set(r.get("tags", []))
        # Penalize obvious articles/directories.
        if "research later" in r.get("tier", "").lower():
            score -= 18
        if "rental" in tags:
            score -= 10
        if "submission route" in tags:
            score += 8
        if "emerging friendly" in tags:
            score += 8
        if "local west Tokyo" in tags:
            score += 4

        reason_bits = []
        if "submission route" in tags:
            reason_bits.append("submission route")
        if "emerging friendly" in tags:
            reason_bits.append("emerging-artist signal")
        if "local west Tokyo" in tags:
            reason_bits.append("local west-Tokyo target")
        if "prestige" in tags:
            reason_bits.append("prestige signal")
        reason = "Good gallery target: " + ", ".join(reason_bits or ["needs manual fit review"]) + "."

        candidates.append(move(
            name=name,
            category="galleries",
            score=score,
            confidence=max(40, 100 - risk),
            reason=reason,
            action="Review past artists, confirm curated vs rental, then shortlist for contact.",
            url=r.get("url", ""),
            source="gallery_fit_analysis",
        ))

    return {
        "title": "Galleries",
        "summary": f"{profile_count} gallery profiles found; {direct} show direct submission signals; {emerging} are emerging-friendly.",
        "best_moves": top_unique(sorted(candidates, key=lambda x: (x["score"], x["confidence"]), reverse=True), 3),
        "see_more_label": "See more gallery targets",
    }

def build_competitions():
    records = load(SOURCES["verified_competitions"], {"records": []}).get("records", [])
    actionable = [r for r in records if r.get("status") == "actionable"]
    candidates = []
    for r in actionable:
        name = r.get("name", "")
        if is_bad_title(name):
            continue
        score = r.get("score", 0)
        deadline = r.get("deadline", "")
        fee = r.get("fee", "")
        if deadline and "Check source" not in deadline:
            score += 8
        if fee and "Check source" not in fee:
            score += 3
        if any(x in name.lower() for x in ["tokas", "contemporary art award", "brillia", "face", "caf", "mimoca", "belladonna", "世界絵画"]):
            score += 8

        candidates.append(move(
            name=name,
            category="competitions",
            score=score,
            confidence=80 if deadline else 60,
            reason="Actionable competition with an extracted application route and deadline signal.",
            action="Open source, confirm deadline/fee, then decide if it fits the current portfolio.",
            url=r.get("url", ""),
            deadline=deadline,
            fee=fee,
            source="verified_competitions",
        ))

    return {
        "title": "Competitions",
        "summary": f"{len(records)} competitions verified; {len(actionable)} currently look actionable.",
        "best_moves": top_unique(sorted(candidates, key=lambda x: (x["score"], x["confidence"]), reverse=True), 3),
        "see_more_label": "See more competitions",
    }

def build_fairs():
    records = load(SOURCES["fair_ecosystem"], {"targets": []}).get("targets", [])
    candidates = []
    for r in records:
        name = r.get("name", "")
        if is_bad_title(name):
            continue
        score = r.get("score", 0)
        if r.get("beginner_friendliness") == "high":
            score += 8
        if r.get("prestige") == "high":
            score += 6
        if "zine" in r.get("fair_type", "") or "book" in r.get("fair_type", ""):
            score += 5
        if r.get("application_route") in {"form", "application_page", "email_possible"}:
            score += 5

        reason = f"{r.get('fair_type', 'fair/event')} target"
        if r.get("beginner_friendliness") != "unknown":
            reason += f"; beginner friendliness: {r.get('beginner_friendliness')}"
        if r.get("prestige") != "unknown":
            reason += f"; prestige: {r.get('prestige')}"
        reason += "."

        candidates.append(move(
            name=name,
            category="fairs_events",
            score=score,
            confidence=75 if r.get("application_url") else 55,
            reason=reason,
            action="Check application window, booth fee, table requirements, and whether prints/zines are ready.",
            url=r.get("application_url", ""),
            deadline=r.get("deadline", ""),
            fee=r.get("fee", ""),
            source="fair_ecosystem",
        ))

    beginner = len([r for r in records if r.get("beginner_friendliness") == "high"])
    prestige = len([r for r in records if r.get("prestige") == "high"])
    return {
        "title": "Fairs / Events",
        "summary": f"{len(records)} fairs/events mapped; {beginner} beginner-friendly; {prestige} high-prestige.",
        "best_moves": top_unique(sorted(candidates, key=lambda x: (x["score"], x["confidence"]), reverse=True), 3),
        "see_more_label": "See more fairs/events",
    }

def build_zines():
    records = load(SOURCES["fair_ecosystem"], {"targets": []}).get("targets", [])
    verified = load(SOURCES["verified_fields"], {"records": []}).get("records", [])
    zine_records = [
        r for r in records
        if "zine" in r.get("fair_type", "").lower()
        or "book" in r.get("fair_type", "").lower()
        or "zine" in r.get("name", "").lower()
        or "book fair" in r.get("name", "").lower()
    ]

    candidates = []
    for r in zine_records:
        name = r.get("name", "")
        if is_bad_title(name):
            continue
        score = r.get("score", 0) + 8
        if r.get("prestige") == "high":
            score += 8
        if r.get("beginner_friendliness") == "high":
            score += 5
        candidates.append(move(
            name=name,
            category="zines",
            score=score,
            confidence=80 if r.get("application_url") else 60,
            reason="Strong zine/art-book ecosystem target with clear relevance to printed work.",
            action="Confirm deadline and fee, then match it to the two-zine plan.",
            url=r.get("application_url", ""),
            deadline=r.get("deadline", ""),
            fee=r.get("fee", ""),
            source="fair_ecosystem",
        ))

    return {
        "title": "Zines / Art Books",
        "summary": f"{len(zine_records)} zine/art-book fair targets found. Best used after two small zines exist.",
        "best_moves": top_unique(sorted(candidates, key=lambda x: (x["score"], x["confidence"]), reverse=True), 3),
        "see_more_label": "See more zine/art-book targets",
    }

def build_open_calls():
    records = load(SOURCES["verified_open_calls"], {"records": []}).get("records", [])
    actionable = [r for r in records if r.get("status") == "actionable"]
    candidates = []
    for r in actionable:
        name = r.get("name", "")
        if is_bad_title(name):
            continue
        score = r.get("actionability_score") or 70
        if r.get("deadline") and "Check source" not in r.get("deadline", ""):
            score += 8
        if any(x in name.lower() for x in ["tokas", "shoto", "belladonna", "hayama"]):
            score += 6
        candidates.append(move(
            name=name,
            category="open_calls",
            score=score,
            confidence=80,
            reason="Verified call/application record with actionable source data.",
            action="Confirm deadline, fee, eligibility, and required files.",
            url=r.get("url", ""),
            deadline=r.get("deadline", ""),
            fee=r.get("fee", ""),
            source="verified_open_calls",
        ))

    return {
        "title": "Open Calls",
        "summary": f"{len(records)} verified open-call/application records; {len(actionable)} actionable.",
        "best_moves": top_unique(sorted(candidates, key=lambda x: (x["score"], x["confidence"]), reverse=True), 3),
        "see_more_label": "See more open calls",
    }

def main():
    categories = [
        build_galleries(),
        build_competitions(),
        build_zines(),
        build_fairs(),
        build_open_calls(),
    ]

    # Global best moves, deduped across categories.
    all_moves = []
    for cat in categories:
        all_moves.extend(cat["best_moves"])
    global_best = top_unique(sorted(all_moves, key=lambda x: (x["score"], x["confidence"]), reverse=True), 5)

    result = {
        "title": "Best Next Moves",
        "summary": "Compressed recommendations generated from the current opportunity research. Reports remain in the background.",
        "global_best_moves": global_best,
        "categories": categories,
    }

    OUT_MEMORY.parent.mkdir(exist_ok=True)
    OUT_DEPLOY.parent.mkdir(exist_ok=True)
    OUT_REPORT.parent.mkdir(exist_ok=True)

    OUT_MEMORY.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_DEPLOY.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# Best Next Moves", "", result["summary"], "", "## Overall", ""]
    for i, m in enumerate(global_best, 1):
        lines.append(f"{i}. **{m['name']}** — {m['category']} — score {m['score']}")
        lines.append(f"   - Why: {m['reason']}")
        lines.append(f"   - Next: {m['next_action']}")
        if m.get("deadline"):
            lines.append(f"   - Deadline: {m['deadline']}")
        if m.get("fee"):
            lines.append(f"   - Fee: {m['fee']}")
        if m.get("url"):
            lines.append(f"   - URL: {m['url']}")
        lines.append("")

    for cat in categories:
        lines += ["", f"## {cat['title']}", "", cat["summary"], ""]
        for i, m in enumerate(cat["best_moves"], 1):
            lines.append(f"{i}. **{m['name']}** — score {m['score']}")
            lines.append(f"   - Why: {m['reason']}")
            lines.append(f"   - Next: {m['next_action']}")
            if m.get("url"):
                lines.append(f"   - URL: {m['url']}")
            lines.append("")

    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")

    print("Wrote", OUT_MEMORY)
    print("Wrote", OUT_DEPLOY)
    print("Wrote", OUT_REPORT)

if __name__ == "__main__":
    main()
