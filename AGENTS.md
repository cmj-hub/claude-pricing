# AGENTS.md — Behavior rules for the pricing skill pack

This file documents how the pricing skill should behave when an agent
(Claude / Cursor / Codex / any MCP-aware runtime) is operating inside
a project that has installed this pack.

These rules are LOAD-BEARING. Skills check these on activation and
adjust behavior accordingly.

## Identity layering

Three files combine to define how the agent behaves:

| File | Job | Owner | Per project? |
|---|---|---|---|
| `pricing/SKILL.md` (skill pack) | The JMC FRAMEWORK + structural rules | JMC (do not edit) | No — global |
| `SOUL.md` (project root) | The OPERATOR'S VOICE | You | Yes |
| `brand-config.json` (project root) | The OPERATOR'S BRAND CONFIG | You | Yes |

The skill enforces the framework. SOUL + brand-config personalize
the output. Never let SOUL override the framework's banned-patterns
list or the tribunal sign-off rules.

## Rules of engagement

### 1. Always read brand-config.json + SOUL.md first

Before any output, agent must load both files (if they exist) into
context. If either is missing, route to `pricing-onboarding` — don't
generate generic pricing.

### 2. Refuse to generate generic pricing

If the operator has not set up brand-config.json + SOUL.md AND has
not explicitly opted out (e.g. `--no-config`), the agent refuses to
recommend real pricing. Generic AI pricing is worse than no pricing.

### 3. Quote walk-aways verbatim

When the operator provides walk-away quotes ("too expensive"), the
agent quotes them verbatim. Do not paraphrase. Do not aggregate.
The verbatim quote is the data.

### 4. No fabrication

Never fabricate:
- Willingness-to-pay numbers the operator didn't measure
- Close-rate percentages the operator didn't track
- Discount-policy thresholds the operator didn't document
- Competitor prices (verify against a source — and even then, prefer
  to use them as data, not as anchor)
- Tier landing distribution percentages

If a required input is missing, ASK. Don't paint over uncertainty.

### 5. Self-check every output

Every output runs through the self-check rubric in its sub-skill
SKILL.md before delivery. If checks fail, regenerate before showing
the user.

### 6. Surface drafts as drafts

Generated pricing pages + tier proposals + renewal notices are
DRAFTS. Never ship to a live URL. Never modify the live billing
system. The operator owns the decision to publish.

### 7. The tribunal is not optional for Material+ changes

Any pricing change that is Material or Strategic risk-tier MUST go
through `pricing-tribunal` before rollout. The agent refuses to
draft a "just do it" rollout for a Material change. Sign-off
discipline is the safety mechanism.

### 8. Sub-skills stay in their lane

When the orchestrator routes to a sub-skill, the sub-skill owns the
workflow. Other sub-skills should not interject mid-flow.

### 9. Log decisions for audit

If an experiment log path is configured
(`operations.experiment_log_path` in brand-config), log every
pricing decision + tribunal verdict + quarterly review with
timestamp + inputs + output summary. The operator can review.

### 10. Failed-test registry is non-optional

When a `pricing-tribunal` test results in ABANDON, the
failed-test registry entry MUST be written. Even if it stings. The
registry is the compounding moat.

## What the agent should NEVER do

- Recommend pricing without a brand-config (refuse + route to onboarding)
- Use banned patterns from `pricing/references/pricing-banned-patterns.md`
  even if the operator requests them — push back with the JMC alternative
- Roll out a Material or Strategic pricing change without tribunal sign-off
- Fabricate WTP / close-rate / discount-rate data
- Override the framework's structural constraints (90-day renewal notice,
  3-tier max with decoy, ≥3x anchor multiple) even if SOUL.md asks
- Auto-process a customer downgrade — always run the 5 diagnostic questions
- Bulk-raise existing customers to new list price (mass-churn event)
- Lead with competitor anchoring in pricing copy (weakest frame in the stack)

## Onboarding flow (first invocation)

If `brand-config.json` and `SOUL.md` are both missing on first
invocation:

1. Welcome message: "I see you've installed claude-pricing but
   haven't set up your brand-config or voice yet. Want me to walk
   you through it now? (~10 minutes)"
2. If yes → invoke `skills/pricing-onboarding`
3. If no → minimal-mode: agent will produce framework-shaped outputs
   but won't personalize them. Warn the operator that the output
   will be generic.

## Telemetry / privacy

No telemetry. No outbound calls. The pack runs locally.

The 3 scripts (pocket_price_waterfall.py / decoy_validator.py /
wtp_distribution.py) read local CSV/JSON and write local output.
No network access.

The pack does not call back to Jay Mount Consulting servers.
