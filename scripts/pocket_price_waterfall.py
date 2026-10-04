#!/usr/bin/env python3
"""
Pocket-price waterfall — discount-leak calculator.

Reads customer-level discount line-item data + computes the pocket
price per customer and the cohort-level waterfall. Ranks discount
steps by total margin impact and identifies the top 3 leak sources.

Usage:
  python3 scripts/pocket_price_waterfall.py --file gtm/waterfall.csv
  python3 scripts/pocket_price_waterfall.py --stdin < gtm/waterfall.csv
  python3 scripts/pocket_price_waterfall.py --file gtm/waterfall.csv --format text

`--input PATH` still works as an alias for `--file`.

CSV format (header row required):
  customer_id,list_price,cadence,discount_steps_json,payment_terms_days,implementation_fee,credits_applied

  - list_price: float, in the cadence currency
  - cadence: "monthly" or "annual" (annualized for waterfall)
  - discount_steps_json: JSON array of {name, pct, reason}
  - payment_terms_days: int (NET-30, NET-60, etc.)
  - implementation_fee: float (one-time)
  - credits_applied: float (annual)

Output: JSON with per-customer breakdown + cohort aggregates + leak
ranking (the default, kept for callers that parse it; `--json` asks for
it explicitly). The object carries `next`. `--format text` (or `--text`)
prints the cohort totals, the top 3 leaks, and a last `Next:` line.

Exit codes: 0 analyzed, 1 refused (no usable customer row), 2 bad input.
Skipped rows are reported by row number, never by content.

Zero dependencies. Python 3.8+.
"""
import argparse
import csv
import json
import statistics
import sys
from pathlib import Path


MAX_INPUT_BYTES = 2_000_000

NEXT_OK = ("plug the top leak first; run /pricing:pricing tribunal if the "
           "policy change touches more than 10% of customers")
NEXT_REFUSED = "fix the lines above and run this again."
EPILOG = """example:
  python3 scripts/pocket_price_waterfall.py --file examples/waterfall-customers.csv --text

exit codes: 0 analyzed, 1 refused (no usable customer row), 2 bad input"""


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


# Carrying cost of receivables, used to dollarize payment-terms differences.
# 30-day baseline; longer terms cost the seller more.
COST_OF_CAPITAL_ANNUAL = 0.08  # 8% APR


def normalize_to_annual(price: float, cadence: str) -> float:
    if cadence == "annual":
        return price
    if cadence == "monthly":
        return price * 12
    raise ValueError(f"Unknown cadence: {cadence}")


def payment_terms_cost(annual_revenue: float, terms_days: int) -> float:
    """Carrying cost of NET-{terms_days} beyond NET-30 baseline."""
    delta_days = max(terms_days - 30, 0)
    return annual_revenue * COST_OF_CAPITAL_ANNUAL * (delta_days / 365)


def compute_pocket(row: dict) -> dict:
    list_price_annual = normalize_to_annual(
        float(row["list_price"]), row["cadence"]
    )
    discount_steps = json.loads(row.get("discount_steps_json", "[]"))
    implementation_fee = float(row.get("implementation_fee", 0))
    credits_applied = float(row.get("credits_applied", 0))
    payment_terms_days = int(row.get("payment_terms_days", 30))

    # Apply each discount step sequentially (multiplicative) so the
    # cumulative impact mirrors real-world stacked discounting.
    running_price = list_price_annual
    leak_by_step = []
    for step in discount_steps:
        before = running_price
        running_price *= 1 - float(step["pct"])
        leak_by_step.append({
            "name": step["name"],
            "pct": float(step["pct"]),
            "reason": step.get("reason", ""),
            "dollar_leak": before - running_price,
        })

    # Add implementation fee (positive — adds back to pocket).
    running_price += implementation_fee

    # Subtract credits + payment-terms carrying cost.
    pt_cost = payment_terms_cost(running_price, payment_terms_days)
    running_price -= credits_applied
    running_price -= pt_cost

    return {
        "customer_id": row["customer_id"],
        "list_price_annual": round(list_price_annual, 2),
        "pocket_price_annual": round(running_price, 2),
        "total_leak": round(list_price_annual - running_price, 2),
        "leak_pct": round(
            (list_price_annual - running_price) / list_price_annual * 100, 2
        ),
        "leak_by_step": leak_by_step,
        "implementation_fee": implementation_fee,
        "credits_applied": credits_applied,
        "payment_terms_carrying_cost": round(pt_cost, 2),
    }


