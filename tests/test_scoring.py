#!/usr/bin/env python3
"""The sample tiers pass the decoy validator; the broken tiers are refused."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def decoy(name):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "decoy_validator.py"),
         "--tiers", str(ROOT / "examples" / name)],
        capture_output=True,
        text=True,
    )


class DecoyValidator(unittest.TestCase):
    def test_healthy_tiers_pass(self):
        result = decoy("tiers-healthy.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertGreaterEqual(json.loads(result.stdout)["score"], 85)

    def test_broken_tiers_exit_1(self):
        result = decoy("tiers-broken.json")
        self.assertEqual(result.returncode, 1)
        self.assertIn("REBUILD", json.loads(result.stdout)["summary"])

    def test_blank_unit_fails_same_metric(self):
        tiers = json.loads((ROOT / "examples" / "tiers-healthy.json").read_text())
        for tier in tiers["tiers"]:
            tier["value_metric_unit"] = " "
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "decoy_validator.py"), "--tiers", "-"],
            input=json.dumps(tiers),
            capture_output=True,
            text=True,
        )
        checks = {c["rule"]: c for c in json.loads(result.stdout)["checks"]}
        self.assertFalse(checks["same_value_metric"]["passed"])
        self.assertIn("no value_metric_unit", checks["same_value_metric"]["detail"])


if __name__ == "__main__":
    unittest.main()
