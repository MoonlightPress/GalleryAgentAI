# Patch Exceptions

Data patches that **cannot currently be expressed as an engine rule**, per The Data Patch Rule in `CLAUDE.md`. Each entry records: the patch, the file, why it can't be an engine rule yet, and the engine rule that *should* eventually own it.

Goal restated: deleting all JSON and running the pipeline from scratch should produce correct results. Every entry below is a place where that is not yet true.

---

## 2026-07-06 — Overseas-study program suppression (Scott: "no leaving the country")

**Patch:** Added 10 opp_ids to `memory/suppressed_opportunities.json` — every variant of the
Bunka-chō 新進芸術家海外研修制度 / Emerging Artists Overseas Training Program (1-year, 2-year,
special short-term, per-fiscal-year labels, plus the Japanese-cultural-promotion sub-program).

**Why:** Scott's standing preference that she not be shown opportunities requiring relocation
abroad. These are legit, high-scoring Tier-3 programs, so nothing else filters them — they kept
surfacing in the Stretch slot.

**Why not (yet) an engine rule:** suppression is a user-preference decision, so it lives in
app-state (`suppressed_opportunities.json`, honored by `load_opportunities()` at serve time and
union-merged on deploy). It survives pipeline runs while the titles are stable. It is NOT fully
regeneration-proof: a *future* pipeline pass could discover the program under a new title (e.g.
令和10年度…) with a new opp_id that isn't in the list. The eventual engine rule that should own
this: a keyword/relocation classifier that flags opportunities requiring overseas physical
residency (海外研修 / overseas study/training / overseas residency) as suppressed-by-preference —
being careful to NOT catch international *open calls* she can enter remotely from Tokyo, which are
good for her. Not built yet; pending a decision on the broader "no relocation" policy scope.

## 1. `exclusive_primary_bucket` edits on compact opportunities — RESOLVED (2026-06-10)
- **Commits:** `97315944` (shashasha → `publication_targets`), `9b26df47` (one entry).
- **File:** `deploy_data/compact_opportunities.json`
- **Resolution:** the field **is** engine-owned — `engines/exclusive_strategy_bucket_engine.py` (pipeline step) runs `choose_bucket()` over every entry and writes `exclusive_primary_bucket` back onto compact. The earlier "no engine owner" claim was an analysis error. To pin a specific entry, set its **`bucket_override`** field (a value in `BUCKET_ORDER`); `choose_bucket` returns it verbatim, so the routing decision is curated data the engine deterministically honors. shashasha is now pinned this way. Served data == fresh engine run (0 diffs).
- **Caveat for true from-scratch:** `bucket_override` lives on the compact entry, which survives incremental runs (the compactor preserves entries). A literal "delete every JSON including the discovery corpus" rebuild would not carry the override unless it is also seeded upstream — acceptable, because the override is a deliberate human decision that belongs with the curated entry, not something discovery should invent.

## 2. `category` backfill on compact opportunities
- **Commit:** `9b26df47` (added `category` to entries that lacked it: `illustration_prize`, `gallery`, `competition_award`, `institutional`, …)
- **File:** `deploy_data/compact_opportunities.json`
- **Why not an engine rule:** category is assigned upstream at discovery/enrichment. These were legacy entries that predate consistent category assignment; classifying an arbitrary existing entry is an LLM/heuristic judgement, not a deterministic transform.
- **Engine rule it should become:** an enrichment backfill pass that classifies any category-less opportunity (the same classifier discovery uses), run once over the corpus. Deferred: requires the enrichment classifier and a re-run over historical entries.

## 3. Per-opportunity deadline correction
- **Commit:** `9b26df47` (`"1 July 2025" → "Rolling consignment — contact directly"`)
- **File:** `deploy_data/compact_opportunities.json`
- **Why not an engine rule:** this is real-world, opportunity-specific truth (the venue takes rolling consignment, not a one-off 2025 deadline). No engine can derive it without re-scraping the source page.
- **Engine rule it should become:** none possible in general. The durable home is a verification/scrape pass that re-reads the source and updates the deadline — i.e. the Verification layer (the project's stated #1 unfinished system). Until verification covers this venue, it stays a documented patch.

## 4. CRM `why_relevant` justifications
- **Commit:** `e3044ad0`
- **File:** `Memory/contact_memory.json`, `deploy_data/compact_opportunities.json`
- **Why not an engine rule:** the specific per-venue reasoning ("Utrecht is Tokyo's most curated art bookshop…") is curated judgement. An engine could emit generic copy but not this.
- **Engine rule it should become:** `why_it_fits_engine.py` could generate a baseline `why_relevant` for any venue lacking one, leaving curated text in place. Partial conversion only; the curated text remains data.

## 5. Peppercorn seed goals
- **Commit:** `66c9c6c6` (added `goals` with `id`+`done`)
- **File:** `Memory/peppercorn_profile.json`
- **Why not a pipeline concern:** `peppercorn_profile.json` is **app state**, written by `POST /api/peppercorn`, never regenerated by the pipeline. The **schema** (`id`+`done`) is produced by the app on every save, so it is engine(app)-backed. The specific seed goals are example/onboarding data.
- **Status:** acceptable. Not overwritten by the pipeline; schema is app-guaranteed. From-scratch (no file) → `get_peppercorn()` returns sensible defaults.

---

## Files that are source/app-state, NOT pipeline-regenerated (edits here are legitimate)

These have **no pipeline writer** — edits persist and are the canonical input:
- `memory/artist_master_profile.json` — hand-curated artist research (the source of truth the pipeline reads).
- `memory/peppercorn_profile.json` — Peppercorn app state (written by the API).
- `memory/contact_memory.json` — CRM app state (written by the API; priorities normalized at read).
- `memory/submission_log.json`, `memory/exhibition_log.json` — user-logged app state.

Editing these by hand is expected and does not require an engine rule — but a corresponding rule is still needed wherever a *derived/served* field is computed from them (e.g. group-show counts are derived by `_live_career_counts()` / `career_strategy_engine`, not patched).
