#!/usr/bin/env python3
"""score_anchor.py passes a sourced anchor shown before the price and refuses the rest."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "examples"
SCRIPT = ROOT / "scripts" / "score_anchor.py"
GOOD = json.loads((EX / "anchor-good.json").read_text())
REFUSED_NEXT = "Next: fix the lines above and run this again."


def run(args, stdin=None):
    return subprocess.run([sys.executable, str(SCRIPT), *args], input=stdin, capture_output=True, text=True)


def score(obj, *extra):
    return run(["--stdin", *extra], stdin=json.dumps(obj))


def good(**changes):
    draft = json.loads(json.dumps(GOOD))
    draft.update(changes)
    return draft


class Examples(unittest.TestCase):
    def test_good_passes(self):
        out = run(["--file", str(EX / "anchor-good.json")])
        self.assertEqual(out.returncode, 0, out.stdout)
        self.assertEqual(out.stdout.strip().splitlines()[-1], "Next: /pricing:pricing tiers (design the tier cards under the anchor)")

    def test_competitor_only_refused(self):
        out = run(["--file", str(EX / "anchor-competitor-only.json")])
        self.assertEqual(out.returncode, 1)
        lines = out.stdout.strip().splitlines()
        self.assertEqual(lines[-1], REFUSED_NEXT)
        for line in lines:
            if line.startswith("- "):
                self.assertIn(" → ", line)
        self.assertIn("16 CFR 233.1", out.stdout)


class Rules(unittest.TestCase):
    def test_anchor_needs_source(self):
        draft = good()
        del draft["anchor"]["source"]
        self.assertEqual(score(draft).returncode, 1)

    def test_anchor_smaller_than_price_refused(self):
        out = score(good(anchor={"amount": 40000, "period": "year", "source": "call"}))
        self.assertEqual(out.returncode, 1)
        self.assertIn("anchors the wrong way", out.stdout)

    def test_units_normalised(self):
        # 5,000 a month anchor = 60,000 a year, above a 48,000 a year price.
        self.assertEqual(score(good(anchor={"amount": 5000, "period": "month", "source": "call"})).returncode, 0)

    def test_price_first_refused(self):
        self.assertEqual(score(good(anchor_before_price=False)).returncode, 1)

    def test_competitor_with_reason_allowed(self):
        self.assertEqual(score(good(frame="competitor", competitor_reason="buyers only compare the two leaders")).returncode, 0)

    def test_cheaper_than_refused(self):
        self.assertEqual(score(good(headline="Forty percent cheaper than the leading tool.")).returncode, 1)

    def test_less_than_time_is_fine(self):
        self.assertEqual(score(good(subhead="Notes land in less than 10 minutes, not 3 hours later.")).returncode, 0)

    def test_cost_plus_refused(self):
        self.assertEqual(score(good(subhead="We price at our cost plus 20%, so $4,000.")).returncode, 1)

    def test_long_headline_refused(self):
        self.assertEqual(score(good(headline=" ".join(["word"] * 15))).returncode, 1)

    def test_subhead_needs_number(self):
        self.assertEqual(score(good(subhead="That is a lot of selling time.")).returncode, 1)

    def test_satisfaction_guarantee_refused(self):
        self.assertEqual(score(good(guarantee="Money back if you're not satisfied.")).returncode, 1)

    def test_was_price_needs_evidence(self):
        self.assertEqual(score(good(was_price={"amount": 6000, "period": "month"})).returncode, 1)
        ok = good(was_price={"amount": 6000, "period": "month", "evidence": "charged 2026-03-01 to 2026-09-30"})
        self.assertEqual(score(ok).returncode, 0)

    def test_json(self):
        data = json.loads(score(GOOD, "--json").stdout)
        self.assertTrue(data["pass"])
        self.assertEqual(data["frame"], "inertia")


class BadInput(unittest.TestCase):
    def test_not_json(self):
        self.assertEqual(run(["--stdin"], stdin="nope").returncode, 2)

    def test_missing_file(self):
        self.assertEqual(run(["--file", "nope.json"]).returncode, 2)

    def test_both_sources(self):
        self.assertEqual(run(["--file", str(EX / "anchor-good.json"), "--stdin"], stdin="{}").returncode, 2)


if __name__ == "__main__":
    unittest.main()
