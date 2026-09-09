---
name: pricing
description: >
  B2B pricing as a surgical discipline. Diagnose willingness-to-pay
  distribution across PSPs, engineer value-metric alignment, design
  three-tier contrast sets with decoy effect, build reference-frame
  stacks (inertia / opportunity cost / replacement cost / competitor),
  apply Prospect Theory loss aversion to pricing copy, run pocket-price
  waterfall analysis to plug discount leaks, and operate quarterly
  pricing reviews as the compounding moat. Anchors every recommendation
  on Hermann Simon's foundational frame: a 1% price improvement drives
  ~11% profit improvement on average B2B economics. Based on the JMC
  Pricing Surgery course (jaymountconsulting.com/learn). Triggers on:
  "pricing strategy", "raise prices", "pricing tiers", "price testing",
  "willingness to pay", "value metric", "pricing page", "discount",
  "pocket price", "decoy pricing", "anchor pricing", "loss aversion
  pricing", "B2B pricing", "SaaS pricing", "services pricing", "renewal
  pricing", "expansion pricing", "outcome-tied guarantee", "pricing
  review".
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
---

# Pricing — JMC Pricing Surgery Skill

Comprehensive pricing orchestrator for B2B operators. Treats pricing
as a surgical discipline — small precise cuts in the right place
compound; sloppy cuts hemorrhage margin.

## Quick Reference

| Slash | What it does |
|---|---|
| `/pricing` | Interactive mode — detect intent, route to a sub-skill |
| `/pricing diagnose` | Three-surface diagnostic: WTP distribution, value-metric, packaging |
| `/pricing audit` | 30-point pricing program audit → 0-100 score + top 3 levers |
| `/pricing tiers` | Three-tier design with decoy + anchor architecture |
| `/pricing anchor` | Reference-frame stack design for pricing copy |
| `/pricing waterfall` | Pocket-price waterfall — find where margin is leaking |
| `/pricing value-metric` | Pick the right price unit (per-seat / per-API / per-outcome) |
| `/pricing tribunal` | Capstone workflow for high-stakes pricing decisions |
| `/pricing review` | Quarterly pricing review cadence + agenda |

## Core principles (the JMC stance)

1. **Pricing is surgery, not strategy.** Diagnose first. Cut last.
   Operators who lead with "let's just raise prices 15%" hemorrhage
   margin and trust. Find the leak, then close it.
2. **A 1% price improvement = ~11% profit improvement** on average
   B2B economics. Pricing is the highest-leverage lever in the
   business and the one most operators give the least attention.
   (Hermann Simon, 50+ years of empirical work.)
3. **Inertia is the real competitor.** Buyers anchor on what they
   currently do — not on competitor prices. Beat the inertia frame,
   not the competitor frame.
4. **Loss aversion dominates size-of-win.** For the 95% of buyers
   not in cycle, de-risking the purchase matters more than the
   ceiling of upside. Kahneman + Tversky's Prospect Theory is
   load-bearing in pricing copy.
5. **Value-metric alignment beats price-point tuning.** The wrong
   unit (per-seat when the value is per-API-call) leaks more margin
   than any discount policy.
6. **Three-tier contrast-set with a real decoy** outperforms
   two-tier or four-tier in 80%+ of B2B SaaS / services tests.
   (Ariely, asymmetric dominance.)
7. **Discount discipline > headline price.** The pocket-price
   waterfall surfaces where margin is leaking after the line-item
   price. Plug the leaks before tuning the headline.
8. **Quarterly review prevents drift.** Pricing that doesn't get
   reviewed gets eroded. The operating practice IS the compounding
   moat.

## Workflow router

When invoked, detect the user's intent and route to a sub-skill:

