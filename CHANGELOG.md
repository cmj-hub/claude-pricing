# Changelog

## [0.6.0] — 2026-10-04

One skill, eleven modes. Drafts live in `gtm/`. Every script says what to do next.

### Moved
- `pricing/SKILL.md` → `skills/pricing/SKILL.md`; `pricing/references/` → `skills/pricing/references/`. `plugin.json` drops the `skills` key (default discovery).
- The eleven sub-skills are now mode files under `skills/pricing/modes/`, read on demand. Type `/pricing:pricing <mode>`:
  `pricing-kickoff` → `status`, `pricing-onboarding` → `setup`, `pricing-diagnostic` → `diagnose`, `pricing-audit` → `audit`, `pricing-contrast-set` → `tiers`, `pricing-reference-frames` → `anchor`, `pricing-pocket-waterfall` → `waterfall`, `pricing-value-metric` → `value-metric`, `pricing-tribunal` → `tribunal`, `pricing-quarterly-review` → `review`, `pricing-renewal-discipline` → `renewal`.
- Drafts: `price.json` → `gtm/price.json`, `tiers.json` → `gtm/tiers.json`, `customers.csv` → `gtm/waterfall.csv`, `responses.csv` → `gtm/wtp.csv`.

### Added
- `argument-hint` and a `$ARGUMENTS` routing table on `/pricing:pricing`; no argument runs `status`. Always-on cost drops from ~2,495 to ~325 tokens (agent descriptions trimmed too).
- Setup mode points to `/gtm:setup` for the shared `operator` / `icp` fields and asks only those gaps inline when the gtm plugin is not installed.
- All four scripts take `--file PATH` and `--stdin`; `--tiers` and `--input` remain as hidden aliases. `--json` everywhere; `--text` / `--format text` on the three JSON-default scripts. `--help` shows an example.
- Refusals read `- what is wrong → what to change` and end with `Next: fix the lines above and run this again.`; a pass ends with the next step. JSON gains `next`, plus `fixes` (score_price, wtp, waterfall) or a per-check `fix` (decoy_validator). Existing keys are unchanged.
- `examples/wtp-responses.csv`, `examples/waterfall-customers.csv`, `tests/test_cli.py`, smoke-test entries.
- `evals/`: five trigger cases and one near-miss (give-first email → sales-offer). `.github/workflows/evals.yml` runs them on manual dispatch only.
- README "In 60 seconds".

### Changed
- `decoy_validator.py`: an empty tier list is bad input (exit 2), not a refusal.
- `wtp_distribution.py`: exits 1 when fewer than 5 usable responses.
- `pocket_price_waterfall.py`: exits 1 when no row is usable; a zero list price skips the row instead of crashing.
- Skipped CSV rows are reported by row number, never by the respondent or customer id.

## [0.5.0] — 2026-10-04

A price never ships without its unit.

### Added
- `scripts/score_price.py` refuses a price with no value metric, a missing contrast set, or no tribunal verdict. Lists every reason; `--json` for the report. Exit 0 ok, 1 refused, 2 bad input.
- `examples/price-good.json`, `examples/price-no-metric.json`, `tests/test_score_price.py`, and a smoke-test entry.
- "Score the price" step in `pricing` and `pricing-value-metric`.
- `SECURITY.md` and a Privacy and security section in the README.

### Fixed
- `decoy_validator.py` fails `same_value_metric` when a tier's `value_metric_unit` is empty or blank.
- `tests/__pycache__/` is no longer tracked.

## [0.4.0] — 2026-10-04

Suite pass. The main skill loads. Shared files merge, never overwrite.

### Fixed
- `pricing/SKILL.md` now loads: `plugin.json` lists `"skills": ["./pricing/"]` (12 skills).
- Malformed `allowed-tools` YAML in three sub-skills.
- `decoy_validator.py` exits 1 when the score is below 60. Tests and smoke test cover it.
- References pointed at three files that did not exist. They now link the matching sections of `pricing-framework.md`.
- Sub-skills call bundled scripts via `${CLAUDE_PLUGIN_ROOT}/scripts/`.
- `pricing-onboarding` can write the files it promises (`allowed-tools: Read Write`).

### Changed
- Main skill description says when to use it and what it is not for.
- `models: ""` on every skill. References are markdown links; `SOUL.md` is linked.
- Contents lists on `SOUL.md` and the three references.
- Onboarding follows the shared-files contract: owns `customer` and `pricing`, fills gaps in `operator` / `icp`, never writes `psp`.
- PSP reads fall back to the shared `psp` block. With no PSP, point at `/psp:psp` (`/plugin install psp@gtm-operator-skills`).
- "Works with the suite" section (step 6).
- README install uses `npx skills add`; the decoy validator example shows scores and exit codes.
- `plugin.json`: repository, keywords, author url. Version 0.4.0.

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
