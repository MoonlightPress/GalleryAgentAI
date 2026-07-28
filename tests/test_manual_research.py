"""Manual research ingestion — the offline (zero-Tavily) fact source.

Context: the 2026-07-27 full pipeline run exhausted the Tavily quota partway
through rumor_mill_engine, leaving 135 of 148 newly discovered opportunities
flagged needs_research with no deadline, fee or submission_url. This engine
lets verified facts — read off the opportunity's real page rather than a search
snippet — be applied through the same slot rumor_mill fills.

Because these records are hand-authored, the validator is the safety boundary:
its whole job is to refuse anything unprovenanced, malformed or hallucinated
BEFORE it can touch the opportunity data.
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from engines.manual_research_engine import validate_record, apply_records, run


GOOD = {
    "title": "The Homiens Art Prize ($12,000 Annually)",
    "source_url": "https://homiens.com/homiens-art-prize/",
    "verified_at": "2026-07-27",
    "found": {"fee": "$35", "submission_url": "https://homiens.com/homiens-art-prize/"},
}


class ValidateRecordTests(unittest.TestCase):

    def test_accepts_a_well_formed_provenanced_record(self):
        ok, reason = validate_record(GOOD)
        self.assertTrue(ok, reason)

    def test_rejects_record_with_no_source_url(self):
        """Provenance is mandatory — a fact with no page behind it is a guess."""
        rec = {**GOOD}
        del rec["source_url"]
        ok, reason = validate_record(rec)
        self.assertFalse(ok)
        self.assertIn("source_url", reason)

    def test_rejects_non_http_source_url(self):
        rec = {**GOOD, "source_url": "not-a-url"}
        ok, reason = validate_record(rec)
        self.assertFalse(ok)
        self.assertIn("source_url", reason)

    def test_rejects_record_carrying_no_facts(self):
        rec = {**GOOD, "found": {}}
        ok, reason = validate_record(rec)
        self.assertFalse(ok)
        self.assertIn("no facts", reason)

    def test_rejects_placeholder_values_that_look_like_data(self):
        """"unknown"/"N/A"/"TBD" are how a model says "I don't know" — they must
        never reach the card as though they were researched facts."""
        for junk in ("unknown", "N/A", "n/a", "TBD", "tbd", "none", "-", ""):
            rec = {**GOOD, "found": {"fee": junk}}
            ok, reason = validate_record(rec)
            self.assertFalse(ok, f"accepted placeholder fee={junk!r}")

    def test_rejects_unparseable_deadline(self):
        rec = {**GOOD, "found": {"deadline": "sometime next spring"}}
        ok, reason = validate_record(rec)
        self.assertFalse(ok)
        self.assertIn("deadline", reason)

    def test_accepts_real_deadline_formats_including_japanese(self):
        for good_date in ("2026-08-04", "2026年08月31日", "August 4, 2026", "2026-08-04 18:00"):
            rec = {**GOOD, "found": {"deadline": good_date}}
            ok, reason = validate_record(rec)
            self.assertTrue(ok, f"rejected real deadline {good_date!r}: {reason}")

    def test_rejects_non_http_submission_url(self):
        rec = {**GOOD, "found": {"submission_url": "javascript:alert(1)"}}
        ok, reason = validate_record(rec)
        self.assertFalse(ok)
        self.assertIn("submission_url", reason)

    def test_rejects_unknown_field_names(self):
        """Typo'd keys would silently do nothing — fail loudly instead."""
        rec = {**GOOD, "found": {"deadlne": "2026-08-04"}}
        ok, reason = validate_record(rec)
        self.assertFalse(ok)
        self.assertIn("deadlne", reason)