| User says | Route to |
|---|---|
| "Should I raise my prices?" | `skills/pricing-diagnostic` (then `pricing-tribunal` if material) |
| "Redesign my pricing page" | `skills/pricing-contrast-set` |
| "My discounts are eating margin" | `skills/pricing-pocket-waterfall` |
| "Should this be per-seat or per-something-else?" | `skills/pricing-value-metric` |
| "How do I anchor my pricing?" | `skills/pricing-reference-frames` |
| "Audit my pricing program" | `skills/pricing-audit` |
| "Big pricing decision — help me decide" | `skills/pricing-tribunal` |
| "What should we check at the pricing review?" | `skills/pricing-quarterly-review` |
| "How do I price renewals / expansion?" | `skills/pricing-renewal-discipline` |

If intent is ambiguous, ask one clarifying question — never two.

## Variables (sub-skills inherit these)

The pricing surgery discipline operates on these variables. Capture
once from `brand-config.json` + diagnostic output, reuse across all
sub-skills:

| Variable | Source | Example |
|---|---|---|
| `psp` | Pain Signal Profile (from companion claude-psp pack) | "Series-B SaaS, demand-gen lead, pipeline gap" |
| `currentTiers` | Operator's pricing page | "$99 / $299 / $999 monthly" |
| `valueMetric` | What scales with customer success | "Active records / API calls / seats / outcomes" |
| `wtpDistribution` | Discovered via Van Westendorp / Gabor-Granger / conjoint | "P10=$50, P50=$200, P90=$800/mo" |
| `referenceAnchor` | Strongest plausible reference frame for this segment | "Inertia: 'building it in-house' at $80K/yr fully-loaded" |
| `discountWaterfall` | Pocket-price waterfall steps | "List → ramp → volume → bundle → annual → effective" |
| `riskTier` | Decision stakes (review-level required) | "Routine / Material / Strategic" |

If any are missing for a real recommendation, ask — don't fabricate.

## References

Load these on demand for deeper context:

- `references/pricing-framework.md` — The full JMC pricing surgery framework
- `references/pricing-banned-patterns.md` — Pricing moves that fail predictably
- `references/pricing-lineage.md` — Simon / Kahneman / Ariely / Christensen / Ramanujam
- `references/reference-frame-stack.md` — Strongest-to-weakest anchor types
- `references/value-metric-catalog.md` — Common B2B value-metric patterns + failure modes
- `references/decoy-effect-patterns.md` — Asymmetric dominance in three-tier design

## Sub-skills

- [`skills/pricing-kickoff`](../skills/pricing-kickoff) — Adaptive router; detects state + picks next-best step
- [`skills/pricing-onboarding`](../skills/pricing-onboarding) — Interactive setup → `brand-config.json` + `SOUL.md`
- [`skills/pricing-diagnostic`](../skills/pricing-diagnostic) — Three-surface diagnostic (WTP, value-metric, packaging)
- [`skills/pricing-audit`](../skills/pricing-audit) — 30-point pricing program audit
- [`skills/pricing-tribunal`](../skills/pricing-tribunal) — High-stakes pricing decision workflow (Hypothesize → Test → Adjudicate → Audit)
- [`skills/pricing-reference-frames`](../skills/pricing-reference-frames) — Anchor design + loss aversion application
- [`skills/pricing-contrast-set`](../skills/pricing-contrast-set) — Three-tier + decoy architecture
- [`skills/pricing-pocket-waterfall`](../skills/pricing-pocket-waterfall) — Discount-leak detection
- [`skills/pricing-value-metric`](../skills/pricing-value-metric) — Price unit selection
- [`skills/pricing-quarterly-review`](../skills/pricing-quarterly-review) — Operating cadence
- [`skills/pricing-renewal-discipline`](../skills/pricing-renewal-discipline) — Renewals + expansion as continuous surgery

## Specialist agents

- [`agents/pricing-reviewer`](../agents/pricing-reviewer.md) — Pricing-page + tier scorer (0-100)
- [`agents/pricing-tribunal-judge`](../agents/pricing-tribunal-judge.md) — Adjudicates pricing hypotheses against the verdict matrix

## Free hosted version

The same job runs in a browser, no install and no key:
[Pricing Page Lab](https://jaymountconsulting.com/tools/pricing-page-lab)

