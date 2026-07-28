"""opp_strategy_translation_engine — Message Batches conversion.

Second-largest Claude spend of a full run (relationship_note /
submission_strategy / recommended_body / quick_action -> zh + ja for every
entry). Same design contract as the content engine: results are applied by
EXACT SOURCE STRING (apply_translations' table), never by chunk position, so
a batch resumed on a later run applies safely against shifted data. Offline
fakes only — unit tests never spend credits.
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from engines.opp_strategy_translation_engine import (
    build_requests, parse_table_text, run_batched,
)


def _msg_result(custom_id, payload):
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
    def __init__(self, status_sequence=("ended",), results_payload=None):
        self.created_with = None
        self.create_calls = 0
        self._statuses = list(status_sequence)
        self._results = results_payload or []

    def create(self, requests):
        self.create_calls += 1
        self.created_with = requests
        return SimpleNamespace(id="msgbatch_strat1", processing_status="in_progress")

    def retrieve(self, batch_id):
        status = self._statuses.pop(0) if len(self._statuses) > 1 else self._statuses[0]
        return SimpleNamespace(id=batch_id, processing_status=status)

    def results(self, batch_id):
        return iter(self._results)


class FakeClient:
    def __init__(self, batches):
        self.messages = SimpleNamespace(batches=batches)


class BuildRequestsTests(unittest.TestCase):

    def test_chunks_of_sixteen_with_stable_custom_ids(self):
        reqs = build_requests([f"string {i}" for i in range(20)])
        self.assertEqual([r["custom_id"] for r in reqs],
                         ["strategy-chunk-0000", "strategy-chunk-0001"])

    def test_prompt_carries_the_strings(self):
        req = build_requests(["Reach out to the curator."])[0]
        self.assertIn("Reach out to the curator.", req["params"]["messages"][0]["content"])


class ParseTableTests(unittest.TestCase):

    def test_plain_object(self):
        self.assertEqual(parse_table_text('{"a": {"zh": "甲", "ja": "ア"}}'),
                         {"a": {"zh": "甲", "ja": "ア"}})

    def test_fenced_object_with_prose(self):
        raw = 'Sure:\n```json\n{"a": {"zh": "甲", "ja": "ア"}}\n```'
        self.assertEqual(parse_table_text(raw), {"a": {"zh": "甲", "ja": "ア"}})


class RunBatchedTests(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.compact = self.tmp / "compact.json"
        self.pending_file = self.tmp / "pending.json"
        self.opps = [{"id": "opp-1",
                      "submission_strategy": "Reach out to the curator."}]
        self.compact.write_text(json.dumps(self.opps, ensure_ascii=False), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def payload(self):
        return {"Reach out to the curator.": {"zh": "联系策展人。", "ja": "キュレーターに連絡。"}}

    def test_happy_path_translates_and_saves(self):
        fake = FakeBatches(results_payload=[_msg_result("strategy-chunk-0000", self.payload())])
        run_batched(FakeClient(fake), compact_path=self.compact,
                    pending_path=self.pending_file, poll_interval=0, max_wait=10)
        out = json.loads(self.compact.read_text(encoding="utf-8"))
        self.assertEqual(out[0]["submission_strategy_zh"], "联系策展人。")
        self.assertEqual(out[0]["submission_strategy_ja"], "キュレーターに連絡。")
        self.assertFalse(self.pending_file.exists())

    def test_pending_batch_is_fetched_instead_of_resubmitting(self):
        self.pending_file.write_text(json.dumps({"batch_id": "msgbatch_old"}), encoding="utf-8")
        fake = FakeBatches(results_payload=[_msg_result("strategy-chunk-0000", self.payload())])
        run_batched(FakeClient(fake), compact_path=self.compact,
                    pending_path=self.pending_file, poll_interval=0, max_wait=10)
        self.assertEqual(fake.create_calls, 0)
        out = json.loads(self.compact.read_text(encoding="utf-8"))
        self.assertEqual(out[0]["submission_strategy_zh"], "联系策展人。")

    def test_timeout_keeps_pending_file(self):
        fake = FakeBatches(status_sequence=("in_progress",))
        run_batched(FakeClient(fake), compact_path=self.compact,
                    pending_path=self.pending_file, poll_interval=0, max_wait=0)
        self.assertTrue(self.pending_file.exists())

    def test_nothing_pending_is_a_clean_no_op(self):
        self.opps[0]["submission_strategy_zh"] = "done"
        self.opps[0]["submission_strategy_ja"] = "done"
        self.compact.write_text(json.dumps(self.opps, ensure_ascii=False), encoding="utf-8")
        fake = FakeBatches()
        run_batched(FakeClient(fake), compact_path=self.compact,
                    pending_path=self.pending_file, poll_interval=0, max_wait=10)
        self.assertEqual(fake.create_calls, 0)


if __name__ == "__main__":
    unittest.main()
