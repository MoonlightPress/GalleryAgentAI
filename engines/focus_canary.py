"""Is Today's Focus actually usable today?

Written 2026-08-21, after her three slots turned out to be an expired
aggregator listing (linking to the 2025 edition), an exhibition that finished
in June, and a gallery-only art fair she cannot enter. All three had been wrong
for an unknown length of time, and nothing in the system was watching — they
were found because Scott happened to ask whether the good ones were at the top.

Three assertions cover all of those failures:
  * every slot is filled
  * nothing in it has a passed deadline
  * nothing in it is structurally ineligible for her
plus a fourth: no two slots are the same opportunity wearing different names,
which silently turns three choices into two.

Pure, no I/O — scripts/check_attention.py runs it after the weekly job and
carries anything it finds to Discord.
"""
SLOTS = ("quick_win", "high_impact", "stretch_goal")

# Prerequisites she cannot satisfy by preparing. Mirrors api._STRUCTURAL_PREREQS;
# exhibition-history requirements are deliberately absent, because building a CV
# is exactly what a stretch goal is for.
STRUCTURAL_PREREQS = frozenset({
    "organizations_only", "youth_only", "gallery_representation", "invitation_only",
})


def _one(value):
    """Slots are served as an object, but tolerate a list."""
    if isinstance(value, list):
        return value[0] if value else None
    return value


def _name(opp):
    return str(opp.get("name") or opp.get("title") or "").strip()


def audit_focus(focus, dedup_key=None):
    """Return a list of human-readable problems. Empty list means healthy.

    `dedup_key` is injectable so this stays import-light; it defaults to the
    api's real one, which is what decides whether two cards are one thing.
    """
    if dedup_key is None:
        try:
            from api import _dedup_key as dedup_key
        except Exception:
            dedup_key = lambda n: (n or "").lower().replace(" ", "")

    problems = []
    filled = {}

    for name in SLOTS:
        opp = _one(focus.get(name))
        if not opp:
            problems.append(f"{name}: empty — she sees fewer than three things today")
            continue
        filled[name] = opp
        label = _name(opp) or "(unnamed)"
        if opp.get("deadline_past"):
            problems.append(
                f"{name}: deadline has passed — {label!r} is being offered as today's action")
        bad = STRUCTURAL_PREREQS & {str(p) for p in (opp.get("prerequisites") or [])}
        if bad:
            problems.append(
                f"{name}: not eligible ({', '.join(sorted(bad))}) — {label!r} is a door she cannot open")

    seen = {}
    for name, opp in filled.items():
        key = dedup_key(_name(opp))
        if key and key in seen:
            problems.append(
                f"{seen[key]} and {name}: the same opportunity under two names "
                f"({_name(opp)!r}) — three slots showing two things")
        elif key:
            seen[key] = name

    return problems
