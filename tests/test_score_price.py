#!/usr/bin/env python3
"""score_price.py refuses a price with no metric and passes a complete draft."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = "super-secret-cell"


def run(args, stdin=None):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "score_price.py"), *args],
        input=stdin,
        capture_output=True,
        text=True,
    )


class ScorePrice(unittest.TestCase):
    def test_bad_fixture_fails(self):
        result = run(["--file", str(ROOT / "examples" / "price-no-metric.json")])
        self.assertEqual(result.returncode, 1)
        self.assertIn("a price with no metric", result.stdout)
        self.assertNotIn("tribunal:", result.stdout)

    def test_every_reason_reported(self):
        result = run(["--file", str(ROOT / "examples" / "price-no-metric.json"), "--json"])
        self.assertEqual(result.returncode, 1)
        out = json.loads(result.stdout)
        self.assertFalse(out["ok"])
        self.assertEqual(
            out["reasons"],
            ["a price with no metric", "no contrast set", "no tribunal verdict"],
        )

    def test_good_fixture_passes(self):
        result = run(["--file", str(ROOT / "examples" / "price-good.json")])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("per active record", result.stdout)
        self.assertIn("Starter", result.stdout)
        self.assertIn("Growth", result.stdout)
        self.assertIn("Scale", result.stdout)
        self.assertIn("Hold the list price until the metric is on the page", result.stdout)

    def test_good_fixture_json(self):
        result = run(["--file", str(ROOT / "examples" / "price-good.json"), "--json"])
        self.assertEqual(result.returncode, 0)
        out = json.loads(result.stdout)
        self.assertTrue(out["ok"])
        self.assertEqual(out["reasons"], [])
        self.assertEqual(out["contrast_set"], ["Starter", "Growth", "Scale"])

    def test_blank_contrast_item_refused(self):
        draft = {
            "price": 99,
            "value_metric": "per seat",
            "contrast_set": ["Starter", " "],
            "tribunal": "Ship",
        }
        result = run(["--stdin"], stdin=json.dumps(draft))
        self.assertEqual(result.returncode, 1)
        self.assertIn("no contrast set", result.stdout)

    def test_bad_json_and_non_object_hide_input(self):
        bad = run(["--stdin"], stdin='{"price": "' + CELL)
        self.assertEqual(bad.returncode, 2)
        self.assertNotIn(CELL, bad.stdout + bad.stderr)
        array = run(["--stdin"], stdin='["' + CELL + '"]')
        self.assertEqual(array.returncode, 2)
        self.assertNotIn(CELL, array.stdout + array.stderr)
        self.assertIn("JSON must be an object", array.stderr)

    def test_missing_file_and_no_source(self):
        missing = run(["--file", str(ROOT / "no-such.json")])
        self.assertEqual(missing.returncode, 2)
        self.assertIn("file not found", missing.stderr)
        neither = run([])
        self.assertEqual(neither.returncode, 2)


if __name__ == "__main__":
    unittest.main()
