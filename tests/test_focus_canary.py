"""Today's Focus must be checkable without a human reading it.

2026-08-21: her three slots were an expired aggregator listing (linking to the
2025 edition), an exhibition that finished in June, and a gallery-only art fair
she cannot enter. All three had been wrong for an unknown length of time. They
were found because Scott happened to ask "will the good ones be at the top" —
nothing in the system was watching.

Three assertions cover every one of those failures, they cost nothing, and the
weekly job already has a Discord notifier to carry the answer.
"""
import unittest

from engines.focus_canary import audit_focus


def slot(name=None, **kw):
    """Distinct default names: identical names would (correctly) trip the
    duplicate check and mask whatever the test is actually about."""
    return {"name": name or f"Distinct Call {kw.get('id', 'x')}", **kw}


class AuditFocusTests(unittest.TestCase):
    def test_healthy_focus_reports_nothing(self):
        focus = {
            "quick_win":    slot("Consignment venue", id="1"),
            "high_impact":  slot("CSPWC Open Water", id="2", deadline="September 19, 2026"),
            "stretch_goal": slot("ACC Fellowship", id="3", deadline="November 10, 2026"),
        }
        self.assertEqual(audit_focus(focus), [])

    def test_empty_slot_is_reported(self):
        focus = {"quick_win": slot(id="1"), "high_impact": None, "stretch_goal": slot(id="3")}
        problems = audit_focus(focus)
        self.assertTrue(any("high_impact" in p and "empty" in p for p in problems), problems)

    def test_passed_deadline_is_reported(self):
        """The 第113回 日本水彩展 case — a finished exhibition as her top move."""
        focus = {
            "quick_win":    slot(id="1"),
            "high_impact":  slot("113th exhibition", id="2", deadline_past=True),
            "stretch_goal": slot(id="3"),
        }
        problems = audit_focus(focus)
        self.assertTrue(any("high_impact" in p and "deadline" in p for p in problems), problems)

    def test_structurally_ineligible_is_reported(self):
        """The Tokyo Gendai case — gallery applications, she has no gallery."""
        focus = {
            "quick_win":    slot(id="1"),
            "high_impact":  slot(id="2"),
            "stretch_goal": slot("Tokyo Gendai", id="3",
                                 prerequisites=["gallery_representation"]),
        }
        problems = audit_focus(focus)
        self.assertTrue(any("stretch_goal" in p and "eligib" in p for p in problems), problems)

    def test_duplicate_slots_are_reported(self):
        """Three slots showing two things is a silent downgrade to two."""
        focus = {
            "quick_win":    slot("公募―日本の絵画 2026", id="7"),
            "high_impact":  slot("公募 日本の絵画 2026 (Japan Painting Open Call)", id="9"),
            "stretch_goal": slot("Something else", id="3"),
        }
        problems = audit_focus(focus)
        self.assertTrue(any("same opportunity" in p for p in problems), problems)

    def test_several_problems_all_reported(self):
        focus = {
            "quick_win":    None,
            "high_impact":  slot(id="2", deadline_past=True),
            "stretch_goal": slot(id="3", prerequisites=["youth_only"]),
        }
        self.assertEqual(len(audit_focus(focus)), 3)

    def test_buildable_prereqs_do_not_trip_it(self):
        """Exhibition history is what a stretch goal exists to work toward."""
        focus = {
            "quick_win":    slot(id="1"),
            "high_impact":  slot(id="2"),
            "stretch_goal": slot(id="3", prerequisites=["exhibition_credits_5"]),
        }
        self.assertEqual(audit_focus(focus), [])


if __name__ == "__main__":
    unittest.main()
