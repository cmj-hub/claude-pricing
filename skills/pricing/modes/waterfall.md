# Waterfall mode

Build the pocket-price waterfall and rank where discount margin leaks.

## Contents

- Activation
- The canonical waterfall
- Workflow
- Self-check
- Script reference
- Related

The discount-leak detector. Headline price ≠ revenue. The waterfall
surfaces every step where margin leaks between list and pocket.

## Activation

Routed here when operator says:

- "My discounts are eating margin"
- "Where is margin leaking?"
- "Pocket price"
- "Discount policy review"
- "Why is our effective price so much lower than list?"

## The canonical waterfall

```
List price
  - Ramp discount (first-year, "introductory")
  - Volume discount (per-seat / per-unit breakpoints)
  - Bundle discount (multi-product)
  - Annual prepay discount
  - Strategic / champion / "executive sponsor" discount
  - Promotional / quarter-end close discount
  - Off-invoice rebates (back-end)
  - Credits / SLA penalties (rolling)
  - Payment-term cost (NET-60 vs NET-30 = ~0.5-1.5% of revenue)
  - Implementation discount (often "free")
= Pocket price
```

Pocket-price waterfall is run per-customer, then aggregated to the
cohort level.

## Workflow

### 1. Gather the data

Required (operator provides or pulls from CRM/billing):

- For each customer (or representative sample of ~30):
  - List price (per-tier, per-seat / per-unit)
  - Cadence (monthly / annual)
  - Each discount line-item with %, dollar value, and reason
  - Payment terms
  - Implementation / onboarding fees (and discounts)
  - Credits / penalties applied in the year

If the operator says "we don't track that" — flag this as the first
finding. You can't manage what you can't measure.

### 2. Run the waterfall script

Save the rows as `gtm/waterfall.csv` (create `gtm/` if missing; shape:
`${CLAUDE_PLUGIN_ROOT}/examples/waterfall-customers.csv`), then run:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/pocket_price_waterfall.py --file gtm/waterfall.csv --text
```

Drop `--text` for the full JSON report (the default). Exit 1 means no
row was usable; the line says which columns each row needs.

The script:

- Reads each customer's line-item data
- Computes pocket price per customer
- Aggregates to cohort-level mean/median
- Ranks discount steps by total margin impact
- Identifies the top 3 leak sources

### 3. Diagnostic questions

After the script runs, ask:

1. **What's the largest single leak step?** (Often: ramp discount or
   strategic discount.)
2. **Is the leak step tied to commercial value?** (Annual prepay
   tied to cash flow = real concession. "Strategic discount" with no
   commercial concession = pure leak.)
3. **Is the leak step bounded by policy or sales-rep discretion?**
   (Discretion = leak source; policy with thresholds = managed.)
4. **What % of revenue moves through the largest leak?** (>20% = top
   priority for policy work.)
5. **Are the leaks PSP-correlated?** (One PSP gets bigger discounts
   = a pricing-vs-WTP issue for that segment.)

### 4. Build the discount policy

For each leak step that's >5% of revenue, output a policy:

```
Discount step: {name}
Current state:
  - Frequency: applied to {N}% of customers
  - Mean discount: {X}%
  - Total $ leak: ${Y}/year
  - Tied to commercial concession: {Yes / No}
  - Bounded by policy: {Yes / No}

Recommended policy:
  - Approval threshold: 0-{N}% rep / {N}-{M}% manager / {M}+% VP
  - Required commercial concession: {longer term / prepay / case study / etc.}
  - Documentation requirement: {what gets logged}
  - Reason codes: {list of accepted reasons}
  - Forbidden reasons: {"close the deal" alone is not a reason}
```

### 5. Quantify the recovery

Estimate margin recovery if policy is implemented:

- Pre-policy mean discount on this step: X%
- Post-policy mean discount estimate: Y%
- Cohort revenue affected: $Z
- Estimated recovery: (X - Y) × Z

Typical first-year recovery from documenting + bounding discount
policy: 3-8% of total revenue. (Hermann Simon empirical baseline.)

### 6. Output the waterfall report

```
Pocket-Price Waterfall — {company}
─────────────────────────────────────────────────────────────────

LIST PRICE (cohort weighted average): ${X}/customer/year

Waterfall steps (ranked by leak magnitude):
  1. Ramp discount: -${Y1}/customer  (Z1% of customers, mean A1%)
  2. Strategic discount: -${Y2}/customer (Z2%, A2%)
  3. Volume discount: -${Y3}/customer (Z3%, A3%)
  ...

POCKET PRICE (cohort weighted average): ${P}/customer/year
LEAK FROM LIST: ${L} (M%)

TOP 3 PRIORITY POLICIES:
  1. {Policy for highest leak}
  2. {Policy for second leak}
  3. {Policy for third leak}

ESTIMATED FIRST-YEAR RECOVERY: ${R} (S% of revenue)

PSP-CORRELATED LEAKS:
  - {PSP X} discounted Y% more than median — investigate
```

## Self-check

- [ ] Per-customer data loaded (or operator flagged as data gap)
- [ ] Waterfall script ran successfully
- [ ] Top 3 leak steps identified
- [ ] Recommended policy for each is specific (thresholds + reason codes)
- [ ] Recovery estimate is conservative (not vibes)
- [ ] PSP-correlated leaks flagged separately

## Script reference

`${CLAUDE_PLUGIN_ROOT}/scripts/pocket_price_waterfall.py`:

- Input: `--file gtm/waterfall.csv` (or `--stdin`) with columns `customer_id, list_price, cadence,
  discount_steps_json, payment_terms_days, implementation_fee,
  credits_applied`
- Output: JSON with per-customer breakdown + cohort aggregates + leak ranking; `--text` for a summary
- Exit codes: 0 analyzed, 1 no usable row, 2 bad input
- No dependencies. Pure stdlib. Python 3.8+.

## Related

- [references/pricing-framework.md](../references/pricing-framework.md) — the waterfall in context
- [modes/tribunal.md](tribunal.md) — for any policy change that affects >10% of customers
- [modes/review.md](review.md) — where the waterfall is re-run quarterly
