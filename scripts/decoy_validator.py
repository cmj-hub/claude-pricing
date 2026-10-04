#!/usr/bin/env python3
"""
Three-tier decoy validator — checks asymmetric dominance + tier health.

Validates a proposed (or current) three-tier pricing structure against
the JMC contrast-set rules:

  1. Three tiers, no more
  2. Same value metric across all tiers
  3. Decoy (T1) is asymmetrically dominated by Target (T2)
     — strictly less quantity of value-metric, or strictly fewer features
  4. Anchor (T3) priced ≥3x Target (T2)
  5. Per-unit price decreases T1 → T2 → T3
  6. Feature differentiation is grokable (each tier has ≤6 distinguishing
     features)

Usage:
  python3 scripts/decoy_validator.py --tiers tiers.json
  python3 scripts/decoy_validator.py --tiers - <<< '<inline JSON>'

Tier JSON format:
  {
    "tiers": [
      {
        "name": "Starter",
        "price": 99,
        "cadence": "monthly",
        "value_metric_unit": "seat",
        "value_metric_quantity": 5,
        "features": ["SSO", "Basic reporting", "Email support"]
      },
      ...
    ]
  }

Returns: JSON with pass/fail per rule + an overall score 0-100.
Exits 1 when the score is below 60 (REBUILD), 0 otherwise.

Zero dependencies. Python 3.8+.
"""
import argparse
import json
import sys
from pathlib import Path


MAX_INPUT_BYTES = 2_000_000


