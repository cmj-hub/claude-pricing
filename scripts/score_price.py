#!/usr/bin/env python3
"""Score a pricing draft: value metric, contrast set, and tribunal.

Stdlib only. No network.

  python3 scripts/score_price.py --file draft.json
  python3 scripts/score_price.py --stdin
"""

from __future__ import annotations

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


def load_payload(args: argparse.Namespace) -> object:
    if args.file and args.stdin:
        fail_input("pass --file or --stdin, not both")
    if args.stdin:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            fail_input("input is too large")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            fail_input("input is not UTF-8 text")
    elif args.file:
        text = read_text(Path(args.file))
    else:
        fail_input("pass --file or --stdin")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        fail_input("invalid JSON")


def nonempty_text(value: object) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return ""


def has_price(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return len(value) > 0
    return True


def contrast_items(value: object) -> list[str]:
    if not isinstance(value, list) or not value:
        return []
    items: list[str] = []
    for item in value:
        if isinstance(item, str) and item.strip():
            items.append(item.strip())
        elif isinstance(item, dict):
            name = nonempty_text(item.get("name"))
            if name:
                items.append(name)
        else:
            return []
    return items if len(items) == len(value) else []


def main() -> int:
    parser = argparse.ArgumentParser(description="Score a pricing draft")
    parser.add_argument("--file", help="Path to a JSON object")
    parser.add_argument("--stdin", action="store_true", help="Read a JSON object from stdin")
    args = parser.parse_args()
    data = load_payload(args)
    if not isinstance(data, dict):
        fail_input("JSON must be an object")

    metric = nonempty_text(data.get("value_metric"))
    contrast = contrast_items(data.get("contrast_set"))
    tribunal = nonempty_text(data.get("tribunal"))
    if isinstance(data.get("tribunal"), list) and data["tribunal"]:
        parts = [nonempty_text(item) for item in data["tribunal"]]
        if all(parts):
            tribunal = "; ".join(parts)

    if has_price(data.get("price")) and not metric:
        print("a price with no metric")
        return 1

    if metric and contrast and tribunal:
        print(f"value metric: {metric}")
        print("contrast set: " + ", ".join(contrast))
        print(f"tribunal: {tribunal}")
        if has_price(data.get("price")):
            print(f"price: {data.get('price')}")
        return 0

    print("draft is incomplete")
    return 1


if __name__ == "__main__":
    sys.exit(main())
