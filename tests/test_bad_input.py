#!/usr/bin/env python3
"""Pricing CLIs fail cleanly and do not echo a bad cell or JSON document."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = "super-secret-token"


def run(script, args, stdin=None):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *args],
        input=stdin,
        capture_output=True,
        text=True,
    )


class PricingBadInput(unittest.TestCase):
    def test_decoy_missing_and_bad_json(self):
        missing = run("decoy_validator.py", ["--tiers", str(ROOT / "no-such.json")])
        self.assertEqual(missing.returncode, 2)
        self.assertIn("file not found", missing.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tiers.json"
            path.write_text('{"tiers": "' + CELL, encoding="utf-8")
            bad = run("decoy_validator.py", ["--tiers", str(path)])
        self.assertEqual(bad.returncode, 2)
        self.assertNotIn(CELL, bad.stderr + bad.stdout)
        array = run("decoy_validator.py", ["--tiers", "-"], stdin="[]")
        self.assertEqual(array.returncode, 2)
        self.assertIn("JSON must be an object", array.stderr)

    def test_decoy_bad_tier_shape(self):
        result = run(
            "decoy_validator.py",
            ["--tiers", "-"],
            stdin='{"tiers":[{"name":"only"}]}',
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("each tier needs", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_wtp_hides_bad_cell(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "wtp.csv"
            path.write_text(
                "respondent_id,psp,too_cheap,bargain,expensive,too_expensive\n"
                f"r1,default,{CELL},1,2,3\n",
                encoding="utf-8",
            )
            result = run("wtp_distribution.py", ["--input", str(path)])
        self.assertNotIn("Traceback", result.stderr)
        self.assertNotIn(CELL, result.stderr + result.stdout)
        self.assertIn("bad number or missing column", result.stderr)

    def test_wtp_missing_file(self):
        result = run("wtp_distribution.py", ["--input", str(ROOT / "no-such.csv")])
        self.assertEqual(result.returncode, 2)
        self.assertIn("file not found", result.stderr)

    def test_pocket_hides_bad_cell(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "customers.csv"
            path.write_text(
                "customer_id,list_price,cadence,discount_steps_json,"
                "payment_terms_days,implementation_fee,credits_applied\n"
                f"acme,{CELL},monthly,[],30,0,0\n",
                encoding="utf-8",
            )
            result = run("pocket_price_waterfall.py", ["--input", str(path)])
        self.assertNotIn("Traceback", result.stderr)
        self.assertNotIn(CELL, result.stderr + result.stdout)
        self.assertIn("bad number or missing column", result.stderr)


if __name__ == "__main__":
    unittest.main()
