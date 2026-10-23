import unittest
from bookclub.errors import DomainError
from bookclub.status_transitions import transition_status


class StatusTransitionTests(unittest.TestCase):
    def test_all_status_pairs(self):
        allowed = {("draft", "published"), ("draft", "cancelled"),
                   ("published", "completed"), ("published", "cancelled")}
        for current in ("draft", "published", "completed", "cancelled"):
            for target in ("draft", "published", "completed", "cancelled"):
                with self.subTest(current=current, target=target):
                    if (current, target) in allowed:
                        self.assertEqual(target, transition_status(current, target, "organizer"))
                    else:
                        with self.assertRaises(DomainError) as ctx:
                            transition_status(current, target, "organizer")
                        self.assertEqual("INVALID_STATUS_TRANSITION", ctx.exception.code)

    def test_member_cannot_change_status(self):
        with self.assertRaises(DomainError) as ctx:
            transition_status("draft", "published", "member")
        self.assertEqual("ROLE_FORBIDDEN", ctx.exception.code)

    def test_invalid_status(self):
        for current, target in [("unknown", "published"), ("draft", "unknown"), ([], "published"), ("draft", None)]:
            with self.subTest(current=current, target=target):
                with self.assertRaises(DomainError) as ctx:
                    transition_status(current, target, "organizer")
                self.assertEqual("INVALID_STATUS", ctx.exception.code)