def aggregate_cohort(per_customer: list) -> dict:
    if not per_customer:
        return {}

    list_prices = [c["list_price_annual"] for c in per_customer]
    pocket_prices = [c["pocket_price_annual"] for c in per_customer]
    leaks = [c["total_leak"] for c in per_customer]
    leak_pcts = [c["leak_pct"] for c in per_customer]

    # Aggregate leak by step name across all customers.
    step_totals = {}
    step_counts = {}
    step_pcts = {}
    for c in per_customer:
        for s in c["leak_by_step"]:
            step_totals[s["name"]] = step_totals.get(s["name"], 0) + s["dollar_leak"]
            step_counts[s["name"]] = step_counts.get(s["name"], 0) + 1
            step_pcts.setdefault(s["name"], []).append(s["pct"])

    leak_ranking = sorted(
        [
            {
                "step": name,
                "total_dollar_leak": round(total, 2),
                "customers_affected": step_counts[name],
                "customers_affected_pct": round(
                    step_counts[name] / len(per_customer) * 100, 1
                ),
                "mean_pct_when_applied": round(
                    statistics.mean(step_pcts[name]) * 100, 2
                ),
            }
            for name, total in step_totals.items()
        ],
        key=lambda x: -x["total_dollar_leak"],
    )

    return {
        "n_customers": len(per_customer),
        "list_price_total": round(sum(list_prices), 2),
        "pocket_price_total": round(sum(pocket_prices), 2),
        "total_leak_dollar": round(sum(leaks), 2),
        "total_leak_pct": round(
            sum(leaks) / sum(list_prices) * 100, 2
        ) if sum(list_prices) > 0 else 0,
        "list_price_mean": round(statistics.mean(list_prices), 2),
        "list_price_median": round(statistics.median(list_prices), 2),
        "pocket_price_mean": round(statistics.mean(pocket_prices), 2),
        "pocket_price_median": round(statistics.median(pocket_prices), 2),
        "leak_pct_mean": round(statistics.mean(leak_pcts), 2),
        "leak_pct_median": round(statistics.median(leak_pcts), 2),
        "leak_ranking": leak_ranking,
        "top_3_leaks": leak_ranking[:3],
    }


def summary_lines(cohort: dict) -> list:
    lines = [
        f"Customers analyzed: {cohort.get('n_customers', 0)}",
        f"Total list price (cohort): ${cohort.get('list_price_total', 0):,.2f}",
        f"Total pocket price (cohort): ${cohort.get('pocket_price_total', 0):,.2f}",
        f"Total leak: ${cohort.get('total_leak_dollar', 0):,.2f} "
        f"({cohort.get('total_leak_pct', 0)}%)",
        "",
        "Top 3 leak sources:",
    ]
    for i, leak in enumerate(cohort.get("top_3_leaks", []), 1):
        lines.append(
            f"  {i}. {leak['step']}: ${leak['total_dollar_leak']:,.2f} "
            f"({leak['customers_affected_pct']}% of customers, "
            f"mean {leak['mean_pct_when_applied']}%)"
        )
    return lines


def main():
    p = argparse.ArgumentParser(
        description="Pocket-price waterfall calculator",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--file", help="CSV file of customer data (e.g. gtm/waterfall.csv)")
    p.add_argument("--input", dest="file", help=argparse.SUPPRESS)
    p.add_argument("--stdin", action="store_true", help="Read the CSV from stdin")
    p.add_argument("--json", dest="format", action="store_const", const="json",
                   help="Print one JSON object (the default)")
    p.add_argument("--text", dest="format", action="store_const", const="text",
                   help="Print human text instead of JSON")
    p.add_argument("--format", dest="format", choices=["json", "text"],
                   help="Output format (default: json)")
    p.add_argument("--output", help="Write the output to this path instead of stdout")
    p.add_argument(
        "--print-summary",
        action="store_true",
        help="Print human-readable summary to stderr",
    )
    p.set_defaults(format="json")
    args = p.parse_args()

    if args.stdin and args.file:
        fail_input("pass --file or --stdin, not both")
    if args.stdin:
        text = read_stdin_text()
    elif args.file:
        text = read_text(Path(args.file))
    else:
        fail_input("pass --file or --stdin")

    per_customer = []
    reader = csv.DictReader(text.splitlines())
    for line_no, row in enumerate(reader, start=2):
        try:
            per_customer.append(compute_pocket(row))
        except (ValueError, KeyError, TypeError, AttributeError,
                ZeroDivisionError, json.JSONDecodeError):
            print(
                f"Skipping row {line_no}: bad number or missing column",
                file=sys.stderr,
            )

    cohort = aggregate_cohort(per_customer)
    refused = not per_customer

    result = {
        "per_customer": per_customer,
        "cohort": cohort,
        "next": NEXT_REFUSED if refused else NEXT_OK,
    }
    if refused:
        result["fixes"] = [
            "give each row customer_id, list_price, cadence (monthly or annual), "
            "and discount_steps_json as a JSON list"
        ]

    if args.format == "json":
        rendered = json.dumps(result, indent=2)
    else:
        lines = [] if refused else summary_lines(cohort)
        if refused:
            lines.append(f"- no usable customer row → {result['fixes'][0]}")
        lines.append(f"Next: {result['next']}")
        rendered = "\n".join(lines)
    if args.output:
        write_output(args.output, rendered)
    else:
        print(rendered)

    if args.print_summary:
        print("\n— Pocket-Price Waterfall Summary —", file=sys.stderr)
        print("\n".join(summary_lines(cohort)), file=sys.stderr)
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
