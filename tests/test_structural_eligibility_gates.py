"""Two watercolor-layer gaps found 2026-07-28 while re-bucketing.

1. 海と山と写真公募展 — a photography open call with 写真 in its TITLE — sat in
   competitions_awards, because the photo gates check native_medium ("unknown"
   here) and category ("competition_award" here), never the title. CLAUDE.md:
   photography floods painting; the layer must not be weakened — an entry that
   says photo in its own name is the easiest possible case.

2. 第五届威尼斯国际青少年美术大赛 — a YOUTH (青少年 = minors) competition served
   to a 26-year-old. Same structural class as organizations_only: she will
   never be a minor again.

Deliberately narrow:
  - 写真 with painting evidence alongside (絵画と写真, mixed calls) stays.
  - "children's illustration" is a GENRE she works in, not a participant
    restriction — must not match.
  - Student calls must not match: she IS a student (Scott, 2026-06-19 — mark
    student calls, don't filter them).
"""

import unittest

from engines.exclusive_strategy_bucket_engine import choose_bucket
from engines.prerequisite_detection_engine import detect_from_text


class PhotoTitleGateTests(unittest.TestCase):

    BASE = {"category": "competition_award", "overall_score": 7.0,
            "native_medium": "unknown"}

    def test_photo_open_call_named_in_title_is_rejected(self):
        opp = {**self.BASE, "title": "海と山と写真公募展"}
        self.assertEqual(choose_bucket(opp), "reject")

    def test_english_photo_contest_title_is_rejected(self):
        opp = {**self.BASE, "title": "Ocean Photography Contest 2026"}
        self.assertEqual(choose_bucket(opp), "reject")

    def test_mixed_media_call_mentioning_photo_survives(self):
        for title in ("絵画・写真・イラスト公募展", "Art & Photography Open Call — painting welcome"):
            opp = {**self.BASE, "title": title}
            self.assertNotEqual(choose_bucket(opp), "reject", title)

    def test_photo_title_with_watercolor_accepted_media_survives(self):
        opp = {**self.BASE, "title": "写真と芸術祭", "accepted_media": "watercolor, photography"}
        self.assertNotEqual(choose_bucket(opp), "reject")

    def test_non_photo_competition_is_untouched(self):
        opp = {**self.BASE, "title": "全国水彩画コンクール"}
        self.assertEqual(choose_bucket(opp), "competitions_awards")


class YouthOnlyTests(unittest.TestCase):

    def test_youth_competition_phrasings_are_detected(self):
        for text in (
            "威尼斯国际青少年美术大赛",
            "全国青少年絵画コンクール 応募は18歳以下",
            "international youth art competition ages 6-17",
            "open to artists under 18",
        ):
            self.assertIn("youth_only", detect_from_text(text.lower()), text)

    def test_childrens_illustration_genre_is_not_flagged(self):
        """Children's illustration is work FOR children — her genre, not a
        participant age limit."""
        for text in (
            "chinese excellence in children's illustration 2026",
            "picture book illustration for young readers",
            "children's book illustration prize",
        ):
            self.assertNotIn("youth_only", detect_from_text(text), text)

    def test_student_calls_are_not_flagged(self):
        """She IS a student — student calls are explicitly kept."""
        for text in (
            "学生限定 アートコンペ 2026",
            "student art competition — currently enrolled artists",
            "美大生 公募展",
        ):
            self.assertNotIn("youth_only", detect_from_text(text.lower()), text)

    def test_youth_only_routes_to_reject(self):
        opp = {"title": "X", "category": "competition_award", "overall_score": 8.0,
               "prerequisites": ["youth_only"]}
        self.assertEqual(choose_bucket(opp), "reject")


if __name__ == "__main__":
    unittest.main()
