#!/usr/bin/env python3
"""Every scorer takes --file/--stdin, keeps its old flag, and ends with a Next line."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

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
        result = run("wtp_distribution.py", ["--file", str(EX / "wtp-responses.csv"), "--text"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.strip().splitlines()[-1].startswith("Next: /pricing:pricing tiers"))

    def test_old_flag_and_json_default(self):
        out = json.loads(run("wtp_distribution.py", ["--input", str(EX / "wtp-responses.csv")]).stdout)
        self.assertEqual(out["n_respondents"], 20)
        self.assertIn("next", out)

    def test_too_few_responses_refused(self):
        sample = "\n".join((EX / "wtp-responses.csv").read_text().splitlines()[:3])
        result = run("wtp_distribution.py", ["--stdin", "--text"], stdin=sample)
        self.assertEqual(result.returncode, 1)
        lines = result.stdout.strip().splitlines()
        self.assertEqual(lines[-1], REFUSED_NEXT)
        self.assertIn(" → ", lines[0])


class WaterfallCli(unittest.TestCase):
    def test_example_text(self):
        result = run("pocket_price_waterfall.py", ["--file", str(EX / "waterfall-customers.csv"), "--text"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Top 3 leak sources", result.stdout)
        self.assertTrue(result.stdout.strip().splitlines()[-1].startswith("Next: "))

    def test_old_flag_json_default(self):
        out = json.loads(run("pocket_price_waterfall.py", ["--input", str(EX / "waterfall-customers.csv")]).stdout)
        self.assertEqual(out["cohort"]["n_customers"], 4)
        self.assertIn("next", out)

    def test_zero_list_price_is_skipped_not_crash(self):
        csv_text = "customer_id,list_price,cadence\nx,0,monthly\n"
        result = run("pocket_price_waterfall.py", ["--stdin", "--text"], stdin=csv_text)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(result.stdout.strip().splitlines()[-1], REFUSED_NEXT)


if __name__ == "__main__":
    unittest.main()