class ApplyRecordsTests(unittest.TestCase):

    def test_fills_empty_field_on_matching_opportunity(self):
        opps = [{"name": GOOD["title"], "fee": ""}]
        applied, skipped = apply_records(opps, [GOOD])
        self.assertEqual(opps[0]["fee"], "$35")
        self.assertEqual(len(applied), 1)

    def test_never_overwrites_existing_data_by_default(self):
        """A hand-authored record must not clobber what the pipeline found.
        Sibling facts on the same record still apply — only the already-populated
        field is held back."""
        opps = [{"name": GOOD["title"], "fee": "$30 early bird"}]
        applied, skipped = apply_records(opps, [GOOD])
        self.assertEqual(opps[0]["fee"], "$30 early bird")
        self.assertNotIn("fee", applied[0][1])
        self.assertIn("submission_url", applied[0][1])

    def test_record_is_skipped_when_every_field_is_already_populated(self):
        rec = {**GOOD, "found": {"fee": "$35"}}
        opps = [{"name": GOOD["title"], "fee": "$30 early bird"}]
        applied, skipped = apply_records(opps, [rec])
        self.assertEqual(opps[0]["fee"], "$30 early bird")
        self.assertEqual(len(applied), 0)
        self.assertIn("already populated", skipped[0][1])

    def test_overwrites_only_when_record_opts_in(self):
        """The $12 -> $35 correction needs an explicit, auditable opt-in."""
        rec = {**GOOD, "override": True}
        opps = [{"name": GOOD["title"], "fee": "$12"}]
        applied, skipped = apply_records(opps, [rec])
        self.assertEqual(opps[0]["fee"], "$35")
        self.assertEqual(len(applied), 1)

    def test_skips_record_whose_title_matches_nothing(self):
        opps = [{"name": "Some Other Call"}]
        applied, skipped = apply_records(opps, [GOOD])
        self.assertEqual(len(applied), 0)
        self.assertEqual(len(skipped), 1)

    def test_invalid_records_are_skipped_not_applied(self):
        bad = {**GOOD, "found": {"fee": "unknown"}}
        opps = [{"name": GOOD["title"], "fee": ""}]
        applied, skipped = apply_records(opps, [bad])
        self.assertEqual(opps[0]["fee"], "")
        self.assertEqual(len(applied), 0)

    def test_stamps_provenance_onto_the_opportunity(self):
        """Every applied fact must be traceable back to the page it came from."""
        opps = [{"name": GOOD["title"], "fee": ""}]
        apply_records(opps, [GOOD])
        self.assertEqual(opps[0]["manual_research_source"], GOOD["source_url"])
        self.assertEqual(opps[0]["manual_research_at"], "2026-07-27")


RETRACT = {
    "title": "第110回記念 二科美術展覧会",
    "source_url": "https://www.nact.jp/exhibition_public",
    "verified_at": "2026-07-28",
    "retract": {"fee": "一般 1,400円"},
    "reason": "stored fee is the visitor admission price, not the 出品料",
}


class RetractionTests(unittest.TestCase):
    """A record may WITHDRAW a wrong value as well as assert a right one.
    Found 2026-07-28: seven entries store the visitor admission price as her
    entry fee. The extractor only writes when the fee is missing, so it can
    never correct them; assert-only records can't either (the validator
    rightly refuses empty values). Retraction is the designed way to remove
    misinformation — and it must name the exact bad value it is removing, so
    a stale retraction can't delete a value that was since corrected."""

    def test_retraction_clears_the_named_wrong_value(self):
        opps = [{"name": RETRACT["title"], "fee": "一般 1,400円"}]
        applied, skipped = apply_records(opps, [RETRACT])
        self.assertEqual(opps[0]["fee"], "")
        self.assertEqual(len(applied), 1)

    def test_retraction_requires_the_current_value_to_match(self):
        """If the pipeline has since found a different (presumably real) fee,
        the stale retraction must not delete it."""
        opps = [{"name": RETRACT["title"], "fee": "出品料 12,000円"}]
        applied, skipped = apply_records(opps, [RETRACT])
        self.assertEqual(opps[0]["fee"], "出品料 12,000円")
        self.assertEqual(len(applied), 0)
        self.assertIn("no longer matches", skipped[0][1])

    def test_retraction_requires_provenance_and_reason(self):
        rec = {k: v for k, v in RETRACT.items() if k != "reason"}
        ok, why = validate_record(rec)
        self.assertFalse(ok)
        self.assertIn("reason", why)

    def test_retraction_of_unknown_field_is_rejected(self):
        rec = {**RETRACT, "retract": {"admision": "x"}}
        ok, why = validate_record(rec)
        self.assertFalse(ok)
        self.assertIn("admision", why)

    def test_record_may_retract_and_assert_together(self):
        """The common correction shape: remove the admission price AND supply
        the real submission fee in one auditable record."""
        rec = {**RETRACT, "found": {"fee": "出品料 12,000円"}}
        opps = [{"name": RETRACT["title"], "fee": "一般 1,400円"}]
        applied, skipped = apply_records(opps, [rec])
        self.assertEqual(opps[0]["fee"], "出品料 12,000円")

    def test_pure_retraction_passes_validation(self):
        ok, why = validate_record(RETRACT)
        self.assertTrue(ok, why)

    def test_completed_retraction_reports_itself_honestly_on_rerun(self):
        """Second run after a successful retraction: the field is empty, so the
        skip reason must say the retraction is done — not claim the field is
        'already populated', which is the opposite of the truth."""
        opps = [{"name": RETRACT["title"], "fee": ""}]
        applied, skipped = apply_records(opps, [RETRACT])
        self.assertEqual(len(applied), 0)
        self.assertIn("already retracted", skipped[0][1])


