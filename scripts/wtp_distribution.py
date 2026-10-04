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
  python3 scripts/wtp_distribution.py --file gtm/wtp.csv
  python3 scripts/wtp_distribution.py --stdin < gtm/wtp.csv
  python3 scripts/wtp_distribution.py --file gtm/wtp.csv --format text

`--input PATH` still works as an alias for `--file`.

CSV format (header row required):
  respondent_id,psp,too_cheap,bargain,expensive,too_expensive

  Each numeric column is the price (in operator's currency) the
  respondent answered for that Van Westendorp question.

Output: JSON with the 4 thresholds + acceptable range + cohort
distribution stats, optionally per-PSP (the default, kept for callers
that parse it; `--json` asks for it explicitly). The object carries
`next`, and `fixes` when the cohort is refused. `--format text` (or
`--text`) prints the thresholds and a last `Next:` line instead.

Exit codes: 0 analyzed, 1 refused (fewer than 5 usable responses),
2 bad input. Skipped rows are reported by row number, never by content.

Zero dependencies. Python 3.8+. Minimum n=15 per PSP for stable
thresholds (n=30+ recommended).
"""
import argparse
import csv
import json
import statistics
import sys
from pathlib import Path


MAX_INPUT_BYTES = 2_000_000
MIN_RESPONSES = 5

NEXT_OK = "/pricing:pricing tiers (price the target tier inside the acceptable range)"
NEXT_REFUSED = "fix the lines above and run this again."
EPILOG = """example:
  python3 scripts/wtp_distribution.py --file examples/wtp-responses.csv --text

exit codes: 0 analyzed, 1 refused (fewer than 5 usable responses), 2 bad input"""


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
    if len(responses) < MIN_RESPONSES:
        return {
            "error": f"Only {len(responses)} responses; need ≥5 minimum, ≥15 recommended.",
            "fix": "collect at least 15 complete Van Westendorp responses for this segment",
        }

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


def refusals(result: dict) -> list:
    """`- what is wrong → what to change` lines for every refused cohort."""
    lines = []
    if "per_psp" in result:
        cohorts = [("overall", result["overall"])] + sorted(result["per_psp"].items())
    else:
        cohorts = [(None, result)]
    for name, cohort in cohorts:
        if "error" in cohort:
            label = f"{name}: " if name else ""
            lines.append(f"- {label}{cohort['error']} → {cohort['fix']}")
    return lines


def format_text(result: dict, refused: bool) -> str:
    lines = []
    cohort = result.get("overall", result)
    if "thresholds" in cohort:
        th = cohort["thresholds"]
        lines += [
            f"respondents: {cohort['n_respondents']}",
            f"acceptable range: {cohort['acceptable_range']['lower']} to "
            f"{cohort['acceptable_range']['upper']}",
            f"optimal price point: {th['optimal_price_point']}",
            f"indifference price point: {th['indifference_price_point']}",
        ]
    for psp, sub in sorted(result.get("per_psp", {}).items()):
        if "acceptable_range" in sub:
            lines.append(
                f"{psp}: {sub['acceptable_range']['lower']} to "
                f"{sub['acceptable_range']['upper']} (n={sub['n_respondents']})"
            )
    lines += refusals(result)
    lines.append(f"Next: {result['next']}")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(
        description="Van Westendorp PSM analyzer",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--file", help="CSV file of survey responses (e.g. gtm/wtp.csv)")
    p.add_argument("--input", dest="file", help=argparse.SUPPRESS)
    p.add_argument("--stdin", action="store_true", help="Read the CSV from stdin")
    p.add_argument("--json", dest="format", action="store_const", const="json",
                   help="Print one JSON object (the default)")
    p.add_argument("--text", dest="format", action="store_const", const="text",
                   help="Print human text instead of JSON")
    p.add_argument("--format", dest="format", choices=["json", "text"], default="json",
                   help="Output format (default: json)")
    p.add_argument("--output", help="Write the output to this path instead of stdout")
    p.set_defaults(format="json")
    p.add_argument(
        "--per-psp",
        action="store_true",
        help="Split analysis per PSP (requires 'psp' column in CSV)",
    )
    args = p.parse_args()

    if args.stdin and args.file:
        fail_input("pass --file or --stdin, not both")
    if args.stdin:
        text = read_stdin_text()
    elif args.file:
        text = read_text(Path(args.file))
    else:
        fail_input("pass --file or --stdin")

    responses = []
    reader = csv.DictReader(text.splitlines())
    for line_no, row in enumerate(reader, start=2):
        try:
            responses.append({
                "respondent_id": row["respondent_id"],
                "psp": row.get("psp") or "default",
                "too_cheap": float(row["too_cheap"]),
                "bargain": float(row["bargain"]),
                "expensive": float(row["expensive"]),
                "too_expensive": float(row["too_expensive"]),
            })
        except (ValueError, KeyError, TypeError):
            print(
                f"Skipping row {line_no}: bad number or missing column",
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
        refused = "error" in result["overall"]
    else:
        result = analyze_cohort(responses)
        refused = "error" in result
    result["next"] = NEXT_REFUSED if refused else NEXT_OK
    if refused:
        result["fixes"] = [line.split(" → ", 1)[1] for line in refusals(result)]

    if args.format == "json":
        out = json.dumps(result, indent=2)
    else:
        out = format_text(result, refused)
    if args.output:
        write_output(args.output, out)
    else:
        print(out)
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
