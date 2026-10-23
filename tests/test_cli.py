#!/usr/bin/env python3
"""Every scorer takes --file/--stdin, keeps its old flag, and ends with a Next line."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

from native_test_support import run_native, waterfall_rows, wtp_rows, module
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
EX = ROOT / "examples"
REFUSED_NEXT = "Next: fix the lines above and run this again."


def run(script, args, stdin=None):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / script), *args],
        input=stdin,
        capture_output=True,
        text=True,
    )


class ScorePriceCli(unittest.TestCase):
    def test_refusal_lines_say_what_to_change(self):
        result = run("score_price.py", ["--file", str(EX / "price-no-metric.json")])
        self.assertEqual(result.returncode, 1)
        lines = result.stdout.strip().splitlines()
        self.assertEqual(lines[-1], REFUSED_NEXT)
        reasons = [line for line in lines if line.startswith("- ")]
        self.assertEqual(len(reasons), 3)
        for line in reasons:
            self.assertIn(" → ", line)

    def test_pass_names_next_suite_step(self):
        result = run("score_price.py", ["--file", str(EX / "price-good.json")])
        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout.strip().splitlines()[-1],
            "Next: /landing-page:page (put the price on the page with its unit)",
        )

    def test_json_is_additive(self):
        out = json.loads(run("score_price.py", ["--file", str(EX / "price-no-metric.json"), "--json"]).stdout)
        self.assertEqual(len(out["fixes"]), len(out["reasons"]))
        self.assertIn("next", out)

    def test_help_shows_example(self):
        result = run("score_price.py", ["--help"])
        self.assertIn("examples/price-good.json", result.stdout)


class DecoyCli(unittest.TestCase):
    def test_file_stdin_and_old_flag_agree(self):
        path = str(EX / "tiers-healthy.json")
        by_file = json.loads(run("decoy_validator.py", ["--file", path]).stdout)
        by_alias = json.loads(run("decoy_validator.py", ["--tiers", path]).stdout)
        by_stdin = json.loads(
            run("decoy_validator.py", ["--stdin"], stdin=Path(path).read_text()).stdout
        )
        self.assertEqual(by_file, by_alias)
        self.assertEqual(by_file, by_stdin)

    def test_text_refusal(self):
        result = run("decoy_validator.py", ["--file", str(EX / "tiers-broken.json"), "--text"])
        self.assertEqual(result.returncode, 1)
        lines = result.stdout.strip().splitlines()
        self.assertEqual(lines[-1], REFUSED_NEXT)
        self.assertTrue(all(" → " in l for l in lines if l.startswith("- ")))

    def test_json_fix_per_failed_check(self):
        out = json.loads(run("decoy_validator.py", ["--file", str(EX / "tiers-broken.json"), "--json"]).stdout)
        for check in out["checks"]:
            self.assertEqual("fix" in check, not check["passed"])
        self.assertIn("next", out)

    def test_empty_tiers_is_bad_input(self):
        result = run("decoy_validator.py", ["--stdin"], stdin='{"tiers": []}')
        self.assertEqual(result.returncode, 2)


class WtpCli(unittest.TestCase):
    def test_example_passes_with_next(self):
        result = run_native("wtp_distribution.py", ["--file", "private-input", "--text"], wtp_rows())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.strip().splitlines()[-1].startswith("Next: /pricing:pricing tiers"))

    def test_old_flag_and_json_default(self):
        out = json.loads(run_native("wtp_distribution.py", ["--input", "private-input"], wtp_rows()).stdout)
        self.assertEqual(out["n_respondents"], 6)
        self.assertIn("next", out)
        self.assertIn("thresholds", out)
        self.assertIn("acceptable_range", out)

    def test_too_few_responses_refused(self):
        result = run_native("wtp_distribution.py", ["--stdin", "--text"], wtp_rows(2))
        self.assertEqual(result.returncode, 1)
        lines = result.stdout.strip().splitlines()
        self.assertEqual(lines[-1], REFUSED_NEXT)
        self.assertIn(" → ", lines[0])


class WaterfallCli(unittest.TestCase):
    def test_example_text(self):
        result = run_native("pocket_price_waterfall.py", ["--file", "private-input", "--text"], waterfall_rows())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Top 3 leak sources", result.stdout)
        self.assertTrue(result.stdout.strip().splitlines()[-1].startswith("Next: "))

    def test_old_flag_json_default(self):
        out = json.loads(run_native("pocket_price_waterfall.py", ["--input", "private-input"], waterfall_rows()).stdout)
        self.assertEqual(out["cohort"]["n_customers"], 2)
        self.assertIn("next", out)

    def test_zero_list_price_is_skipped_not_crash(self):
        result = run_native("pocket_price_waterfall.py", ["--stdin", "--text"], [dict(customer_id="synthetic-zero", list_price=0, cadence="annual")])
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(result.stdout.strip().splitlines()[-1], REFUSED_NEXT)


class NativeWaterfallMath(unittest.TestCase):
    def test_discount_stacking_annualization_fees_and_credits(self):
        target = module("pocket_price_waterfall.py")
        row = waterfall_rows()[0]
        row.update(list_price=10, cadence="monthly", implementation_fee=5, credits_applied=3,
                   payment_terms_days=30, discount_steps_json="test-only steps")
        steps = [dict(name="test-one", pct=0.1), dict(name="test-two", pct=0.2)]
        with patch.object(target.json, "loads", return_value=steps) as parse:
            result = target.compute_pocket(row)
        parse.assert_called_once_with("test-only steps")
        self.assertEqual(result["list_price_annual"], 120)
        self.assertAlmostEqual(result["pocket_price_annual"], 88.4)
        self.assertEqual([step["name"] for step in result["leak_by_step"]], ["test-one", "test-two"])
        self.assertAlmostEqual(result["leak_by_step"][0]["dollar_leak"], 12)
        self.assertAlmostEqual(result["leak_by_step"][1]["dollar_leak"], 21.6)

    def test_receivables_cost_only_applies_beyond_baseline(self):
        target = module("pocket_price_waterfall.py")
        self.assertEqual(target.payment_terms_cost(100, 15), 0)
        self.assertEqual(target.payment_terms_cost(100, 30), 0)
        self.assertAlmostEqual(target.payment_terms_cost(365, 60), 2.4)


if __name__ == "__main__":
    unittest.main()
