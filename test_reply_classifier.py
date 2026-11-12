
import unittest
from reply_classifier import classify_reply


class TestReplyClassifier(unittest.TestCase):

    def test_positive_reply(self):
        result = classify_reply("Thank you, excellent work")
        self.assertEqual(result["category"], "Positive")

    def test_negative_reply(self):
        result = classify_reply(
            "I am disappointed with this problem"
        )
        self.assertEqual(result["category"], "Negative")

    def test_neutral_reply(self):
        result = classify_reply(
            "I received your message yesterday"
        )
        self.assertEqual(result["category"], "Neutral")

    def test_urgent_reply(self):
        result = classify_reply("This is urgent")
        self.assertEqual(result["priority"], "URGENT")

    def test_follow_up(self):
        result = classify_reply("Please confirm")
        self.assertTrue(result["follow_up_required"])

    def test_yesterday_is_neutral(self):
        result = classify_reply(
            "I received your message yesterday"
        )
        self.assertEqual(result["category"], "Neutral")

    def test_mixed_reply_with_like(self):
        result = classify_reply(
            "I like your product, but I am unhappy with the delivery"
        )

        self.assertEqual(result["category"], "Mixed")

    def test_call_me_back_follow_up(self):
        result = classify_reply("Please call me back tomorrow")
        self.assertTrue(result["follow_up_required"])

    def test_empty_message(self):
        result = classify_reply("")
        self.assertEqual(result["category"], "Neutral")
        self.assertEqual(result["priority"], "NORMAL")
        self.assertFalse(result["follow_up_required"])

    def test_whitespace_message(self):
        result = classify_reply("     ")
        self.assertEqual(result["category"], "Neutral")
        self.assertEqual(result["priority"], "NORMAL")
        self.assertFalse(result["follow_up_required"])
    def test_complaint_reply(self):
        result = classify_reply(
            "I am unhappy with the poor service"
        )
        self.assertEqual(result["category"], "Negative")
        self.assertEqual(result["priority"], "HIGH")
    def test_not_happy_reply(self):
        result = classify_reply("I am not happy with the service")
        self.assertEqual(result["category"], "Negative")
        self.assertEqual(result["priority"], "HIGH")

if __name__ == "__main__":
    unittest.main()
