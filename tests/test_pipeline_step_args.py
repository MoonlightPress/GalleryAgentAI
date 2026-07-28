"""Pipeline steps must be able to carry arguments.

smart_pipeline_runner invoked every script as `python <script>` with no args,
so engine flags were unreachable from inside the pipeline. rumor_mill_engine
has had a --max cap all along; it could not be applied where it mattered, and
on 2026-07-27 the uncapped step consumed ~1,650 of the run's 3,042 Tavily
credits while producing zero new opportunities.

A PIPELINE entry may now read "rumor_mill_engine.py --max 300".
"""

import unittest

from smart_pipeline_runner import parse_step, find_script


class ParseStepTests(unittest.TestCase):

    def test_bare_script_name_has_no_args(self):
        script, args = parse_step("career_path_ranker.py")
        self.assertEqual(script, "career_path_ranker.py")
        self.assertEqual(args, [])

    def test_script_with_flag_and_value_is_split(self):
        script, args = parse_step("rumor_mill_engine.py --max 300")
        self.assertEqual(script, "rumor_mill_engine.py")
        self.assertEqual(args, ["--max", "300"])

    def test_multiple_flags_are_preserved_in_order(self):
        script, args = parse_step("x.py --max 300 --cache-days 30")
        self.assertEqual(args, ["--max", "300", "--cache-days", "30"])

    def test_surrounding_whitespace_is_ignored(self):
        script, args = parse_step("  rumor_mill_engine.py   --max  300  ")
        self.assertEqual(script, "rumor_mill_engine.py")
        self.assertEqual(args, ["--max", "300"])

    def test_resolver_still_finds_a_script_that_carried_args(self):
        """The optional-script check and path resolution must use the script
        name, never the whole entry string."""
        script, _ = parse_step("rumor_mill_engine.py --max 300")
        self.assertIsNotNone(find_script(script))


if __name__ == "__main__":
    unittest.main()
