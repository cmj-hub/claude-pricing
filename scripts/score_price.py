#!/usr/bin/env python3
"""
score_price.py — refuse a price that has no value metric behind it.

Checks one pricing draft before it goes on a page or into an offer:

  1. A price is never shown without a value metric (the unit it is per)
  2. The contrast set is named (the tiers or alternatives the buyer compares)
  3. The tribunal verdict is written down (what you decided and why)

Every failing rule is reported, not just the first.

Usage:
  python3 scripts/score_price.py --file gtm/price.json
  python3 scripts/score_price.py --stdin < gtm/price.json
  python3 scripts/score_price.py --file gtm/price.json --json

Draft JSON format:
  {
    "price": 1200,
    "value_metric": "per active record",
    "contrast_set": ["Starter", "Growth", "Scale"],
    "tribunal": "Hold the list price until the metric is on the page"
  }

`contrast_set` items may be strings or objects with a `name`.
`tribunal` may be a string or a list of strings.

Every refusal line reads `- <what is wrong> → <what to change>`. The last
line names the next step. `--json` adds `fixes` (parallel to `reasons`)
and `next`; the other keys are unchanged.

Exit codes: 0 ok, 1 refused, 2 bad input. Bad input is never echoed.

Zero dependencies. Python 3.8+. No network.
"""
import argparse
import json
import sys
from pathlib import Path


MAX_INPUT_BYTES = 2_000_000

NEXT_OK = "/landing-page:page (put the price on the page with its unit)"
NEXT_REFUSED = "fix the lines above and run this again."
EPILOG = """example:
  python3 scripts/score_price.py --file examples/price-good.json
  python3 scripts/score_price.py --file examples/price-no-metric.json --json

exit codes: 0 ok, 1 refused, 2 bad input"""

FIXES = {
    "a price with no metric": "add value_metric, the unit the price is per (e.g. \"per active record\")",
    "no value metric": "add value_metric, the unit the price is per (e.g. \"per active record\")",
    "no contrast set": "add contrast_set, the tiers or alternatives the buyer compares",
    "no tribunal verdict": "add a tribunal verdict: what you decided and why, in one line",
}


def fail_input(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def read_text(path: Path) -> str:
    try:
        if not path.exists():
            fail_input("file not found")
        if not path.is_file():
            fail_input("not a file")
        if path.stat().st_size > MAX_INPUT_BYTES:
            fail_input("file is too large")
        raw = path.read_bytes()
    except SystemExit:
        raise
    except OSError:
        fail_input("cannot read file")
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        fail_input("file is not UTF-8 text")


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


def parse_json_text(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        fail_input("invalid JSON")


def nonempty_text(value) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return ""


def has_price(value) -> bool:
    if value is None or isinstance(value, bool):
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return len(value) > 0
    return True


def contrast_items(value) -> list:
    """Names in the contrast set, or [] if any item is blank or malformed."""
    if not isinstance(value, list) or not value:
        return []
    items = []
    for item in value:
        if isinstance(item, dict):
            item = item.get("name")
        name = nonempty_text(item)
        if not name:
            return []
        items.append(name)
    return items


def tribunal_text(value) -> str:
    if isinstance(value, list) and value:
        parts = [nonempty_text(item) for item in value]
        return "; ".join(parts) if all(parts) else ""
    return nonempty_text(value)


def check(data: dict) -> dict:
    metric = nonempty_text(data.get("value_metric"))
    contrast = contrast_items(data.get("contrast_set"))
    tribunal = tribunal_text(data.get("tribunal"))
    priced = has_price(data.get("price"))

    reasons = []
    if priced and not metric:
        reasons.append("a price with no metric")
    elif not metric:
        reasons.append("no value metric")
    if not contrast:
        reasons.append("no contrast set")
    if not tribunal:
        reasons.append("no tribunal verdict")

    return {
        "ok": not reasons,
        "reasons": reasons,
        "fixes": [FIXES[r] for r in reasons],
        "value_metric": metric,
        "contrast_set": contrast,
        "tribunal": tribunal,
        "has_price": priced,
        "next": NEXT_REFUSED if reasons else NEXT_OK,
    }


def format_text(result: dict, price) -> str:
    if not result["ok"]:
        lines = ["refused:"]
        lines += [f"- {r} → {f}" for r, f in zip(result["reasons"], result["fixes"])]
        lines.append(f"Next: {NEXT_REFUSED}")
        return "\n".join(lines)
    lines = [
        f"value metric: {result['value_metric']}",
        "contrast set: " + ", ".join(result["contrast_set"]),
        f"tribunal: {result['tribunal']}",
    ]
    if result["has_price"]:
        lines.append(f"price: {price} {result['value_metric']}")
    lines.append(f"Next: {NEXT_OK}")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(
        description="Refuse a price with no value metric",
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--file", help="Path to a JSON pricing draft (e.g. gtm/price.json)")
    p.add_argument("--stdin", action="store_true", help="Read the JSON draft from stdin")
    p.add_argument("--json", action="store_true", help="Print one JSON object instead of text")
    args = p.parse_args()

    if args.file and args.stdin:
        fail_input("pass --file or --stdin, not both")
    if args.stdin:
        data = parse_json_text(read_stdin_text())
    elif args.file:
        data = parse_json_text(read_text(Path(args.file)))
    else:
        fail_input("pass --file or --stdin")
    if not isinstance(data, dict):
        fail_input("JSON must be an object")

    result = check(data)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_text(result, data.get("price")))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
