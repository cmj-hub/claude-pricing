---
name: pricing
description: >
  B2B pricing surgery: diagnose willingness-to-pay across PSPs, pick the
  value metric, build a reference-frame stack (inertia / opportunity
  cost / replacement cost / competitor), design a three-tier contrast
  set with a real decoy, apply loss aversion to pricing copy, plug
  discount leaks with a pocket-price waterfall, and run quarterly
  pricing reviews. Anchors on Hermann Simon: a 1% price improvement is
  ~11% profit on typical B2B economics. Use when the operator asks
  about pricing strategy, raising prices, pricing tiers, price testing,
  willingness to pay, value metric, discounts, pocket price, decoy or
  anchor pricing, renewal or expansion pricing, outcome-tied
  guarantees, or a pricing review. Not for defining the Pain Signal
  Profile (use psp), writing the whole landing page (use
  landing-page), or the give-first first email (use sales-offer).
allowed-tools: Read Write Grep Glob
license: MIT
models: ""

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
| `psp` | `customer.psps[]`; if empty, the shared `psp` block written by the psp pack | "Series-B SaaS, demand-gen lead, pipeline gap" |
| `currentTiers` | Operator's pricing page | "$99 / $299 / $999 monthly" |
| `valueMetric` | What scales with customer success | "Active records / API calls / seats / outcomes" |
| `wtpDistribution` | Discovered via Van Westendorp / Gabor-Granger / conjoint | "P10=$50, P50=$200, P90=$800/mo" |
| `referenceAnchor` | Strongest plausible reference frame for this segment | "Inertia: 'building it in-house' at $80K/yr fully-loaded" |
| `discountWaterfall` | Pocket-price waterfall steps | "List → ramp → volume → bundle → annual → effective" |
| `riskTier` | Decision stakes (review-level required) | "Routine / Material / Strategic" |

If any are missing for a real recommendation, ask — don't fabricate.
If neither `customer.psps[]` nor `psp` exists, say the psp pack
produces it (`/psp:psp`; install with
`/plugin install psp@gtm-operator-skills`). Do not invent a PSP.

## Works with the suite

This is step 6 of the GTM operator suite (`/plugin marketplace add cmj-hub/gtm-operator-skills`).

- **Reads:** `customer.psps` (fallback: the `psp` block) and `icp` from `brand-config.json` if present.
- **Writes:** `customer` and `pricing`. Merge at the field level; never overwrite another pack's keys.
- **Before this:** psp (`/psp:psp`), when no PSP exists yet.
- **After this:** landing-page (`/landing-page:page`), when the tiers are set; sales-offer (`/sales-offer:cold-offer`), when the price goes into a give-first offer.

If a companion pack is not installed, name it and its install line (`/plugin install <name>@gtm-operator-skills`); do not do its job inline.

## References

Load these on demand for deeper context:

- [Pricing framework](references/pricing-framework.md) — The full JMC pricing surgery framework
- [Banned patterns](references/pricing-banned-patterns.md) — Pricing moves that fail predictably
- [Lineage](references/pricing-lineage.md) — Simon / Kahneman / Ariely / Christensen / Ramanujam
- [Reference-frame stack](references/pricing-framework.md#the-reference-frame-stack) — Strongest-to-weakest anchor types
- [Value-metric engineering](references/pricing-framework.md#value-metric-engineering) — Common B2B value-metric patterns + failure modes
- [Three-tier contrast set](references/pricing-framework.md#three-tier-contrast-set-architecture) — Asymmetric dominance in three-tier design
- [SOUL.md](../SOUL.md) — Operator voice template (pricing section)

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

