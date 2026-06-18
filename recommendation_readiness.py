RELATIONSHIP_CATEGORIES = {
    "gallery",
    "gallery_small",
    "cafe_gallery",
    "artist_space",
    "bookstore_gallery",
    "bookstore_event",
    "gallery_event",
    "event_space",
    "zine_shop_consignment",
}

PHOTOGRAPHY_CATEGORIES = {"photo_open_call", "global_photobook"}

READY = "ready"
CHECK = "check_before_acting"
REVIEW = "review"
CLOSED = "closed_or_stale"


def assess_actionability(opp: dict) -> dict:
    flags: list[str] = []
    reasons: list[str] = []

    category = opp.get("category", "")
    relationship = category in RELATIONSHIP_CATEGORIES

    if _is_photography_only(opp):
        flags.append("photography_only")
        return _result(CLOSED, flags, reasons)

    if opp.get("status") in {"closed_this_cycle", "closed", "permanently_closed"}:
        flags.append(str(opp.get("status")))
        return _result(CLOSED, flags, reasons)

    if opp.get("deadline_past") and not relationship:
        flags.append("deadline_past")
        return _result(CLOSED, flags, reasons)

    deadline_ready = _deadline_ready(opp, relationship)
    fee_ready = _fee_ready(opp)
    route_ready = _route_ready(opp)
    source_ready = _source_ready(opp)

    if deadline_ready:
        reasons.append("Deadline is checked" if not relationship else "Evergreen or proposal-based")
    else:
        flags.append("deadline_unverified")

    if fee_ready == READY:
        reasons.append("Fee is known")
    elif fee_ready == CHECK:
        flags.append("fee_unknown")
    else:
        flags.append("fee_missing")

    if route_ready:
        reasons.append("Relationship contact route exists" if relationship else "Submission path is clear")
    else:
        flags.append("submission_or_contact_missing")

    if source_ready == CHECK:
        flags.append("source_needs_reverification")
    elif source_ready == REVIEW:
        flags.append("source_unverified")

    if opp.get("student_call") and not opp.get("artist_eligible"):
        flags.append("student_only")

    if relationship and route_ready:
        if "deadline_unverified" in flags:
            flags.remove("deadline_unverified")
        if flags:
            return _result(CHECK, flags, reasons)
        return _result(READY, flags, reasons)

    if not route_ready or not deadline_ready or "student_only" in flags:
        return _result(REVIEW, flags, reasons)

    if source_ready == REVIEW:
        return _result(REVIEW, flags, reasons)

    if fee_ready == CHECK or source_ready == CHECK:
        return _result(CHECK, flags, reasons)

    return _result(READY, flags, reasons)


def _deadline_ready(opp: dict, relationship: bool) -> bool:
    if relationship:
        return True
    return bool(opp.get("deadline_verified"))


def _fee_ready(opp: dict) -> str:
    if opp.get("fees_verified"):
        return READY
    fees = str(opp.get("fees") or "").strip().lower()
    if fees and fees not in {"unknown", "tbd", "check source", "check site"}:
        if "unknown" in fees or "confirm" in fees:
            return CHECK
        return READY
    return CHECK


def _route_ready(opp: dict) -> bool:
    if opp.get("submission_page"):
        return True
    contact = str(opp.get("contact") or opp.get("contact_email") or opp.get("contact_url") or "")
    return bool(contact) or bool(opp.get("contact_verified"))


def _source_ready(opp: dict) -> str:
    status = str(opp.get("url_verification_status") or "").lower()
    if status == "ok":
        return READY
    if opp.get("status") == "needs_reverification":
        return CHECK
    if _route_ready(opp):
        return CHECK
    return REVIEW


def _is_photography_only(opp: dict) -> bool:
    if opp.get("native_medium") == "photography":
        return True
    if opp.get("category") not in PHOTOGRAPHY_CATEGORIES:
        return False
    accepted = str(opp.get("accepted_media") or opp.get("recommended_body_of_work") or "").lower()
    return not any(term in accepted for term in ("watercolor", "painting", "artist book"))


def _result(status: str, flags: list[str], reasons: list[str]) -> dict:
    return {
        "actionability_status": status,
        "review_flags": _unique(flags),
        "recommendation_reasons": _unique(reasons)[:3],
    }


def _unique(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        if value and value not in seen:
            result.append(value)
            seen.add(value)
    return result
