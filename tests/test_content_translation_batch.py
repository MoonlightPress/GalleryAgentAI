"""content_translation_engine — Message Batches conversion.

Why: translations are the dominant Claude spend of a full pipeline run (every
new opportunity × 8 fields × 2 languages on Sonnet), Scott tops up $5 at a
time, and the Aug 3 run is projected to find ~3-4x the new entries of the run
that just drained the balance. The Batches API halves the cost with zero
quality tradeoff — translations run at the end of a monthly unattended
pipeline, so latency is irrelevant.

Design constraints proven here:
  - Requests are built deterministically from the pending list (chunks of 8,
    stable custom_ids, same model/system/prompt as the sync path).
  - Results are applied BY ITEM ID (apply_batch), never by chunk position —
    so results fetched on a later run, against a shifted opportunity list,
    still land on the right entries.
  - The submitted batch id is persisted BEFORE polling; if the run dies or
    times out, the next run fetches that batch's results instead of paying
    for the same translations twice.
  - All tests run offline against a fake client — the real balance is $0
    right now, and unit tests must never spend credits anyway.
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from engines.content_translation_engine import (
    build_requests, parse_response_text, run_batched, needs_translation, MODEL,
)


def _msg_result(custom_id, payload):
    """Shape of one entry from client.messages.batches.results()."""
    return SimpleNamespace(
        custom_id=custom_id,
        result=SimpleNamespace(
            type="succeeded",
            message=SimpleNamespace(
                content=[SimpleNamespace(type="text", text=json.dumps(payload, ensure_ascii=False))]
            ),
        ),
    )


class FakeBatches:
    def __init__(self, status_sequence=("ended",), results_payload=None, existing=None):
        self.created_with = None
        self.create_calls = 0
        self._statuses = list(status_sequence)
        self._results = results_payload or []
        self._existing = existing or {}

    def create(self, requests):
        self.create_calls += 1
        self.created_with = requests
        return SimpleNamespace(id="msgbatch_test1", processing_status="in_progress")

    def retrieve(self, batch_id):
        status = self._statuses.pop(0) if len(self._statuses) > 1 else self._statuses[0]
        return SimpleNamespace(id=batch_id, processing_status=status)

    def results(self, batch_id):
        return iter(self._results)


class FakeClient:
    def __init__(self, batches):
        self.messages = SimpleNamespace(batches=batches)


TR = {  # one translated record, keyed back by id
    "id": "opp-1", "name_zh": "翻译名", "one_sentence_zh": "一句话",
    "why_it_fits_zh": "为什么", "three_bullets_zh": ["一", "二"],
    "name_ja": "訳名", "one_sentence_ja": "一文",
    "why_it_fits_ja": "理由", "three_bullets_ja": ["一", "二"],
}


class NeedsTranslationTests(unittest.TestCase):
    """Money-leak regression (2026-07-28): needs_translation demanded all 8
    target fields, but an entry whose SOURCE three_bullets is empty can never
    earn three_bullets_zh/_ja — apply_batch skips empty values — so 402 of 801
    live entries were re-submitted to Sonnet on EVERY pipeline run with nothing
    left to translate. A field only 'needs translation' if its source exists."""

    DONE = {"name_zh": "n", "one_sentence_zh": "s", "why_it_fits_zh": "w",
            "name_ja": "n", "one_sentence_ja": "s", "why_it_fits_ja": "w"}

    def test_empty_source_bullets_do_not_keep_an_entry_pending(self):
        opp = {"name": "Call", "one_sentence": "s", "why_it_fits": "w",
               "three_bullets": [], **self.DONE}
        self.assertFalse(needs_translation(opp))

    def test_missing_source_why_does_not_keep_an_entry_pending(self):
        opp = {"name": "Call", "one_sentence": "s", "three_bullets": ["a"],
               **self.DONE, "three_bullets_zh": ["a"], "three_bullets_ja": ["a"]}
        del opp["why_it_fits_zh"]; del opp["why_it_fits_ja"]
        self.assertFalse(needs_translation(opp))

    def test_untranslated_entry_with_full_source_is_pending(self):
        opp = {"name": "Call", "one_sentence": "s", "why_it_fits": "w",
               "three_bullets": ["a"]}
        self.assertTrue(needs_translation(opp))

    def test_partially_translated_entry_is_pending(self):
        opp = {"name": "Call", "one_sentence": "s", "why_it_fits": "w",
               "three_bullets": ["a"], **self.DONE}  # bullets not yet translated
        self.assertTrue(needs_translation(opp))


class BuildRequestsTests(unittest.TestCase):

    def pending(self, n):
        return [{"id": f"opp-{i}", "name": f"Call {i}", "one_sentence": "s",
                 "three_bullets": ["a"]} for i in range(n)]

    def test_chunks_of_eight_with_stable_custom_ids(self):
        reqs = build_requests(self.pending(20))
        self.assertEqual(len(reqs), 3)
        self.assertEqual([r["custom_id"] for r in reqs],
                         ["translate-chunk-0000", "translate-chunk-0001", "translate-chunk-0002"])

    def test_params_carry_model_system_and_prompt(self):
        req = build_requests(self.pending(1))[0]
        self.assertEqual(req["params"]["model"], MODEL)
        self.assertIn("translator", req["params"]["system"].lower())
        self.assertIn("opp-0", req["params"]["messages"][0]["content"])

    def test_empty_pending_builds_no_requests(self):
        self.assertEqual(build_requests([]), [])


class ParseResponseTests(unittest.TestCase):

    def test_plain_json_array(self):
        self.assertEqual(parse_response_text('[{"id": "x"}]'), [{"id": "x"}])

    def test_markdown_fenced_json(self):
        raw = '```json\n[{"id": "x"}]\n```'
        self.assertEqual(parse_response_text(raw), [{"id": "x"}])

    def test_surrounding_prose_is_stripped(self):
        raw = 'Here you go:\n[{"id": "x"}]\nHope that helps!'
        self.assertEqual(parse_response_text(raw), [{"id": "x"}])

    def test_mildly_broken_json_is_repaired(self):
        raw = '[{"id": "x",}]'  # trailing comma
        self.assertEqual(parse_response_text(raw), [{"id": "x"}])


class RunBatchedTests(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.compact = self.tmp / "compact.json"
        self.pending_file = self.tmp / "pending_batch.json"
        self.opps = [
            {"id": "opp-1", "name": "Call 1", "one_sentence": "s", "three_bullets": ["a"]},
            {"id": "opp-2", "name": "Call 2", "one_sentence": "s", "three_bullets": ["a"],
             # already fully translated — must not be re-submitted
             **{f: "done" for f in ("name_zh", "one_sentence_zh", "why_it_fits_zh",
                                     "name_ja", "one_sentence_ja", "why_it_fits_ja")},
             "three_bullets_zh": ["done"], "three_bullets_ja": ["done"]},
        ]
        self.compact.write_text(json.dumps(self.opps, ensure_ascii=False), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def saved(self):
        return json.loads(self.compact.read_text(encoding="utf-8"))

    def test_happy_path_translates_and_saves(self):
        fake = FakeBatches(results_payload=[_msg_result("translate-chunk-0000", [TR])])
        run_batched(FakeClient(fake), compact_path=self.compact,
                    pending_path=self.pending_file, poll_interval=0, max_wait=10)
        out = self.saved()
        self.assertEqual(out[0]["name_zh"], "翻译名")
        self.assertEqual(out[0]["three_bullets_ja"], ["一", "二"])

    def test_already_translated_entries_are_not_submitted(self):
        fake = FakeBatches(results_payload=[_msg_result("translate-chunk-0000", [TR])])
        run_batched(FakeClient(fake), compact_path=self.compact,
                    pending_path=self.pending_file, poll_interval=0, max_wait=10)
        submitted = fake.created_with
        self.assertEqual(len(submitted), 1)  # one chunk, containing only opp-1
        self.assertNotIn("opp-2", submitted[0]["params"]["messages"][0]["content"])

    def test_batch_id_is_persisted_before_polling(self):
        """If the process dies mid-poll, the paid-for batch must be findable."""
        class DiesOnRetrieve(FakeBatches):
            def retrieve(self, batch_id):
                raise KeyboardInterrupt

        fake = DiesOnRetrieve()
        with self.assertRaises(KeyboardInterrupt):
            run_batched(FakeClient(fake), compact_path=self.compact,
                        pending_path=self.pending_file, poll_interval=0, max_wait=10)
        pend = json.loads(self.pending_file.read_text(encoding="utf-8"))
        self.assertEqual(pend["batch_id"], "msgbatch_test1")

    def test_pending_batch_is_fetched_instead_of_resubmitting(self):
        """A prior run's unfetched batch = translations already paid for.
        The next run must fetch those results, not create a new batch."""
        self.pending_file.write_text(json.dumps({"batch_id": "msgbatch_old"}), encoding="utf-8")
        fake = FakeBatches(results_payload=[_msg_result("translate-chunk-0000", [TR])])
        run_batched(FakeClient(fake), compact_path=self.compact,
                    pending_path=self.pending_file, poll_interval=0, max_wait=10)
        self.assertEqual(fake.create_calls, 0)
        self.assertEqual(self.saved()[0]["name_zh"], "翻译名")

    def test_pending_file_is_cleared_after_successful_apply(self):
        fake = FakeBatches(results_payload=[_msg_result("translate-chunk-0000", [TR])])
        run_batched(FakeClient(fake), compact_path=self.compact,
                    pending_path=self.pending_file, poll_interval=0, max_wait=10)
        self.assertFalse(self.pending_file.exists())

    def test_timeout_keeps_pending_file_and_returns_without_error(self):
        """An unattended pipeline must not abort the remaining steps because a
        batch is slow — and must not lose the batch id."""
        fake = FakeBatches(status_sequence=("in_progress",))
        run_batched(FakeClient(fake), compact_path=self.compact,
                    pending_path=self.pending_file, poll_interval=0, max_wait=0)
        self.assertTrue(self.pending_file.exists())
        # nothing applied, file untouched semantically
        self.assertNotIn("name_zh", self.saved()[0])

    def test_nothing_pending_is_a_clean_no_op(self):
        for f in ("name_zh", "one_sentence_zh", "why_it_fits_zh",
                  "name_ja", "one_sentence_ja", "why_it_fits_ja"):
            self.opps[0][f] = "done"
        self.opps[0]["three_bullets_zh"] = ["done"]
        self.opps[0]["three_bullets_ja"] = ["done"]
        self.compact.write_text(json.dumps(self.opps, ensure_ascii=False), encoding="utf-8")
        fake = FakeBatches()
        run_batched(FakeClient(fake), compact_path=self.compact,
                    pending_path=self.pending_file, poll_interval=0, max_wait=10)
        self.assertEqual(fake.create_calls, 0)


if __name__ == "__main__":
    unittest.main()
