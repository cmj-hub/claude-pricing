# Status mode

Read the pack's state, show the checklist, and name the one next step.

## Contents

- Activation
- The 9-step state machine
- Workflow
- Output format
- Self-check
- Related

The adaptive entry point. The operator runs `/pricing:pricing` and this
mode detects state, surfaces a state checklist, and routes to
the next step. Goal: never make the operator guess where to start.

## Activation

The main skill routes here when:

- User invokes `/pricing:pricing` with no arguments
- User asks "where do I start", "what's next", "first time using this"
- User asks "what should I do this quarter on pricing"

## The 9-step state machine

| # | Step | Detection | Next mode |
|---|---|---|---|
| 1 | brand-config + SOUL set up | `brand-config.json` + `SOUL.md` exist | the `setup` mode if either missing |
| 2 | Current tiers documented | `brand-config.json` has `pricing.currentTiers[]` populated | the `setup` mode (tier section) if missing |
| 3 | PSP defined | `brand-config.json` has `customer.psps[]` populated, or the shared `psp` block | psp pack (`/psp:psp`) if missing |
| 4 | WTP discovery done | `brand-config.json` has `pricing.wtpResearch.lastConducted` < 12 months ago | the `diagnose` mode if missing/stale |
| 5 | Value-metric chosen | `brand-config.json` has `pricing.valueMetric.unit` populated | the `value-metric` mode if missing |
| 6 | Reference anchor set | `brand-config.json` has `pricing.referenceAnchor.frame` populated | the `anchor` mode if missing |
| 7 | Pocket-price waterfall built | `brand-config.json` has `pricing.pocketWaterfall.steps[]` populated | the `waterfall` mode if missing |
| 8 | Three-tier contrast set designed | `brand-config.json` has `pricing.tiers.architecture` = "three-tier-decoy" | the `tiers` mode if missing |
| 9 | Quarterly review scheduled | `brand-config.json` has `pricing.review.nextScheduled` populated | the `review` mode if missing |

Steps 1-3 are blocking (everything depends on them). Steps 4-7 are
the diagnostic foundation. Steps 8-9 are the operating practice.

## Workflow

### 1. Detect state

Read `brand-config.json` and `SOUL.md` if present:

```bash
# Pseudo
[ -f brand-config.json ] && jq -r '.pricing // {}' brand-config.json
[ -f brand-config.json ] && jq -r '.customer.psps // .psp // empty' brand-config.json
[ -f SOUL.md ] && grep -q "^## My stance on pricing" SOUL.md
```

Also list the pack's drafts in `gtm/` (any of `gtm/price.json`,
`gtm/tiers.json`, `gtm/waterfall.csv`, `gtm/wtp.csv`). A draft that
exists counts as partial (🔶) for its step until its script exits 0.

For each of the 9 steps, mark ⬜ (not done), 🔶 (partial), or ✅ (done).

### 2. Surface state checklist

Output a readable state report:

```
Pricing setup — state check
─────────────────────────────────────────────────────────────────

1. ✅ brand-config + SOUL set up
2. ✅ Current tiers documented ($99 / $299 / $999 monthly)
3. ⬜ Pain Signal Profile defined          ← START HERE
4. ⬜ Willingness-to-pay discovery done
5. ⬜ Value-metric chosen
6. ⬜ Reference anchor set
7. ⬜ Pocket-price waterfall built
8. ⬜ Three-tier contrast set designed
9. ⬜ Quarterly pricing review scheduled

Recommended next step: Step 3 — define your Pain Signal Profile(s).
Pricing decisions without a PSP anchor produce one-size-fits-none
tiers. The psp pack handles this in ~30 min: /psp:psp
(install: /plugin install psp@gtm-operator-skills).

Want to run the PSP workflow now? (y/n)
```

### 3. Route based on state

| State | Action |
|---|---|
| Step 1 missing | Route to the `setup` mode for full setup |
| Steps 2-3 missing | Route to the `setup` mode (tier section) + point at `/psp:psp` |
| Steps 4-7 partial | Route to the lowest-numbered missing diagnostic step |
| Steps 8-9 missing | Route to the `tiers` mode or the `review` mode |
| Everything done | Name the next suite step: `/landing-page:page` (tiers go on the page) or `/sales-offer:cold-offer` (price goes into a give-first offer); offer the `review` mode for the quarter |

### 4. Don't generate without state

If state isn't loaded and the operator says "just write me a pricing
page" — refuse, route to the `setup` mode. Generic pricing is worse than
no pricing.

The operator can override with `--no-config` flag for sandbox runs;
warn that the output will be generic.

## Output format

Always include:

- The 9-step state checklist
- Which step is YOU ARE HERE
- One specific next action (with time estimate)
- A binary y/n to start that step now

Never list all 9 modes as options ("pick one"). Always lead
with the recommended next step. The operator can override.

## Self-check

Before delivering the kickoff:

- [ ] Read `brand-config.json` and `SOUL.md` (or noted they're missing)
- [ ] All 9 steps checked
- [ ] Identified YOU ARE HERE
- [ ] Recommended ONE next action, not a menu
- [ ] Time estimate provided

## Related

- [SKILL.md](../SKILL.md) — the orchestrator
- [references/pricing-framework.md](../references/pricing-framework.md) — full framework
- [modes/setup.md](setup.md) — what runs if state is empty
