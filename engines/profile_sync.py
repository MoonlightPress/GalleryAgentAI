"""
profile_sync.py

Keeps the artist's Peppercorn edits and the canonical artist_master_profile.json
in sync, and decides which opportunities need email drafts (re)written.

The bug this fixes: editing the artist statement in Peppercorn wrote only to
peppercorn_profile.json, which nothing downstream reads. The email-draft writer
(ibm_email_writer.py) reads artist_master_profile.json and is write-once, so a
statement edit never changed her drafts or advice. These pure helpers unify the
source and flag stale drafts so a regen knows to refresh.
"""
from __future__ import annotations


def apply_peppercorn_edits(master: dict, peppercorn: dict) -> tuple[dict, bool]:
    """Merge a Peppercorn edit into the canonical master profile.

    Currently propagates the artist statement (the field the email writer
    consumes). Returns ``(master, changed)``. When the statement actually
    changes, sets ``master['email_drafts_stale'] = True`` so a later regen
    knows the existing drafts are out of date.

    An empty / whitespace-only statement is treated as "no edit" so clearing
    the box in the UI never wipes her real statement.
    """
    new_stmt = (peppercorn or {}).get("artist_statement")
    if not isinstance(new_stmt, str) or not new_stmt.strip():
        return master, False

    new_stmt = new_stmt.strip()
    stmt_block = master.get("artist_statement")
    if not isinstance(stmt_block, dict):
        stmt_block = {}
        master["artist_statement"] = stmt_block

    if stmt_block.get("synthesized_en") == new_stmt:
        return master, False

    stmt_block["synthesized_en"] = new_stmt
    master["email_drafts_stale"] = True
    return master, True


def _is_eligible(opp: dict) -> bool:
    """Tier 1-2 by career tier, plus anything the system says to act on now."""
    return (
        opp.get("career_tier") in (1, 2)
        or opp.get("exclusive_primary_bucket") == "immediate_best_moves"
    )


def select_email_targets(opps: list, master: dict, limit: int) -> list:
    """Pick which opportunities the draft writer should (re)write.

    Normal run: only eligible opps MISSING a draft (cheap, idempotent).
    Stale run (``master['email_drafts_stale']`` truthy): every eligible opp,
    so a profile edit actually refreshes the existing drafts.
    """
    eligible = [o for o in opps if _is_eligible(o)]
    eligible.sort(key=lambda x: float(x.get("overall_score") or 0), reverse=True)

    if master and master.get("email_drafts_stale"):
        targets = eligible
    else:
        targets = [o for o in eligible if not (o.get("email_ja") and o.get("email_en"))]

    return targets[:limit]


def clear_drafts_stale(master: dict) -> dict:
    """Mark the drafts fresh again (call after a successful regen)."""
    master["email_drafts_stale"] = False
    return master


# Default used only if the profile is unreadable / missing the field. Her real
# Instagram following is ~26k (the ~90k figure is her Twitter/X account and a
# longstanding mix-up — see AGENTS.md "Artist Social Media"). Never hardcode a
# follower literal in copy-generating prompts: read it from here so a future
# regen always uses the real, current number from the profile.
_FOLLOWER_FALLBACK = "26k"


def follower_count_str(master: dict) -> str:
    """Return her Instagram follower count as a short display string (e.g. "26k").

    Reads the canonical artist_master_profile.json structure:
      social_presence.instagram.followers      ("26k")  -> preferred
      social_presence.instagram.followers_approx (26000) -> compacted to "26k"
    Falls back to ``_FOLLOWER_FALLBACK`` if neither is present, so a malformed
    profile can never silently inject a wrong number (or crash a prompt build).
    """
    sp = (master or {}).get("social_presence")
    sp = sp if isinstance(sp, dict) else {}
    insta = sp.get("instagram")
    insta = insta if isinstance(insta, dict) else {}

    disp = insta.get("followers")
    if isinstance(disp, str) and disp.strip():
        return disp.strip()

    approx = insta.get("followers_approx")
    if isinstance(approx, (int, float)) and approx > 0:
        n = int(approx)
        if n >= 1000:
            k = n / 1000.0
            # "26k" not "26.0k"; keep one decimal only when it adds information.
            return (f"{k:.0f}k" if abs(k - round(k)) < 0.05 else f"{k:.1f}k")
        return str(n)

    return _FOLLOWER_FALLBACK
