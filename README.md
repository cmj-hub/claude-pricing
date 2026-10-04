<p align="center">
  <img src="./assets/lockup.png" width="880" alt="Pricing strategy skill for Claude Code. A pricing strategy is how you choose what to charge, what the price is compared with, and where the discount leaks.">
</p>

# Pricing strategy skill for Claude Code

A pricing strategy is how you choose what to charge, what the price is compared with, and where the discount leaks.

> "Raise prices 15%" is not a diagnosis. The leak is usually after the list price.

Pricing surgery treats price as the highest-leverage B2B lever: diagnose willingness-to-pay, pick the value metric, set a reference frame, build a three-tier contrast set, then plug discount leaks. A 1% price improvement is ~11% profit on typical B2B economics (Simon).

You already know the list price. You may not know the pocket price — what is left after ramp discounts, "strategic" exceptions, annual prepay, implementation credits, and net-60. Hermann Simon spent fifty years on that gap. This pack scores it.

The mechanism is surgical, not theatrical. Willingness-to-pay. Value metric. Reference frame. Three-tier contrast with a real decoy. Pocket-price waterfall. `decoy_validator.py` on the sample healthy set scores **100**. The broken two-tier mixed-unit set scores **10.5**. Python. No LLM. No paid API.

The build guide teaches a human. The pack teaches an agent.

<p align="center">
  <img src="./assets/demo.gif" alt="Pricing strategy skill — healthy tiers 100, broken tiers 10.5" width="100%">
</p>

## What this replaces

A boutique pricing sprint's diagnostic week — not the political work of getting sales and finance in the same room.

## Install

```text
npx skills add cmj-hub/claude-pricing --all -g --full-depth
```

`--all` writes this pack for every host the installer knows. One host:

```text
npx skills add cmj-hub/claude-pricing --skill '*' -g --full-depth -y -a claude-code
```

Swap `claude-code` for `cursor`, `codex`, `grok`, `github-copilot`, `windsurf`, `cline`, or `opencode`.

### Claude Code only

```text
/plugin marketplace add cmj-hub/gtm-operator-skills
/plugin install pricing@gtm-operator-skills
```

Then run `/pricing:pricing`.

## What you walk out with in 15 minutes

Artifact: `examples/tiers-healthy.json`.

```bash
python3 scripts/decoy_validator.py --tiers examples/tiers-healthy.json
# score 100.0, "HEALTHY three-tier contrast set." — exit 0
python3 scripts/decoy_validator.py --tiers examples/tiers-broken.json
# score 10.5, "REBUILD — multiple structural failures." — exit 1
python3 scripts/score_price.py --file examples/price-no-metric.json
# refused: a price with no metric, no contrast set, no tribunal verdict — exit 1
```

Run the decoy validator on the sample three-tier set. Then drop in yours. It prints the JSON report either way and exits 1 when the score is below 60, so it can gate a CI check or a pre-publish hook.

## What this pack will not do

It will not change live prices. It will not run a customer survey. It will not sit a tribunal on the first run.

This pack drafts and scores. It will not pick this quarter's PSP, ingest your CRM, or update when Gmail changes the spam window. Those are judgement calls and live data. This pack gives you the instrument and the rubric; you bring the account.

## Is this just "raise prices 15%"?

No. A blanket raise still leaks pocket price. Diagnose willingness-to-pay, the value metric, and the discount stack first. Then cut. Pricing is surgery. Diagnose first. Cut last.

## Do I need survey data?

No for the first loop. The decoy validator runs on a three-tier JSON file. Van Westendorp is in the pack when you have responses. It is not a gate.

## Does this change live prices?

No. It scores and recommends. Shipping the change — grandfathering, sales enablement, the email to the book — is your motion.

## On the site

- [Pricing Surgery pack](https://jaymountconsulting.com/skills/claude-pricing) — this pack's page
- [Skill packs catalog](https://jaymountconsulting.com/skills) — install paths + every pack
- [Course twin](https://jaymountconsulting.com/learn/courses/pricing-surgery) — human build guide for this pack

## Free, no signup

- **[Pricing Page Lab](https://jaymountconsulting.com/tools/pricing-page-lab)** — the same job as this pack, hosted. No account, no key.
- [Offers & Productized Outcomes framework](https://jaymountconsulting.com/frameworks/offers-productized-outcomes)
- [Calculator Pack](https://jaymountconsulting.com/resources/calculator-pack)

## Free, by email

[**Growth Audit**](https://jaymountconsulting.com/growth-audit) — where your go-to-market stack is leaking, sent to your inbox.

That one does ask for an email, and it enrols you in a short follow-up on the same topic. Unsubscribe whenever.

[**The Friday Signal**](https://jaymountconsulting.com/newsletter/signal) — one free edition a week on building GTM systems that compound. No pitch in it.


## Next

Previous: [Value proposition](https://github.com/cmj-hub/claude-evp)

Next: [Sales offer](https://github.com/cmj-hub/claude-sales-offer)

## Privacy and security

Four stdlib Python scripts run locally on the files you pass them. No script opens a network connection. The skills read and write `brand-config.json`, `SOUL.md`, and draft JSON in your project; nothing else. The `pricing-reviewer` agent fetches a pricing page only when you give it the URL. No telemetry, no credentials, nothing sent or published. See [SECURITY.md](SECURITY.md).

## License

MIT. See [LICENSE](./LICENSE).

## About

Built by [Jay Mount Consulting](https://jaymountconsulting.com).
