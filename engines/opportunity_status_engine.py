
import json
import os
from datetime import date, timedelta
from pathlib import Path


OPP_PATH = "deploy_data/compact_opportunities.json"
STATUS_PATH = "memory/opportunity_status.json"
ACTION_QUEUE_PATH = "memory/action_queue.json"
SUPPRESSION_PATH = "memory/ibm_suppression.json"


DEFAULT_STATUS = {
    "status": "new",
    "saved": False,
    "rejected": False,
    "contacted": False,
    "response_received": False,
    "follow_up_date": "",
    "notes": "",
    "last_updated": "",
}


def load_json(path, fallback):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def title_of(opp):
    return opp.get("title") or opp.get("name") or "Unknown"


def key_for(opp):
    raw = title_of(opp) + "::" + str(opp.get("organization") or "")
    return raw.strip().lower()


def score_num(value):
    try:
        return float(value or 0)
    except Exception:
        return 0.0


def missing_fields(opp):
    missing = []
    if not (opp.get("source_link") or opp.get("source_url") or opp.get("official_website") or opp.get("submission_page")):
        missing.append("source")
    if not opp.get("submission_page"):
        missing.append("submission process")
    if not opp.get("deadline"):
        missing.append("deadline")
    if not opp.get("fees"):
        missing.append("fees")
    if not (opp.get("contact") or opp.get("email") or opp.get("contact_url")):
        missing.append("contact")
    return missing


def recommended_action(opp, status):
    if status.get("rejected"):
        return "No action — rejected."

    if status.get("contacted") and not status.get("response_received"):
        if status.get("follow_up_date"):
            return f"Waiting for response. Follow up on {status.get('follow_up_date')}."
        return "Waiting for response. Set a follow-up date."

    missing = missing_fields(opp)

    if missing:
        return "Research missing details: " + ", ".join(missing[:3]) + "."

    if score_num(opp.get("overall_score")) >= 7:
        return "High-fit opportunity. Review report and prepare outreach."

    if score_num(opp.get("overall_score")) >= 5.5:
        return "Promising. Save or compare against higher-fit options."

    return "Low urgency. Keep only if strategically relevant."


def initialize_statuses():
    opps = load_json(OPP_PATH, [])
    statuses = load_json(STATUS_PATH, {})

    changed = False

    for opp in opps:
        key = key_for(opp)
        if key not in statuses:
            statuses[key] = dict(DEFAULT_STATUS)
            statuses[key]["last_updated"] = date.today().isoformat()
            changed = True

    if changed:
        save_json(STATUS_PATH, statuses)

    print(f"Status records available: {len(statuses)}")


def update_status(title_key, **updates):
    statuses = load_json(STATUS_PATH, {})
    current = statuses.get(title_key, dict(DEFAULT_STATUS))

    for k, v in updates.items():
        current[k] = v

    current["last_updated"] = date.today().isoformat()
    statuses[title_key] = current
    save_json(STATUS_PATH, statuses)


def build_action_queue():
    opps = load_json(OPP_PATH, [])
    statuses = load_json(STATUS_PATH, {})

    queue = []

    for opp in opps:
        key = key_for(opp)
        status = statuses.get(key, dict(DEFAULT_STATUS))
        score = score_num(opp.get("overall_score"))
        missing = missing_fields(opp)

        if status.get("rejected"):
            continue

        priority = "low"
        if score >= 7 or len(missing) >= 3:
            priority = "high"
        elif score >= 5.5 or missing:
            priority = "medium"

        queue.append({
            "key": key,
            "title": title_of(opp),
            "organization": opp.get("organization", ""),
            "score": score,
            "priority": priority,
            "status": status.get("status", "new"),
            "saved": status.get("saved", False),
            "contacted": status.get("contacted", False),
            "response_received": status.get("response_received", False),
            "follow_up_date": status.get("follow_up_date", ""),
            "missing": missing,
            "recommended_action": recommended_action(opp, status),
        })

    priority_order = {"high": 0, "medium": 1, "low": 2}
    queue.sort(key=lambda x: (priority_order.get(x["priority"], 9), -x["score"]))

    save_json(ACTION_QUEUE_PATH, queue)
    print(f"Built action queue with {len(queue)} items.")


def mark_saved(title_key):
    update_status(title_key, status="saved", saved=True)


def mark_rejected(title_key, reason=""):
    update_status(title_key, status="rejected", rejected=True, notes=reason)


def load_suppression():
    data = load_json(SUPPRESSION_PATH, {})
    return data.get("suppressed", {})


def mark_not_for_me(title_key, reason=""):
    """Mark as rejected and add to IBM suppression list so pipeline excludes it."""
    update_status(title_key, status="not_for_me", rejected=True, notes=reason)
    data = load_json(SUPPRESSION_PATH, {"suppressed": {}})
    data.setdefault("suppressed", {})[title_key] = {
        "reason": reason,
        "date": date.today().isoformat(),
    }
    save_json(SUPPRESSION_PATH, data)


def mark_contacted(title_key, follow_up_days=14):
    follow_up = (date.today() + timedelta(days=follow_up_days)).isoformat()
    update_status(
        title_key,
        status="contacted",
        saved=True,
        contacted=True,
        follow_up_date=follow_up,
    )


def mark_response_received(title_key):
    update_status(title_key, status="response_received", response_received=True)


def main():
    initialize_statuses()
    build_action_queue()


if __name__ == "__main__":
    main()
