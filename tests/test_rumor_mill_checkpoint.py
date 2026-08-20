"""Rumor Mill checkpointing — a killed run must keep what it already paid for.

Problem this solves (2026-08-20): rumor_mill saved its search cache and its
bucket moves only AFTER the whole loop finished. The run was killed 167 items
in, and because nothing had been written, 873 Tavily credits and 126 bucket
promotions evaporated — memory/rumor_mill.json was still dated Jul 27 and
opportunity_buckets.json still dated Aug 18. The pipeline-level ledger added in
July resumes at STEP granularity, which does not help inside the single most
expensive step in the pipeline.

Two behaviours fix that:
  * build_checkpoint() — compute the buckets-with-moves-applied from a pristine
    copy of the originals every time, so it can be written repeatedly mid-run
    and the final write is byte-identical to the old save-once behaviour.
  * save_json() — write to a temp file and os.replace() it into place, so a
    checkpoint interrupted mid-write cannot leave a torn JSON file behind.
    Checkpointing writes ~30x more often than before, so this matters more now.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path

from engines.rumor_mill_engine import build_checkpoint, save_json


def item(title, **extra):
    return {"title": title, **extra}


class BuildCheckpointTests(unittest.TestCase):
    def setUp(self):
        self.base = {
            "needs_research": [item("A"), item("B"), item("C")],
            "high_confidence": [item("existing")],
        }
        self.needs = list(self.base["needs_research"])

    def test_moved_item_leaves_needs_research_and_lands_in_target(self):
        out = build_checkpoint(self.base, self.needs, [(item("B"), "high_confidence")])
        self.assertEqual([o["title"] for o in out["needs_research"]], ["A", "C"])
        self.assertEqual(
            [o["title"] for o in out["high_confidence"]], ["existing", "B"]
        )

    def test_no_moves_leaves_buckets_untouched(self):
        out = build_checkpoint(self.base, self.needs, [])
        self.assertEqual(out, self.base)

    def test_repeated_checkpoints_are_idempotent(self):
        """The whole point: called after item 10, 20, 30... the result must be
        identical to calling it once at the end. A cumulative implementation
        that appends to the live dict would duplicate entries on every pass."""
        moved = [(item("B"), "high_confidence")]
        first = build_checkpoint(self.base, self.needs, moved)
        second = build_checkpoint(self.base, self.needs, moved)
        third = build_checkpoint(self.base, self.needs, moved)
        self.assertEqual(first, second)
        self.assertEqual(second, third)

    def test_growing_moves_list_across_checkpoints(self):
        moved = [(item("B"), "high_confidence")]
        build_checkpoint(self.base, self.needs, moved)
        moved.append((item("A"), "low_priority"))
        out = build_checkpoint(self.base, self.needs, moved)
        self.assertEqual([o["title"] for o in out["needs_research"]], ["C"])
        self.assertEqual([o["title"] for o in out["low_priority"]], ["A"])
        self.assertEqual(
            [o["title"] for o in out["high_confidence"]], ["existing", "B"]
        )

    def test_does_not_mutate_the_caller_s_buckets(self):
        """The loop keeps using all_buckets after a checkpoint; corrupting it
        mid-run would make every later checkpoint compound the damage."""
        before = json.dumps(self.base, sort_keys=True)
        build_checkpoint(self.base, self.needs, [(item("B"), "high_confidence")])
        self.assertEqual(json.dumps(self.base, sort_keys=True), before)

    def test_target_bucket_absent_is_created(self):
        out = build_checkpoint(self.base, self.needs, [(item("A"), "brand_new")])
        self.assertEqual([o["title"] for o in out["brand_new"]], ["A"])


class SaveJsonAtomicTests(unittest.TestCase):
    def test_writes_readable_json(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "out.json"
            save_json(p, {"k": "值"})
            self.assertEqual(json.loads(p.read_text(encoding="utf-8")), {"k": "值"})

    def test_leaves_no_temp_file_behind(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "out.json"
            save_json(p, {"k": 1})
            self.assertEqual([f.name for f in Path(d).iterdir()], ["out.json"])

    def test_overwrite_never_exposes_a_truncated_file(self):
        """os.replace is atomic: the old content is readable right up until the
        new content is complete. An in-place write can be caught half-done —
        which is how a torn compact_opportunities.json served an empty site."""
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "out.json"
            save_json(p, {"first": True})
            save_json(p, {"second": True})
            self.assertEqual(json.loads(p.read_text(encoding="utf-8")), {"second": True})

    def test_creates_parent_directory(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "nested" / "deeper" / "out.json"
            save_json(p, [1, 2, 3])
            self.assertEqual(json.loads(p.read_text(encoding="utf-8")), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
