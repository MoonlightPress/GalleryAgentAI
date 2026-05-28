import json
import os
from pathlib import Path

from opportunity_buckets import (
    bucket_opportunity,
)

from career_stage_profiles import (
    CAREER_STAGES,
)


OPP_PATH = "deploy_data/compact_opportunities.json"

OUT_PATH = (
    "memory/strategy_feed.json"
)


def load_json(path, fallback):
    if os.path.exists(path):
        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    return fallback


def save_json(path, data):
    Path(path).parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False,
        )


def title_of(opp):
    return (
        opp.get("title")
        or opp.get("name")
        or "Unknown"
    )


def strategic_reason(opp, bucket):
    category = (
        opp.get("category_label")
        or opp.get("category")
        or ""
    )

    if bucket == "career_changing":
        return (
            "High-prestige opportunity "
            "with strong long-term impact."
        )

    if bucket == "easy_win":
        return (
            "Strong fit with relatively "
            "low barrier to entry."
        )

    if bucket == "community_builder":
        return (
            "Useful for building local "
            "connections and visibility."
        )

    if bucket == "portfolio_builder":
        return (
            "Good opportunity for "
            "publication history and portfolio depth."
        )

    if bucket == "low_probability":
        return (
            "Prestige or difficulty may "
            "outweigh current likelihood."
        )

    return (
        "Potentially useful depending "
        "on current strategic goals."
    )


def build_strategy_feed():
    opps = load_json(OPP_PATH, [])

    feed = {
        "featured": [],
        "easy_wins": [],
        "career_changing": [],
        "portfolio_builders": [],
        "community_builders": [],
    }

    sorted_opps = sorted(
        opps,
        key=lambda x: float(
            x.get("overall_score", 0) or 0
        ),
        reverse=True,
    )

    for opp in sorted_opps:
        bucket = bucket_opportunity(opp)

        item = {
            "title": title_of(opp),
            "bucket": bucket,
            "score": opp.get("overall_score"),
            "confidence": opp.get(
                "confidence_level"
            ),
            "reason": strategic_reason(
                opp,
                bucket,
            ),
            "category": opp.get(
                "category_label"
            ),
            "city": opp.get("city"),
            "image": opp.get(
                "card_image",
                "",
            ),
        }

        if len(feed["featured"]) < 12:
            feed["featured"].append(item)

        if (
            bucket == "easy_win"
            and len(feed["easy_wins"]) < 12
        ):
            feed["easy_wins"].append(item)

        if (
            bucket == "career_changing"
            and len(feed["career_changing"]) < 12
        ):
            feed["career_changing"].append(item)

        if (
            bucket == "portfolio_builder"
            and len(feed["portfolio_builders"]) < 12
        ):
            feed["portfolio_builders"].append(item)

        if (
            bucket == "community_builder"
            and len(feed["community_builders"]) < 12
        ):
            feed["community_builders"].append(item)

    save_json(OUT_PATH, feed)

    print(
        "Built strategy feed:"
    )

    for k, v in feed.items():
        print(f"{k}: {len(v)}")


if __name__ == "__main__":
    build_strategy_feed()