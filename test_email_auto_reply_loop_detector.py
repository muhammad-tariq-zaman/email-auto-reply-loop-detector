import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import detect

def row(sender, recipient, count, subject="Out of office"):
    return {"from_mailbox": sender, "to_mailbox": recipient,
            "auto_replies": str(count), "subject": subject}

class TestAutoReplyLoop(unittest.TestCase):
    def test_both_ways_is_loop(self):
        r, _ = detect([row("a@x.com", "b@y.com", 2),
                       row("b@y.com", "a@x.com", 2)])
        self.assertEqual(r[0][3], "LOOP")
        self.assertIn("each way", r[0][4])

    def test_five_one_way_is_loop(self):
        r, _ = detect([row("a@x.com", "b@y.com", 6)])
        self.assertEqual(r[0][3], "LOOP")
        self.assertIn("one way", r[0][4])

    def test_three_one_way_is_suspect(self):
        r, _ = detect([row("a@x.com", "b@y.com", 3)])
        self.assertEqual(r[0][3], "SUSPECT")

    def test_two_is_ok(self):
        r, _ = detect([row("a@x.com", "b@y.com", 2)])
        self.assertEqual(r[0][3], "OK")

    def test_same_pair_rows_are_summed(self):
        r, _ = detect([row("a@x.com", "b@y.com", 2),
                       row("a@x.com", "b@y.com", 2)])
        self.assertEqual((len(r), r[0][2], r[0][3]), (1, 4, "SUSPECT"))

    def test_loop_comes_first(self):
        r, _ = detect([row("a@x.com", "b@y.com", 1),
                       row("c@x.com", "d@y.com", 7)])
        self.assertEqual(r[0][0], "c@x.com")

    def test_invalid_row_is_skipped(self):
        r, skipped = detect([row("a@x.com", "b@y.com", "many"),
                             row("a@x.com", "b@y.com", 1)])
        self.assertEqual((len(r), skipped), (1, 1))

    def test_empty_input(self):
        self.assertEqual(detect([]), ([], 0))
