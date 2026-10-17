# Pricing anchoring: the context file

Load this with anchor mode. The reference-frame stack in [pricing-framework.md](pricing-framework.md) says which frame to pick. This file says how to put the anchor on the page so it holds, and what `score_anchor.py` checks.

## Contents

- What an anchor is
- The anchor comes first
- The anchor is a number with a source
- Same unit as the price
- Where the anchor number comes from
- A former price must be real
- What the scorer refuses
- Sources

## What an anchor is

An anchor is the first number a buyer sees, and the one they judge the price against. Tversky and Kahneman showed in 1974 that people's estimates move toward a number they saw first, even an arbitrary one. On a pricing page that number is yours to choose. Choose a true one.

The strongest anchor is what the buyer's current way of working costs them a year. The weakest is a competitor's price, because the buyer answers it with "I'll keep shopping."

## The anchor comes first

The buyer reads the anchor block before the tier cards. If the price comes first, the price is the anchor, and everything after it reads as a reason it is too high.

`anchor_before_price` is `true` only when the anchor block sits above the tiers on the page, the deck slide or the proposal.

## The anchor is a number with a source

"Teams waste hours on admin" anchors nothing. "Your reps spend 6,240 hours a year typing call notes" anchors at once, and the buyer can check it.

Every anchor carries where its number came from: the buyer on a call, their own export, a file. If the buyer gave you the number, it is theirs to believe. If you made it up, they will find out on the call.

## Same unit as the price

An anchor per year next to a price per month makes the buyer do the division, and most will not. Show both in the same unit, or say both: "$343,200 a year. $4,000 a month."

The scorer turns both into a yearly figure and refuses an anchor that is no bigger than the price. An anchor smaller than the price argues against you.

## Where the anchor number comes from

If the offer-stack pack has run, `gtm/offer-stack.json` already holds each pain's yearly cost and the total, each with a source. That total is the inertia anchor. Use the single biggest pain if the total mixes time and cash, and say "worth" for time, "costs" for cash.

If it has not run, ask anchor mode's discovery questions (what they do today, its loaded cost, the cost of another quarter of the same), or install the pack: `npx skills add cmj-hub/claude-offer-stack --all -g --full-depth`.

## A former price must be real

A struck-through "was $650, now $450" is an anchor too. In the US, the FTC's Guides Against Deceptive Pricing (16 CFR 233.1) say a former price is a fair comparison only if it was the actual price openly offered to the public, on a regular basis, for a reasonably substantial period. A price set high so it can be cut is called fictitious there.

So `was_price` needs `evidence`: the dates you charged it. No evidence, no strike-through. Other countries have their own rules; check yours.

## What the scorer refuses

- An anchor with no number, or no source.
- An anchor no bigger than the price, in yearly terms.
- The price shown before the anchor.
- A competitor frame with no `competitor_reason`.
- "Cheaper than", "30% less than" and similar price comparisons with a competitor.
- Copy that explains the price from your costs ("cost-plus", "our margin").
- A headline over 14 words, a subhead over 22, a subhead with no number.
- A missing guarantee, one over 30 words, or one that rests on satisfaction with no outcome.
- A `was_price` with no `evidence`.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_anchor.py --file gtm/anchor.json
```

## Sources

- Tversky, A. and Kahneman, D. (1974). Judgment under Uncertainty: Heuristics and Biases. Science 185(4157), 1124-1131. https://doi.org/10.1126/science.185.4157.1124
- US FTC, Guides Against Deceptive Pricing, 16 CFR 233.1, Former price comparisons. https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-233/section-233.1