class FeeAliasTests(unittest.TestCase):
    """fee/fees is a split-field pair (audit 2026-07-06): different-era engines
    write different keys, and the serving accessor _fees_value prefers "fees"
    even when it holds the placeholder "Unknown". Records speak of "fee"; the
    engine must handle whichever spelling the entry actually carries — 5 of the
    7 admission-price entries store the bad value in "fees", where a fee-only
    retraction would silently miss it."""

    def test_retraction_clears_a_fees_side_bad_value(self):
        rec = {"title": "X", "source_url": "https://nact.jp/e", "verified_at": "2026-07-28",
               "retract": {"fee": "一般 1,400円"}, "reason": "visitor admission"}
        opps = [{"name": "X", "fees": "一般 1,400円"}]
        applied, _ = apply_records(opps, [rec])
        self.assertEqual(opps[0]["fees"], "")
        self.assertEqual(len(applied), 1)

    def test_retraction_also_clears_placeholder_siblings(self):
        """COMITIA: fee holds the bad value, fees holds "Unknown". After the
        retraction neither field may keep feeding the serving accessor junk."""
        rec = {"title": "X", "source_url": "https://c.jp/", "verified_at": "2026-07-28",
               "retract": {"fee": "1,000 yen (visitor)"}, "reason": "visitor ticket"}
        opps = [{"name": "X", "fee": "1,000 yen (visitor)", "fees": "Unknown"}]
        apply_records(opps, [rec])
        self.assertEqual(opps[0]["fee"], "")
        self.assertEqual(opps[0]["fees"], "")

    def test_assertion_writes_both_spellings(self):
        """_fees_value prefers "fees"; rumor_mill writes "fee". Writing one
        spelling leaves some reader seeing stale data — write the pair."""
        opps = [{"name": GOOD["title"], "fee": "", "fees": ""}]
        apply_records(opps, [GOOD])
        self.assertEqual(opps[0]["fee"], "$35")
        self.assertEqual(opps[0]["fees"], "$35")

    def test_placeholder_fees_does_not_block_a_fill(self):
        opps = [{"name": GOOD["title"], "fees": "Unknown"}]
        applied, _ = apply_records(opps, [GOOD])
        self.assertEqual(opps[0]["fees"], "$35")

    def test_real_fees_value_still_blocks_a_fill_without_override(self):
        rec = {**GOOD, "found": {"fee": "$35"}}
        opps = [{"name": GOOD["title"], "fees": "$30 early bird"}]
        applied, _ = apply_records(opps, [rec])
        self.assertEqual(opps[0]["fees"], "$30 early bird")
        self.assertEqual(len(applied), 0)


class RunFileTests(unittest.TestCase):
    """The engine runs as a pipeline step, so a missing or malformed source file
    must degrade to a no-op — never abort a 101-step run."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.research = Path(self.tmp) / "manual_research.json"
        self.compact = Path(self.tmp) / "compact.json"
        self.compact.write_text(
            json.dumps([{"name": GOOD["title"], "fee": ""}]), encoding="utf-8"
        )

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_missing_research_file_is_a_clean_no_op(self):
        applied, skipped = run(self.research, self.compact)
        self.assertEqual(applied, [])
        self.assertEqual(json.loads(self.compact.read_text(encoding="utf-8"))[0]["fee"], "")

    def test_malformed_research_file_does_not_raise(self):
        self.research.write_text("{ not json", encoding="utf-8")
        applied, skipped = run(self.research, self.compact)
        self.assertEqual(applied, [])

    def test_valid_records_are_written_back_to_disk(self):
        self.research.write_text(json.dumps({"records": [GOOD]}), encoding="utf-8")
        applied, skipped = run(self.research, self.compact)
        saved = json.loads(self.compact.read_text(encoding="utf-8"))
        self.assertEqual(saved[0]["fee"], "$35")
        self.assertEqual(saved[0]["manual_research_source"], GOOD["source_url"])
        self.assertEqual(len(applied), 1)

    def test_nothing_is_written_when_no_record_applies(self):
        """Must not rewrite the file (and churn git) for a no-op run."""
        self.research.write_text(json.dumps({"records": []}), encoding="utf-8")
        before = self.compact.read_text(encoding="utf-8")
        run(self.research, self.compact)
        self.assertEqual(self.compact.read_text(encoding="utf-8"), before)


if __name__ == "__main__":
    unittest.main()
