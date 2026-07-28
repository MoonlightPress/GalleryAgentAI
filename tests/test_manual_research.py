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
