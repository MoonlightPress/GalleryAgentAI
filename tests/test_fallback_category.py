import unittest

from api import _fallback_category_from_source_type


class FallbackCategoryFromSourceTypeTests(unittest.TestCase):
    def test_watercolor_source_type_maps_to_watercolor_category(self):
        self.assertEqual(
            _fallback_category_from_source_type("watercolor_open_exhibition"),
            "global_watercolor_open_call",
        )

    def test_gallery_source_type_maps_to_gallery(self):
        self.assertEqual(_fallback_category_from_source_type("illustration_gallery"), "gallery")
        self.assertEqual(_fallback_category_from_source_type("small_gallery"), "gallery")
        self.assertEqual(_fallback_category_from_source_type("gallery_complex"), "gallery")

    def test_society_source_type_maps_to_institutional(self):
        self.assertEqual(_fallback_category_from_source_type("illustration_society"), "institutional")

    def test_unmatched_source_type_defaults_to_global_open_call(self):
        self.assertEqual(_fallback_category_from_source_type("illustration_award"), "global_open_call")
        self.assertEqual(_fallback_category_from_source_type("open_call_index"), "global_open_call")

    def test_missing_source_type_defaults_to_global_open_call(self):
        self.assertEqual(_fallback_category_from_source_type(None), "global_open_call")
        self.assertEqual(_fallback_category_from_source_type(""), "global_open_call")

    def test_watercolor_rule_checked_before_society_rule(self):
        # "watercolor_society" should hit the more specific watercolor rule,
        # not the generic society->institutional rule, given rule order.
        self.assertEqual(
            _fallback_category_from_source_type("watercolor_society"),
            "global_watercolor_open_call",
        )


if __name__ == "__main__":
    unittest.main()
