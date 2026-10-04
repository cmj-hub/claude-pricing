---
name: pricing
description: "B2B pricing surgery: willingness-to-pay, value metric, anchors, three tiers with a real decoy, discount leaks, tribunal, renewal and quarterly reviews. Use when the operator asks about pricing, raising prices, tiers, discounts, value metric, or a pricing audit. Not for the Pain Signal Profile (psp), the whole landing page (landing-page), or a give-first first email (sales-offer)."
argument-hint: "[status | setup | diagnose | audit | tiers | anchor | waterfall | value-metric | tribunal | review | renewal]"
allowed-tools: Read Write Grep Glob Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_price.py:*) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/decoy_validator.py:*) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/wtp_distribution.py:*) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/pocket_price_waterfall.py:*)
license: MIT
models: ""
---

# Pricing — JMC Pricing Surgery Skill

Comprehensive pricing orchestrator for B2B operators. Treats pricing
as a surgical discipline — small precise cuts in the right place
compound; sloppy cuts hemorrhage margin.

## Preflight (runs before every mode)

1. Read `brand-config.json` and `SOUL.md` at the project root if they exist.
2. If `operator` or `icp` is missing, say "Run `/gtm:setup` once for the whole suite" (the [setup mode](modes/setup.md) asks those inline when the gtm plugin is not installed).
3. If `pricing` is empty or `SOUL.md` has no pricing section, run the [setup mode](modes/setup.md) first, unless the operator passed `--no-config` (then warn that the output is generic).
4. Drafts this pack writes go in `gtm/` at the project root (create it if missing): `gtm/price.json`, `gtm/tiers.json`, `gtm/waterfall.csv`, `gtm/wtp.csv`.

## Modes

If `$ARGUMENTS` names a mode, go straight to it. If `$ARGUMENTS` is empty, run `status`. Otherwise match the operator's words below; if intent is still ambiguous, ask one clarifying question — never two.

Read the mode file with the Read tool and follow it.

| You say / argument | Mode file |
|---|---|
| `status`, no argument, "where do I start?", "what's next?" | [modes/status.md](modes/status.md) |
| `setup`, first run, no brand-config or SOUL.md | [modes/setup.md](modes/setup.md) |
| `diagnose`, "Should I raise my prices?", "where am I leaving money?" | [modes/diagnose.md](modes/diagnose.md) (then `tribunal` if material) |
| `audit`, "Audit my pricing program", "grade my pricing" | [modes/audit.md](modes/audit.md) |
| `tiers`, "Redesign my pricing page", decoy, three tiers | [modes/tiers.md](modes/tiers.md) |
| `anchor`, "How do I anchor my pricing?", pricing copy | [modes/anchor.md](modes/anchor.md) |
| `waterfall`, "My discounts are eating margin", pocket price | [modes/waterfall.md](modes/waterfall.md) |
| `value-metric`, "per-seat or per-something-else?" | [modes/value-metric.md](modes/value-metric.md) |
| `tribunal`, "Big pricing decision — help me decide" | [modes/tribunal.md](modes/tribunal.md) |
| `review`, "What should we check at the pricing review?" | [modes/review.md](modes/review.md) |
| `renewal`, "How do I price renewals / expansion?" | [modes/renewal.md](modes/renewal.md) |

Moved in 0.6.0: the eleven `pricing-*` sub-skills are now these modes. Type `/pricing:pricing <mode>`.

When a run finishes cleanly, say the next step: the next mode the status checklist names, or the next suite command (`/landing-page:page` once the tiers are set; `/sales-offer:cold-offer` when the price goes into a give-first offer).

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

## Variables (every mode uses these)

The pricing surgery discipline operates on these variables. Capture
once from `brand-config.json` + diagnostic output, reuse across all
modes:

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

## Score the price

Before a price goes on a page or into an offer, write it as
`gtm/price.json` (`price`, `value_metric`, `contrast_set`, `tribunal`) and run:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_price.py --file gtm/price.json
```

Exit 1 lists every reason it refused, each as `- what is wrong → what to
change`, then `Next: fix the lines above and run this again.` Fix each
one; never show a price without the unit it is per. Exit 0 ends with
the next suite step. Exit 2 is bad input. `--json` for the report.
Example drafts: `examples/price-good.json`, `examples/price-no-metric.json`.

All four scripts take `--file PATH` or `--stdin` and exit 0 ok, 1
refused, 2 bad input. `score_price.py` prints text by default; the
other three print JSON by default (`--text` for lines).

## Works with the suite

This is step 6 of the GTM operator suite (`/plugin marketplace add cmj-hub/gtm-operator-skills`).

- **Reads:** `customer.psps` (fallback: the `psp` block) and `icp` from `brand-config.json` if present.
- **Writes:** `customer` and `pricing`; drafts in `gtm/`. Merge at the field level; never overwrite another pack's keys.
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
- [SOUL.md](../../SOUL.md) — Operator voice template (pricing section)

## Specialist agents

- [`agents/pricing-reviewer`](../../agents/pricing-reviewer.md) — Pricing-page + tier scorer (0-100)
- [`agents/pricing-tribunal-judge`](../../agents/pricing-tribunal-judge.md) — Adjudicates pricing hypotheses against the verdict matrix

## Free hosted version

The same job runs in a browser, no install and no key:
[Pricing Page Lab](https://jaymountconsulting.com/tools/pricing-page-lab)

