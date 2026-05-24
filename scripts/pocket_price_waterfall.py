#!/usr/bin/env python3
"""
Pocket-price waterfall — discount-leak calculator.

Reads customer-level discount line-item data + computes the pocket
price per customer and the cohort-level waterfall. Ranks discount
steps by total margin impact and identifies the top 3 leak sources.

Usage:
  python3 scripts/pocket_price_waterfall.py --input customers.csv --output waterfall.json

CSV format (header row required):
  customer_id,list_price,cadence,discount_steps_json,payment_terms_days,implementation_fee,credits_applied

  - list_price: float, in the cadence currency
  - cadence: "monthly" or "annual" (annualized for waterfall)
  - discount_steps_json: JSON array of {name, pct, reason}
  - payment_terms_days: int (NET-30, NET-60, etc.)
  - implementation_fee: float (one-time)
  - credits_applied: float (annual)

Output: JSON with per-customer breakdown + cohort aggregates + leak ranking.

Zero dependencies. Python 3.8+.
"""
import argparse
import csv
import json
import statistics
import sys
from pathlib import Path


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


def main():
    p = argparse.ArgumentParser(description="Pocket-price waterfall calculator")
    p.add_argument("--input", required=True, help="CSV file of customer data")
    p.add_argument("--output", help="Output JSON path (default: stdout)")
    p.add_argument(
        "--print-summary",
        action="store_true",
        help="Print human-readable summary to stderr",
    )
    args = p.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print(f"Input file not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    per_customer = []
    with in_path.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                per_customer.append(compute_pocket(row))
            except (ValueError, KeyError, json.JSONDecodeError) as e:
                print(
                    f"Skipping customer {row.get('customer_id', '?')}: {e}",
                    file=sys.stderr,
                )

    cohort = aggregate_cohort(per_customer)

    result = {
        "per_customer": per_customer,
        "cohort": cohort,
    }

    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2))
    else:
        print(json.dumps(result, indent=2))

    if args.print_summary:
        print("\n— Pocket-Price Waterfall Summary —", file=sys.stderr)
        print(
            f"Customers analyzed: {cohort.get('n_customers', 0)}",
            file=sys.stderr,
        )
        print(
            f"Total list price (cohort): ${cohort.get('list_price_total', 0):,.2f}",
            file=sys.stderr,
        )
        print(
            f"Total pocket price (cohort): ${cohort.get('pocket_price_total', 0):,.2f}",
            file=sys.stderr,
        )
        print(
            f"Total leak: ${cohort.get('total_leak_dollar', 0):,.2f} "
            f"({cohort.get('total_leak_pct', 0)}%)",
            file=sys.stderr,
        )
        print(file=sys.stderr)
        print("Top 3 leak sources:", file=sys.stderr)
        for i, leak in enumerate(cohort.get("top_3_leaks", []), 1):
            print(
                f"  {i}. {leak['step']}: ${leak['total_dollar_leak']:,.2f} "
                f"({leak['customers_affected_pct']}% of customers, "
                f"mean {leak['mean_pct_when_applied']}%)",
                file=sys.stderr,
            )


if __name__ == "__main__":
    main()
