<p align="center">
  <img src="./assets/header.svg" alt="claude-pricing — B2B pricing as a surgical discipline" width="100%">
</p>

# claude-pricing

> Hermann Simon showed pricing is the highest-leverage lever in B2B — a 1% price improvement is ~11% profit on typical B2B economics.

Pricing surgery treats price as the highest-leverage B2B lever: diagnose willingness-to-pay, pick the value metric, set a reference frame, build a three-tier contrast set, then plug discount leaks. A 1% price improvement is ~11% profit on typical B2B economics (Simon).

The build guide teaches the framework to a human. This pack teaches the same framework to an agent.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/cmj-hub/claude-pricing?style=social)](https://github.com/cmj-hub/claude-pricing)
![No paid APIs](https://img.shields.io/badge/paid%20APIs-none-success)
![Install](https://img.shields.io/badge/install-npx%20skills-blue)

<p align="center">
  <img src="./assets/demo.gif" alt="claude-pricing — terminal demo of the decoy validator" width="100%">
</p>

`decoy_validator.py` on a healthy three-tier set scores **≥85**. A two-tier mixed-unit set scores **<60**. Pocket-price waterfall ranks discount leaks by margin. No paid APIs.

## Install

Two commands. Works in Claude Code, Cursor, Codex, Grok, Copilot, Windsurf, Cline, OpenCode, Antigravity, Goose, Continue, Roo, and the rest of the [skills CLI](https://skills.sh) agent list.

```bash
npx skills add cmj-hub/claude-pricing --all -g --full-depth
```

```text
/plugin marketplace add cmj-hub/claude-pricing
/plugin install pricing
```

The first line is the cross-harness install. The second is Claude Code's plugin (slash commands + reviewer agents).

npm (from GitHub — this pack is not on npmjs.com):

```bash
npm install github:cmj-hub/claude-pricing
npx jmc-pricing
```

`npx jmc-pricing` runs the same installer as `curl` below.

```bash
curl -fsSL https://raw.githubusercontent.com/cmj-hub/claude-pricing/main/install.sh | bash
```

Windows: `iwr https://raw.githubusercontent.com/cmj-hub/claude-pricing/main/install.ps1 -useb | iex`

## What you walk out with in 15 minutes

Artifact: `examples/tiers-healthy.json`. Run the decoy validator on the sample three-tier set, then drop in yours.

```bash
python3 scripts/decoy_validator.py --tiers examples/tiers-healthy.json
python3 scripts/decoy_validator.py --tiers examples/tiers-broken.json
```

One loop. One ICP. Example data. Then do yours.

## What this pack will not do

- It will not change live prices.
- It will not run a customer survey for you.
- It will not adjudicate a tribunal or a quarterly review on the first run.
- It is not "raise prices 15%." Diagnose first.

This pack drafts and scores. It will not pick this quarter's PSP, ingest your CRM, or update when Gmail changes the spam window. That is the course + Operator Pass: the catalog that keeps moving, the tools that stay calibrated, the Friday room where you bring the artifact.

## Also in the pack

| Piece | Job |
|---|---|
| `pricing` orchestrator | Diagnose / tiers / waterfall / route |
| `scripts/decoy_validator.py` | Asymmetric dominance on a three-tier set |
| `scripts/pocket_price_waterfall.py` | Discount-leak ranking |
| `scripts/wtp_distribution.py` | Van Westendorp thresholds (optional; not the first loop) |

Sub-skills stay in the repo. First run is the loop above, not the operating system.

## Is this just "raise prices 15%"?

No. Leading with a blanket raise hemorrhages trust and still leaks pocket price. Diagnose WTP, value metric, and discount leaks first. Then cut.

## Do I need survey data?

No for the first loop. The decoy validator runs on a three-tier JSON file. Van Westendorp is in the pack when you have responses; it is not a gate.

## Does this change live prices?

No. It scores and recommends. Shipping a price change, sales enablement, and grandfathering is your motion — or a Build Partnership.

## Suite, course, Operator Pass

- Suite: [https://jaymountconsulting.com/skills](https://jaymountconsulting.com/skills)
- Course: [Pricing Surgery](https://jaymountconsulting.com/learn/courses/pricing-surgery)
- Operator Pass: [https://jaymountconsulting.com/operator-pass](https://jaymountconsulting.com/operator-pass)

Founder: $97/mo billed annually ($1,164/yr), locked for life if bought before October 31, 2026. After that: $197/mo billed annually ($2,364/yr), no lock.

## Companion packs

- **[Pain Signal Profile](https://github.com/cmj-hub/claude-psp)** — `claude-psp`
- **[Early Value Proposition](https://github.com/cmj-hub/claude-evp)** — `claude-evp`
- **[Signal-anchored cold email](https://github.com/cmj-hub/claude-cold-email)** — `claude-cold-email`
- **[Four-pillar founder brand](https://github.com/cmj-hub/claude-founder-brand)** — `claude-founder-brand`
- **[Breakthrough Advertising (Schwartz)](https://github.com/cmj-hub/claude-breakthrough-advertising)** — `claude-breakthrough-advertising`
- **[Johanson / Stanley tutorial email](https://github.com/cmj-hub/claude-johanson-stanley)** — `claude-johanson-stanley`

## License

MIT. See [LICENSE](./LICENSE).

## About

Built by [Jay Mount Consulting](https://jaymountconsulting.com). Public build: [https://jaymountconsulting.com/build](https://jaymountconsulting.com/build). Skill suite: [https://jaymountconsulting.com/skills](https://jaymountconsulting.com/skills).
