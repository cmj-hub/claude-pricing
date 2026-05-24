#!/usr/bin/env python3
"""
Van Westendorp Price Sensitivity Meter (PSM) analyzer.

Computes the four threshold intersection points from Van Westendorp
survey data:

  - Point of Marginal Cheapness (PMC): where "too cheap" meets "not bargain"
  - Point of Marginal Expensiveness (PME): where "not expensive" meets "too expensive"
  - Optimal Price Point (OPP): where "too cheap" meets "too expensive"
  - Indifference Price Point (IPP): where "bargain" meets "expensive"

Acceptable price range = [PMC, PME].

Usage:
  python3 scripts/wtp_distribution.py --input responses.csv

CSV format (header row required):
  respondent_id,psp,too_cheap,bargain,expensive,too_expensive

  Each numeric column is the price (in operator's currency) the
  respondent answered for that Van Westendorp question.

Output: JSON with the 4 thresholds + acceptable range + cohort
distribution stats, optionally per-PSP.

Zero dependencies. Python 3.8+. Minimum n=15 per PSP for stable
thresholds (n=30+ recommended).
"""
import argparse
import csv
import json
import statistics
import sys
from pathlib import Path


def cumulative_distribution(values: list, prices: list, direction: str) -> list:
    """
    Build a cumulative percentage at each price point.

    direction == "ascending": cumulative pct of values ≤ price
                              (used for "too cheap", "bargain")
    direction == "descending": cumulative pct of values ≥ price
                               (used for "expensive", "too expensive")
    """
    n = len(values)
    if n == 0:
        return [(p, 0) for p in prices]
    sorted_vals = sorted(values)
    result = []
    for price in prices:
        if direction == "ascending":
            count = sum(1 for v in sorted_vals if v <= price)
        else:
            count = sum(1 for v in sorted_vals if v >= price)
        result.append((price, count / n))
    return result


def find_intersection(curve_a: list, curve_b: list):
    """
    Find the price where curve_a and curve_b cross. Linear interp.
    Returns the price or None if curves don't intersect.
    """
    for i in range(len(curve_a) - 1):
        a1_price, a1_val = curve_a[i]
        a2_price, a2_val = curve_a[i + 1]
        _, b1_val = curve_b[i]
        _, b2_val = curve_b[i + 1]
        diff1 = a1_val - b1_val
        diff2 = a2_val - b2_val
        if diff1 == 0:
            return a1_price
        if diff1 * diff2 < 0:
            # Sign change — interpolate.
            t = diff1 / (diff1 - diff2)
            return a1_price + t * (a2_price - a1_price)
    return None


def analyze_cohort(responses: list) -> dict:
    if len(responses) < 5:
        return {"error": f"Only {len(responses)} responses; need ≥5 minimum, ≥15 recommended."}

    too_cheap = [r["too_cheap"] for r in responses]
    bargain = [r["bargain"] for r in responses]
    expensive = [r["expensive"] for r in responses]
    too_expensive = [r["too_expensive"] for r in responses]

    min_p = min(too_cheap)
    max_p = max(too_expensive)
    step = max((max_p - min_p) / 100, 0.01)
    prices = [min_p + i * step for i in range(101)]

    # Curves
    tc_curve = cumulative_distribution(too_cheap, prices, "descending")
    nb_curve = cumulative_distribution(bargain, prices, "descending")
    ne_curve = cumulative_distribution(expensive, prices, "ascending")
    te_curve = cumulative_distribution(too_expensive, prices, "ascending")

    # Intersections
    pmc = find_intersection(tc_curve, ne_curve)
    pme = find_intersection(nb_curve, te_curve)
    opp = find_intersection(tc_curve, te_curve)
    ipp = find_intersection(nb_curve, ne_curve)

    def round_or_none(x):
        return round(x, 2) if x is not None else None

    result = {
        "n_respondents": len(responses),
        "thresholds": {
            "point_marginal_cheapness": round_or_none(pmc),
            "indifference_price_point": round_or_none(ipp),
            "optimal_price_point": round_or_none(opp),
            "point_marginal_expensiveness": round_or_none(pme),
        },
        "acceptable_range": {
            "lower": round_or_none(pmc),
            "upper": round_or_none(pme),
        },
        "raw_stats": {
            "too_cheap_p50": round(statistics.median(too_cheap), 2),
            "bargain_p50": round(statistics.median(bargain), 2),
            "expensive_p50": round(statistics.median(expensive), 2),
            "too_expensive_p50": round(statistics.median(too_expensive), 2),
        },
        "interpretation": {
            "what_pmc_means": (
                "Below PMC, buyers question quality — 'this is too cheap to be real.'"
            ),
            "what_pme_means": (
                "Above PME, buyers consider price unjustifiable — 'too expensive at any value claim.'"
            ),
            "what_opp_means": (
                "OPP is the price with the LEAST buyer resistance — equal pushback "
                "on 'too cheap' and 'too expensive' sides."
            ),
            "what_ipp_means": (
                "IPP is the median willingness-to-pay; half think it's a bargain, "
                "half think it's expensive."
            ),
        },
    }

    if result["acceptable_range"]["lower"] and result["acceptable_range"]["upper"]:
        result["recommendation"] = (
            f"Price within [${result['acceptable_range']['lower']}, "
            f"${result['acceptable_range']['upper']}] for this segment. "
            f"OPP ${result['thresholds']['optimal_price_point']} is the "
            f"least-resistance anchor."
        )
    return result


def main():
    p = argparse.ArgumentParser(description="Van Westendorp PSM analyzer")
    p.add_argument("--input", required=True, help="CSV file of survey responses")
    p.add_argument("--output", help="Output JSON path (default: stdout)")
    p.add_argument(
        "--per-psp",
        action="store_true",
        help="Split analysis per PSP (requires 'psp' column in CSV)",
    )
    args = p.parse_args()

    path = Path(args.input)
    if not path.exists():
        print(f"Input not found: {path}", file=sys.stderr)
        sys.exit(1)

    responses = []
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                responses.append({
                    "respondent_id": row["respondent_id"],
                    "psp": row.get("psp", "default"),
                    "too_cheap": float(row["too_cheap"]),
                    "bargain": float(row["bargain"]),
                    "expensive": float(row["expensive"]),
                    "too_expensive": float(row["too_expensive"]),
                })
            except (ValueError, KeyError) as e:
                print(
                    f"Skipping respondent {row.get('respondent_id', '?')}: {e}",
                    file=sys.stderr,
                )

    if args.per_psp:
        by_psp = {}
        for r in responses:
            by_psp.setdefault(r["psp"], []).append(r)
        result = {
            "per_psp": {psp: analyze_cohort(rs) for psp, rs in by_psp.items()},
            "overall": analyze_cohort(responses),
        }
    else:
        result = analyze_cohort(responses)

    out = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(out)
    else:
        print(out)


if __name__ == "__main__":
    main()
