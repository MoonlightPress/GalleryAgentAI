def bucket_opportunity(opp):
    score = float(opp.get("overall_score", 0) or 0)

    category = str(
        opp.get("category") or ""
    ).lower()

    prestige = float(
        opp.get("prestige_score", 0) or 0
    )

    difficulty = float(
        opp.get("difficulty_score", 0) or 0
    )

    if score >= 8 and difficulty <= 5:
        return "easy_win"

    if prestige >= 8 and score >= 7:
        return "career_changing"

    if category in [
        "cafe_gallery",
        "fair_popup",
        "market_event",
    ]:
        return "community_builder"

    if category in [
        "bookstore_gallery",
        "zine_print",
        "online_feature",
    ]:
        return "portfolio_builder"

    if difficulty >= 8 and score <= 5:
        return "low_probability"

    return "general"