def fail_input(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def read_text(path: Path) -> str:
    try:
        if not path.exists():
            fail_input(f"file not found: {path}")
        if not path.is_file():
            fail_input(f"not a file: {path}")
        if path.stat().st_size > MAX_INPUT_BYTES:
            fail_input(f"file is too large: {path}")
        raw = path.read_bytes()
    except SystemExit:
        raise
    except OSError:
        fail_input(f"cannot read file: {path}")
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        fail_input(f"file is not UTF-8 text: {path}")


def parse_json_text(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        fail_input("invalid JSON")


def read_stdin_text() -> str:
    raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        fail_input("input is too large")
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        fail_input("input is not UTF-8 text")


def write_output(path: str, text: str) -> None:
    dest = Path(path)
    try:
        if dest.exists() and not dest.is_file():
            fail_input(f"not a file: {path}")
        dest.write_text(text)
    except SystemExit:
        raise
    except OSError:
        fail_input(f"cannot write output: {path}")


def normalize_price_annual(price: float, cadence: str) -> float:
    if cadence == "annual":
        return price
    if cadence == "monthly":
        return price * 12
    raise ValueError(f"Unknown cadence: {cadence}")


def per_unit_price(tier: dict) -> float:
    annual = normalize_price_annual(tier["price"], tier["cadence"])
    qty = max(tier["value_metric_quantity"], 1)
    return annual / qty


def check_three_tiers(tiers: list) -> dict:
    passed = len(tiers) == 3
    return {
        "rule": "three_tiers_only",
        "passed": passed,
        "detail": f"Found {len(tiers)} tier(s); expected exactly 3.",
        "weight": 15,
    }


def check_same_metric(tiers: list) -> dict:
    units = {t["value_metric_unit"] for t in tiers}
    blank = any(not isinstance(u, str) or not u.strip() for u in units)
    passed = len(units) == 1 and not blank
    if passed:
        detail = f"All tiers use '{list(units)[0]}'"
    elif blank:
        detail = "A tier has no value_metric_unit. A price needs a unit it is per."
    else:
        detail = (
            f"Mixed units across tiers: {sorted(units)}. "
            f"Buyer can't grok comparison."
        )
    return {
        "rule": "same_value_metric",
        "passed": passed,
        "detail": detail,
        "weight": 20,
    }


def check_decoy_dominated(tiers: list) -> dict:
    if len(tiers) < 2:
        return {
            "rule": "decoy_asymmetrically_dominated",
            "passed": False,
            "detail": "Need at least 2 tiers to check dominance.",
            "weight": 25,
        }
    t1, t2 = tiers[0], tiers[1]
    qty_ok = t1["value_metric_quantity"] < t2["value_metric_quantity"]
    feat_t1 = set(t1.get("features", []))
    feat_t2 = set(t2.get("features", []))
    features_ok = feat_t1.issubset(feat_t2) or len(feat_t1) < len(feat_t2)
    passed = qty_ok and features_ok
    return {
        "rule": "decoy_asymmetrically_dominated",
        "passed": passed,
        "detail": (
            "T1 is asymmetrically dominated by T2 (strictly less quantity "
            "+ subset features)." if passed else
            f"T1 not dominated: qty_check={qty_ok}, features_check={features_ok}. "
            f"Buyer won't see T2 as obviously better."
        ),
        "weight": 25,
    }


def check_anchor_3x(tiers: list) -> dict:
    if len(tiers) < 3:
        return {
            "rule": "anchor_at_least_3x_target",
            "passed": False,
            "detail": "Need 3 tiers to check anchor multiple.",
            "weight": 15,
        }
    t2_annual = normalize_price_annual(tiers[1]["price"], tiers[1]["cadence"])
    t3_annual = normalize_price_annual(tiers[2]["price"], tiers[2]["cadence"])
    multiple = t3_annual / t2_annual if t2_annual > 0 else 0
    passed = multiple >= 3.0
    return {
        "rule": "anchor_at_least_3x_target",
        "passed": passed,
        "detail": (
            f"T3 is {multiple:.2f}x T2 (≥3x required for anchor effect)."
            if passed else
            f"T3 is only {multiple:.2f}x T2; anchor effect weak. "
            f"Either raise T3 or this isn't a real anchor tier."
        ),
        "weight": 15,
    }


def check_per_unit_decreases(tiers: list) -> dict:
    per_units = [per_unit_price(t) for t in tiers]
    decreasing = all(
        per_units[i] >= per_units[i + 1] for i in range(len(per_units) - 1)
    )
    return {
        "rule": "per_unit_price_decreases_across_tiers",
        "passed": decreasing,
        "detail": (
            f"Per-unit (annual): {[round(p, 2) for p in per_units]}. "
            f"{'Decreasing (good).' if decreasing else 'NOT monotonic — creates a cliff.'}"
        ),
        "weight": 10,
    }


def check_feature_count(tiers: list) -> dict:
    counts = [len(t.get("features", [])) for t in tiers]
    over = [(i, c) for i, c in enumerate(counts) if c > 6]
    passed = not over
    return {
        "rule": "feature_count_grokable",
        "passed": passed,
        "detail": (
            f"Feature counts: {counts}. All ≤6 (grokable in <30s)." if passed
            else f"Tier(s) over 6 features: {over}. Buyer parsing tax."
        ),
        "weight": 10,
    }


def run_checks(tiers: list) -> dict:
    checks = [
        check_three_tiers(tiers),
        check_same_metric(tiers),
        check_decoy_dominated(tiers),
        check_anchor_3x(tiers),
        check_per_unit_decreases(tiers),
        check_feature_count(tiers),
    ]
    earned = sum(c["weight"] for c in checks if c["passed"])
    total = sum(c["weight"] for c in checks)
    score = round(earned / total * 100, 1) if total else 0
    return {
        "score": score,
        "earned": earned,
        "total": total,
        "checks": checks,
        "summary": (
            "HEALTHY three-tier contrast set." if score >= 85
            else "ITERATE — real issues but structure is repairable."
            if score >= 60 else "REBUILD — multiple structural failures."
        ),
    }


def main():
    p = argparse.ArgumentParser(description="Three-tier decoy validator")
    p.add_argument(
        "--tiers", required=True,
        help="Path to JSON file with tier definitions, or '-' to read stdin",
    )
    p.add_argument("--output", help="Output JSON path (default: stdout)")
    args = p.parse_args()

    if args.tiers == "-":
        data = parse_json_text(read_stdin_text())
    else:
        data = parse_json_text(read_text(Path(args.tiers)))

    if not isinstance(data, dict):
        fail_input("JSON must be an object")
    tiers = data.get("tiers", [])
    if not isinstance(tiers, list) or not all(isinstance(tier, dict) for tier in tiers):
        fail_input("tiers must be a list of objects")
    if not tiers:
        print("No tiers provided.", file=sys.stderr)
        sys.exit(1)

    try:
        result = run_checks(tiers)
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        fail_input(
            "each tier needs price, cadence, value_metric_unit, and value_metric_quantity"
        )
    out = json.dumps(result, indent=2)

    if args.output:
        write_output(args.output, out)
    else:
        print(out)
    # Exit 1 on REBUILD so a caller can loop until the structure holds.
    if result["score"] < 60:
        sys.exit(1)


if __name__ == "__main__":
    main()
