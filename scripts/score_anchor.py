#!/usr/bin/env python3
"""Score a pricing anchor: the number the buyer sees before the price.

Stdlib only. No network. Reads the draft you hand it and nothing else.

  python3 scripts/score_anchor.py --file gtm/anchor.json
  python3 scripts/score_anchor.py --stdin
  python3 scripts/score_anchor.py --file examples/anchor-good.json --json

The draft is the anchor block from anchor mode:

  {"frame": "inertia",
   "anchor": {"amount": 343200, "period": "year",
              "source": "gtm/offer-stack.json pain total, from the discovery call"},
   "price": {"amount": 4000, "period": "month"},
   "anchor_before_price": true,
   "headline": "...", "subhead": "...", "guarantee": "...",
   "was_price": {"amount": 6000, "period": "month",
                 "evidence": "offered at $6,000/mo from 2026-03-01 to 2026-09-30"}}

frame is inertia, opportunity, replacement or competitor. was_price is
optional; leave it out unless you show a struck-through former price.

Refused: an anchor with no number or no source, an anchor no bigger
than the price, the price shown before the anchor, a competitor frame
with no reason, "cheaper than" copy, cost-plus copy, a headline over 14
words or subhead over 22, a subhead with no number, a missing,
satisfaction-only or over-30-word guarantee, and a former price with no
evidence it was really charged.

Exit codes: 0 pass, 1 refused (fix the draft), 2 unreadable input.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MAX_INPUT_BYTES = 2_000_000
FRAMES = ("inertia", "opportunity", "replacement", "competitor")
PER_YEAR = {"one-time": 1, "year": 1, "quarter": 4, "month": 12, "week": 52}
HEADLINE_MAX = 14
SUBHEAD_MAX = 22
GUARANTEE_MAX = 30
CHEAPER_RE = re.compile(
    r"\bcheaper than\b|\b\d+% (?:less|cheaper|lower) than\b|\blower price than\b|\bsave \$?\d[\d,]* (?:vs|versus|over)\b",
    re.I,
)
COST_PLUS_RE = re.compile(r"\bcost[- ]plus\b|\bour costs?\b|\bour margin\b|\bmarkup\b", re.I)
SATISFACTION = (
    "if not satisfied",
    "if you're not satisfied",
    "if you are not satisfied",
    "satisfaction guaranteed",
    "100% satisfaction",
    "no questions asked",
    "if you don't love it",
)
DIGIT_RE = re.compile(r"\d")


def fail_input(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def read_payload(args: argparse.Namespace) -> dict:
    if bool(args.file) == bool(args.stdin):
        fail_input("pass --file or --stdin")
    if args.stdin:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
    else:
        path = Path(args.file)
        if not path.is_file():
            fail_input(f"file not found: {path}")
        if path.stat().st_size > MAX_INPUT_BYTES:
            fail_input("file is too large")
        raw = path.read_bytes()
    if len(raw) > MAX_INPUT_BYTES:
        fail_input("input is too large")
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        fail_input("input is not UTF-8 JSON")
    if not isinstance(data, dict):
        fail_input("draft is not a JSON object")
    return data


def text(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def yearly(block: object) -> float | None:
    if not isinstance(block, dict):
        return None
    amount = block.get("amount")
    period = text(block.get("period")).lower() or "year"
    if isinstance(amount, bool) or not isinstance(amount, (int, float)) or amount <= 0:
        return None
    if period not in PER_YEAR:
        return None
    return float(amount) * PER_YEAR[period]


def word_count(line: str) -> int:
    return len(line.split())


def score(data: dict) -> dict:
    fixes: list[str] = []
    frame = text(data.get("frame")).lower()
    if frame not in FRAMES:
        fixes.append(f"frame is {frame or 'missing'} → pick one of {', '.join(FRAMES)}; start with inertia")
    elif frame == "competitor" and not text(data.get("competitor_reason")):
        fixes.append(
            "the frame is competitor cost, the weakest in the stack → find what the buyer does today"
            " and what it costs (inertia), or write competitor_reason saying why no other frame is true"
        )

    anchor = data.get("anchor")
    anchor_year = yearly(anchor)
    if anchor_year is None:
        fixes.append(
            "the anchor has no number → put the yearly cost of the status quo on the page,"
            " e.g. the pain total from gtm/offer-stack.json"
        )
    elif not text(anchor.get("source")):
        fixes.append("the anchor has no source → say where the number came from: the buyer, a call, a file")

    price_year = yearly(data.get("price"))
    if price_year is None:
        fixes.append("price has no amount or period → give both, e.g. {\"amount\": 4000, \"period\": \"month\"}")
    elif anchor_year is not None and anchor_year <= price_year:
        fixes.append(
            "the anchor is no bigger than the price, so it anchors the wrong way"
            " → find the larger cost the buyer carries today"
        )

    if data.get("anchor_before_price") is not True:
        fixes.append("the price shows before the anchor → put the anchor block above the tier cards")

    headline = text(data.get("headline"))
    subhead = text(data.get("subhead"))
    guarantee = text(data.get("guarantee"))
    if not headline:
        fixes.append("no headline → one or two lines on the chosen frame, loss-coded if you can")
    elif word_count(headline) > HEADLINE_MAX:
        fixes.append(f"headline is {word_count(headline)} words → cut it to {HEADLINE_MAX} or fewer")
    if not subhead:
        fixes.append("no subhead → one line that puts the number on the frame")
    else:
        if word_count(subhead) > SUBHEAD_MAX:
            fixes.append(f"subhead is {word_count(subhead)} words → cut it to {SUBHEAD_MAX} or fewer")
        if not DIGIT_RE.search(subhead):
            fixes.append("subhead has no number → put the anchor figure in it")

    copy = " ".join((headline, subhead, guarantee))
    if CHEAPER_RE.search(copy):
        fixes.append("the copy compares on price with a competitor → anchor on what the buyer loses today instead")
    if COST_PLUS_RE.search(copy):
        fixes.append("the copy explains price from your costs → the buyer does not care what it costs you; anchor on their cost")

    if not guarantee:
        fixes.append("no guarantee → one sentence tied to an outcome and a date, with a bounded cost to you")
    else:
        if word_count(guarantee) > GUARANTEE_MAX:
            fixes.append(f"guarantee is {word_count(guarantee)} words → cut it to {GUARANTEE_MAX} or fewer")
        if any(p in guarantee.lower() for p in SATISFACTION) and not DIGIT_RE.search(guarantee):
            fixes.append("the guarantee rests on satisfaction → tie it to an outcome you can check by a date")

    was = data.get("was_price")
    if was is not None:
        if yearly(was) is None:
            fixes.append("was_price has no amount or period → give both, or drop the struck-through price")
        elif not text(was.get("evidence") if isinstance(was, dict) else ""):
            fixes.append(
                "a former price with no evidence → show it only if you openly charged it for a real"
                " period (US FTC 16 CFR 233.1); write the dates in evidence, or drop it"
            )

    ratio = ""
    if anchor_year and price_year and anchor_year > price_year:
        ratio = f"anchor {anchor_year:,.0f} a year against price {price_year:,.0f} a year ({anchor_year / price_year:.1f}x)"
    passed = not fixes
    nxt = (
        "Next: /pricing:pricing tiers (design the tier cards under the anchor)"
        if passed
        else "Next: fix the lines above and run this again."
    )
    return {"pass": passed, "frame": frame, "ratio": ratio, "fixes": fixes, "next": nxt}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="score_anchor",
        description="Score the anchor block above a pricing page's tier cards.",
        epilog="Example: python3 scripts/score_anchor.py --file examples/anchor-good.json",
    )
    parser.add_argument("--file", help="path to gtm/anchor.json")
    parser.add_argument("--stdin", action="store_true", help="read the draft from stdin")
    parser.add_argument("--json", action="store_true", help="print one JSON object")
    args = parser.parse_args(argv)

    result = score(read_payload(args))
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["ratio"]:
            print(result["ratio"])
        if result["pass"]:
            print(f"pass: {result['frame']} anchor, quantified, sourced, shown before the price")
        else:
            print(f"refused: {len(result['fixes'])} fix(es)")
            for fix in result["fixes"]:
                print(f"- {fix}")
        print(result["next"])
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
