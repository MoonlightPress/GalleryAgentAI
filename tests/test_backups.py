import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from engines.backups import backup_filename, snapshot


NOW = datetime(2026, 6, 25, 14, 30, 0, tzinfo=timezone.utc)


class BackupFilenameTests(unittest.TestCase):
    def test_inserts_utc_timestamp_before_extension(self):
        self.assertEqual(
            backup_filename("peppercorn_profile.json", NOW),
            "peppercorn_profile.20260625T143000Z.json",
        )

    def test_name_without_extension(self):
        self.assertEqual(backup_filename("data", NOW), "data.20260625T143000Z")

    def test_only_the_final_extension_is_split(self):
        self.assertEqual(
            backup_filename("a.b.json", NOW), "a.b.20260625T143000Z.json"
        )


class SnapshotTests(unittest.TestCase):
    def test_creates_timestamped_copy_with_identical_contents(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            src = d / "peppercorn_profile.json"
            src.write_text('{"artist_statement": "hello"}', encoding="utf-8")
            backups = d / "backups"

            dest = snapshot(src, backups, NOW)

            self.assertIsNotNone(dest)
            self.assertTrue(dest.exists())
            self.assertEqual(dest.name, "peppercorn_profile.20260625T143000Z.json")
            self.assertEqual(
                json.loads(dest.read_text(encoding="utf-8")),
                {"artist_statement": "hello"},
            )
            # original is left in place
            self.assertTrue(src.exists())

    def test_missing_source_returns_none_and_does_not_raise(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            dest = snapshot(d / "nope.json", d / "backups", NOW)
            self.assertIsNone(dest)

    def test_backups_dir_is_created_if_absent(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            src = d / "f.json"
            src.write_text("{}", encoding="utf-8")
            backups = d / "deep" / "backups"
            dest = snapshot(src, backups, NOW)
            self.assertTrue(dest.exists())
            self.assertTrue(backups.is_dir())


if __name__ == "__main__":
    unittest.main()
