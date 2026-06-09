"""
medium_confirmation_gate.py

Whitelist gate: an opportunity only qualifies if its text explicitly
confirms one of the approved visual mediums. Everything else routes
to research_needed so it can be manually verified or annotated.

NEVER deletes records. Rerouting is reversible — pre_gate_bucket
preserves the original bucket so re-running with corrected data
restores the original routing.

Insert in pipeline: after source_medium_classifier.py (native_medium
already set), before any scoring engine.

NOTE: uses 'research_needed' (not 'needs_research') to match BUCKET_ORDER
in exclusive_strategy_bucket_engine.py.
"""
import json
import os
import re
from pathlib import Path

OPP_PATH    = "deploy_data/compact_opportunities.json"
REPORT_PATH = "reports/medium_confirmation_gate_report.md"

# ── Text fields searched, in priority order ────────────────────────────────
# NOTE: recommended_body_of_work is intentionally excluded — it's pipeline-
# generated speculation (portfolio_match_engine), not evidence from the source.
# Including it caused false positives (e.g. poetry presses confirmed via the
# "Artist Book" pattern because the portfolio engine assigned that category).
TEXT_FIELDS = [
    "accepted_media",           # explicit medium field — highest trust
    "title", "name",
    "one_sentence",
    "why_this_fits_short",
    "category_label",
    "quick_action",
    "source_purity_reason",
    "verification_summary",
]

# ── Whitelist patterns ─────────────────────────────────────────────────────
# Each entry: (compiled regex, human label)
# Pattern design notes:
#   - watercolor: allow British spelling
#   - drawing: \bdrawn?\b OR \bdrawings?\b as noun forms only;
#     avoid "drawing attention / drawing on" by requiring word boundary
#     + excluding "drawing on" / "drawing from" via negative lookahead
#   - mixed media: only qualifies in combination; listed here because
#     any visual-art mixed-media context is relevant
CONFIRM_PATTERNS = [
    (re.compile(r'\bwatercolou?r(?:s|ist|ists)?\b', re.I),       'watercolor'),
    (re.compile(r'\bpainting(?:s)?\b|\bpainter(?:s)?\b', re.I), 'painting'),
    (re.compile(r'\bworks?\s+on\s+paper\b', re.I),               'works on paper'),
    (re.compile(r'\billustration(?:s)?\b|\billustrator(?:s)?\b', re.I), 'illustration'),
    (re.compile(r'\bvisual\s+arts?\b', re.I),                    'visual art'),
    (re.compile(r'\bfine\s+arts?\b', re.I),                      'fine art'),
    (re.compile(r'\bprintmaking\b|\blinocut\b|\betching\b|\bscreen\s*print\b', re.I), 'printmaking'),
    (re.compile(r'\bdrawings?\b(?!\s+(?:on|from|upon|to|together|card))', re.I), 'drawing'),
    (re.compile(r'\bgouache\b', re.I),                           'gouache'),
    (re.compile(r'\bartist\s+books?\b', re.I),                   'artist book'),
    (re.compile(r'\bart\s+books?\b', re.I),                      'art book'),
    (re.compile(r'\bmixed\s+media\b', re.I),                     'mixed media'),
    (re.compile(r'\bzines?\b|\bzine\s+fair\b|\bzine\s+shop\b|\bzine\s+fest\b', re.I), 'zine'),
]

# ── Category-level bypass ──────────────────────────────────────────────────
# These category slugs encode medium confirmation in their name — no text
# search needed.
CONFIRMED_CATEGORIES = {
    'global_watercolor_open_call',
    'japan_watercolor_open_call',
    'japan_watercolor_institution',
    'global_watercolor_society',
    'painting_open_call',
}

# ── Buckets already excluded from the API ─────────────────────────────────
# Don't reroute these — they're invisible to the frontend already.
EXCLUDED_BUCKETS = {'reject', 'low_priority'}


def _text_blob(opp: dict) -> str:
    parts = []
    for field in TEXT_FIELDS:
        val = opp.get(field) or ''
        if isinstance(val, str):
            parts.append(val)
    return ' '.join(parts)


