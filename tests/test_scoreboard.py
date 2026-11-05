import tempfile
import unittest
from pathlib import Path
from scoreboard import summarize, run


def row(variant="A", visitors="100", conversions="20"):
    return {"variant": variant, "visitors": visitors, "conversions": conversions}


class ScoreboardTests(unittest.TestCase):
    def test_conversion_rate(self):
        self.assertEqual(summarize([row()])["variants"][0]["conversion_rate"], 0.2)
    def test_aggregation(self):
        self.assertEqual(summarize([row(), row()])["variants"][0]["visitors"], 200)
    def test_best_observed(self):
        self.assertEqual(summarize([row(), row("B", "100", "30")])["best_observed_variant"], "B")
    def test_bad_visitors(self):
        with self.assertRaises(ValueError):
            summarize([row(visitors="0")])
    def test_bad_conversions(self):
        with self.assertRaises(ValueError):
            summarize([row(conversions="101")])
    def test_confidence_interval(self):
        low, high = summarize([row()])["variants"][0]["wilson_95_interval"]
        self.assertLess(low, .2)
        self.assertGreater(high, .2)
    def test_empty(self):
        self.assertIsNone(summarize([])["best_observed_variant"])
    def test_csv(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.csv"
            path.write_text("variant,visitors,conversions\nA,100,20\n", encoding="utf-8")
            self.assertEqual(run(str(path))["variants"][0]["conversions"], 20)


if __name__ == "__main__":
    unittest.main()
