<p align="center">
  <img src="./assets/header.svg" alt="claude-pricing — B2B pricing as a surgical discipline" width="100%">
</p>

# claude-pricing

> A 1% price cut is not a 1% problem. On typical B2B economics it is ~11% of profit (Simon).

Pricing surgery treats price as the highest-leverage B2B lever: diagnose willingness-to-pay, pick the value metric, set a reference frame, build a three-tier contrast set, then plug discount leaks.

"Just raise prices 15%" is not a diagnosis.
A two-tier page with mixed units is a leak you can see.

The sample healthy three-tier set in this repo scores **100**.
The broken set scores **10.5**.

`decoy_validator.py` is Python. No LLM. No paid API.

The build guide teaches the framework to a human. This pack teaches the same framework to an agent.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/cmj-hub/claude-pricing?style=social)](https://github.com/cmj-hub/claude-pricing)
![No paid APIs](https://img.shields.io/badge/paid%20APIs-none-success)
![Install](https://img.shields.io/badge/install-npx%20skills-blue)

<p align="center">
  <img src="./assets/demo.gif" alt="claude-pricing — terminal demo of the decoy validator" width="100%">
</p>

## Install

Two commands. Claude Code, Cursor, Codex, Grok, Copilot, Windsurf, Cline, OpenCode, and the rest of the [skills CLI](https://skills.sh) list.

```bash
npx skills add cmj-hub/claude-pricing --all -g --full-depth
```

```text
/plugin marketplace add cmj-hub/gtm-operator-skills
/plugin install pricing
```

Also: `npm install github:cmj-hub/claude-pricing` then `npx jmc-pricing`. Or `curl -fsSL https://raw.githubusercontent.com/cmj-hub/claude-pricing/main/install.sh | bash`.

## What you walk out with in 15 minutes

Artifact: `examples/tiers-healthy.json`.

```bash
python3 scripts/decoy_validator.py --tiers examples/tiers-healthy.json
python3 scripts/decoy_validator.py --tiers examples/tiers-broken.json
```

Run the decoy validator on the sample. Then drop in yours.

## What this pack will not do

It will not change live prices.
It will not run a customer survey.
It will not sit a tribunal on the first run.

This pack drafts and scores. It will not pick this quarter's PSP, ingest your CRM, or update when Gmail changes the spam window. That is the course + Operator Pass: the catalog that keeps moving, the tools that stay calibrated, the Friday room where you bring the artifact.

## Is this just "raise prices 15%"?

No. A blanket raise still leaks pocket price.
Diagnose WTP, the value metric, and the discount stack first. Then cut.

## Do I need survey data?

No for the first loop. The decoy validator runs on a three-tier JSON file. Van Westendorp is in the pack when you have responses. It is not a gate.

## Does this change live prices?

No. It scores and recommends. Shipping the change is your motion.

## Suite, course, Operator Pass

- Suite: [gtm-operator-skills](https://github.com/cmj-hub/gtm-operator-skills) · [jaymountconsulting.com/skills](https://jaymountconsulting.com/skills)
- Course: [Pricing Surgery](https://jaymountconsulting.com/learn/courses/pricing-surgery)
- Operator Pass: [jaymountconsulting.com/operator-pass](https://jaymountconsulting.com/operator-pass)

Founder: $97/mo billed annually ($1,164/yr), locked for life if bought before October 31, 2026. After that: $197/mo billed annually ($2,364/yr), no lock.

## Companion packs

- [claude-psp](https://github.com/cmj-hub/claude-psp) — five-part buying brief
- [claude-evp](https://github.com/cmj-hub/claude-evp) — 22-word line per Schwartz tier
- [claude-cold-email](https://github.com/cmj-hub/claude-cold-email) — signal, pain, EVP, binary ask
- [claude-founder-brand](https://github.com/cmj-hub/claude-founder-brand) — Pillar / Proof / Process / Person

## License

MIT. See [LICENSE](./LICENSE).

## About

Built by [Jay Mount Consulting](https://jaymountconsulting.com).