def _check(opp: dict) -> tuple[bool, str | None]:
    """Return (passed, signal_label)."""
    # 1. Category bypass
    cat = opp.get('category', '')
    if cat in CONFIRMED_CATEGORIES:
        return True, f'category:{cat}'

    # 2. Already classified as painting by source_medium_classifier
    if opp.get('native_medium') == 'painting':
        return True, 'native_medium:painting'

    # 3. Text search across all relevant fields
    blob = _text_blob(opp)
    for pattern, label in CONFIRM_PATTERNS:
        if pattern.search(blob):
            return True, f'text:{label}'

    return False, None


def main():
    if not os.path.exists(OPP_PATH):
        print(f"File not found: {OPP_PATH}")
        return

    with open(OPP_PATH, encoding='utf-8') as f:
        opps = json.load(f)

    confirmed      = 0
    rerouted       = 0
    skipped        = 0   # already in excluded buckets

    rerouted_lines = []

    for opp in opps:
        passed, signal = _check(opp)

        if passed:
            opp['confirmation_gate_status'] = 'confirmed'
            opp['confirmation_gate_signal'] = signal
            opp.pop('confirmation_gate_note', None)  # clear stale note if re-run
            # Restore original bucket if this entry was previously rerouted by the gate
            prior = opp.pop('pre_gate_bucket', None)
            if prior is not None and opp.get('exclusive_primary_bucket') == 'research_needed':
                opp['exclusive_primary_bucket'] = prior
            confirmed += 1
        else:
            opp['confirmation_gate_status'] = 'needs_confirmation'
            opp['confirmation_gate_signal'] = None
            opp['confirmation_gate_note'] = (
                'No explicit medium confirmation found. '
                'Verify this venue accepts watercolor, painting, illustration, '
                'or works on paper before acting on this opportunity.'
            )

            bucket = opp.get('exclusive_primary_bucket') or ''
            if bucket in EXCLUDED_BUCKETS:
                skipped += 1
            else:
                # Preserve original bucket so re-runs with richer data can restore it
                if 'pre_gate_bucket' not in opp:
                    opp['pre_gate_bucket'] = bucket
                opp['exclusive_primary_bucket'] = 'research_needed'
                rerouted += 1
                name = opp.get('title') or opp.get('name') or '?'
                rerouted_lines.append(
                    f"- **{name}** (was: `{bucket or 'none'}`) — "
                    f"{(opp.get('one_sentence') or '')[:90]}"
                )

    opps.sort(key=lambda x: float(x.get('overall_score', 0) or 0), reverse=True)

    with open(OPP_PATH, 'w', encoding='utf-8') as f:
        json.dump(opps, f, indent=2, ensure_ascii=False)

    # ── Report ────────────────────────────────────────────────────────────
    report = [
        "# Medium Confirmation Gate Report",
        "",
        "An opportunity passes only when one of these signals is present:",
        "watercolor, painting, works on paper, illustration, visual art, fine art,",
        "printmaking, drawing, gouache, artist book, art book, mixed media, zine —",
        "found in accepted_media, name, one_sentence, why_this_fits_short, or other",
        "text fields. Failures route to research_needed; bucket is preserved in",
        "pre_gate_bucket for reversal if richer data is added later.",
        "",
        f"## Summary",
        "",
        f"- **Confirmed:** {confirmed}",
        f"- **Rerouted to research_needed:** {rerouted}",
        f"- **Skipped (already reject/low_priority):** {skipped}",
        f"- **Total:** {len(opps)}",
        "",
        "## Rerouted entries",
        "",
    ] + (rerouted_lines if rerouted_lines else ["_(none)_"])

    Path(REPORT_PATH).parent.mkdir(parents=True, exist_ok=True)
    Path(REPORT_PATH).write_text('\n'.join(report), encoding='utf-8')

    print(f"Confirmed: {confirmed} | Rerouted: {rerouted} | Skipped (excluded): {skipped}")
    print(f"Report: {REPORT_PATH}")


if __name__ == "__main__":
    main()
