# Security

## What this pack does on your machine

- Runs four local Python scripts, standard library only: `decoy_validator.py`, `wtp_distribution.py`, `pocket_price_waterfall.py`, `score_price.py`.
- The scripts read only the file you pass them (tier JSON, survey CSV, customer CSV, price draft JSON) or stdin. Input over 2 MB is refused, and bad input is never echoed back.
- `--output` writes the report to the path you name, and nowhere else.
- The skills read `brand-config.json` and `SOUL.md` at your project root, and write only there: `brand-config.json` and `SOUL.md` (field-level merge, setup mode only) and draft files in `gtm/` (`gtm/price.json`, `gtm/tiers.json`, `gtm/waterfall.csv`, `gtm/wtp.csv`).
- Network: no script opens a network connection. The `pricing-reviewer` agent may use WebFetch to load a public pricing page, only when you give it the URL.
- No telemetry. No credentials are asked for or stored.
- Nothing is sent, posted, or published by the pack. It never changes a live price.

## Reporting a vulnerability

Email jay@jaymountconsulting.com with "security" and the repo name in the subject, or open a private advisory under this repo's Security tab. Do not open a public issue for a vulnerability. Expect a reply within five business days.

## Supported versions

Only the latest release on `main` gets fixes.
