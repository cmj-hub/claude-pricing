# Changelog

## [0.3.0] — 2026-09-08

Public magnet pass. Instrument stays public. First loop is 15 minutes.

### Added
- Definition-first README (GEO paragraph, 15-minute artifact, FAQ H2s, current Pass price).
- Cross-agent installer: `npx skills add cmj-hub/claude-pricing --all -g --full-depth` (Claude Code, Cursor, Codex, Grok, Copilot, Windsurf, Cline, OpenCode, Antigravity, Goose, and the rest of the skills CLI list). Fallback copies into well-known `*/skills` dirs.
- `package.json` (`jmc-pricing`) so `npm install github:cmj-hub/claude-pricing` and `npx jmc-pricing` work. Not published to npmjs.com.
- `examples/` golden good/bad pair for the first loop.

### Changed
- Removed pricing copy from the public pack; CTAs point at the free hosted tools.
- `plugin.json` description is the definition, homepage is /skills.

## [0.2.0] — 2026-05-24

Initial public release of claude-pricing.

### Added

- Top-level `pricing` orchestrator (`pricing/SKILL.md`) with
  workflow router across 11 sub-skills
- 11 sub-skills:
  - `pricing-kickoff` — adaptive 9-step state router
  - `pricing-onboarding` — 10-min interactive brand-config + SOUL setup
  - `pricing-diagnostic` — three-surface diagnostic (WTP / value-metric / packaging)
  - `pricing-audit` — 30-point pricing program audit
  - `pricing-tribunal` — high-stakes decision workflow (Hypothesize → Test → Adjudicate → Audit)
  - `pricing-reference-frames` — anchor design + Prospect Theory application
  - `pricing-contrast-set` — three-tier + decoy architecture
  - `pricing-pocket-waterfall` — discount-leak detection
  - `pricing-value-metric` — price unit selection
  - `pricing-quarterly-review` — operating cadence + agenda
  - `pricing-renewal-discipline` — renewals + expansion + contraction
- 2 specialist agents:
  - `pricing-reviewer` — pricing-page + tier scorer (0-100)
  - `pricing-tribunal-judge` — adjudicates pricing hypotheses
- 3 zero-dependency Python scripts (Python 3.8+):
  - `pocket_price_waterfall.py` — per-customer + cohort discount-leak calculator
  - `decoy_validator.py` — three-tier asymmetric-dominance checker
  - `wtp_distribution.py` — Van Westendorp PSM analyzer (4 thresholds + acceptable range)
- Reference documents:
  - `pricing-framework.md` — full JMC framework (three surfaces, reference-frame stack, Prospect Theory, three-tier contrast set, pocket-price waterfall, tribunal discipline)
  - `pricing-banned-patterns.md` — 18 pricing patterns the skill refuses
  - `pricing-lineage.md` — historical lineage (Simon, Kahneman, Ariely, Christensen, Ramanujam)
- 3-tier identity:
  - `pricing/SKILL.md` — JMC framework (load-bearing structural rules)
  - `brand-config.json` — operator's pricing + customer config
  - `SOUL.md` — operator's voice + stance on pricing
- Adaptive kickoff with 9-step state machine
- Smoke-test (`scripts/smoke-test.sh`) covering all 3 scripts + 8 assertions

### Quality bar

All 3 scripts have:
- Zero dependencies (Python stdlib only)
- Smoke tests on real fixture data
- Type-checked via Pyright

The orchestrator + 11 sub-skills + 2 agents follow the AgriciDaniel
pattern (nested orchestrator + sub-skills + agents + scripts + 3-tier
config + adaptive kickoff).

## Inspiration credit (not in README per JMC policy)

Pattern + structural conventions inspired by:

- The AgriciDaniel skill-pack architecture (nested orchestrator +
  sub-skills + agents + scripts + 3-tier config)
- Hermann Simon's *Confessions of the Pricing Man* + *Power Pricing*
- Kahneman & Tversky's Prospect Theory (Nobel 2002)
- Madhavan Ramanujam's *Monetizing Innovation*
- Dan Ariely's *Predictably Irrational* (decoy effect)
