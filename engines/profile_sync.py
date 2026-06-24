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
