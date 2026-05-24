# The JMC Pricing Surgery Framework

> The full framework. Sub-skills load slices of this on demand.

---

## The frame

Pricing is the highest-leverage operational lever in the business and
the one operators give the least attention. **A 1% price improvement
drives roughly an 11% profit improvement** on average B2B economics —
because pricing changes flow directly to the bottom line without
proportional cost increases.

(Source: Hermann Simon, *Confessions of the Pricing Man*; Simon-Kucher
& Partners empirical work across 2,000+ engagements.)

Most B2B pricing is under-managed. Cost-plus formulas. Competitor
anchoring. Vibes-based tier construction. Undisciplined discounting.
The result: pricing drifts, margin erodes, and operators reach for
"let's just raise prices 15%" — the move with the worst risk/reward
profile in the playbook.

The JMC discipline is surgical: **diagnose first, intervene precisely**.

---

## The three diagnostic surfaces

Before changing any pricing dimension, diagnose across three surfaces:

### Surface 1 — Willingness-to-pay (WTP) distribution

Per Pain Signal Profile (PSP), what does the WTP distribution look
like? Use structured customer-development methods:

- **Van Westendorp PSM** — four threshold questions on a sample of 20-40
  qualified buyers per PSP. Outputs: "too cheap" / "bargain" /
  "expensive" / "too expensive" intersection points.
- **Gabor-Granger** — direct price-acceptance laddering. Outputs:
  price-acceptance curve, demand at each point.
- **Conjoint analysis** — for multi-attribute decisions where price is
  one factor among several. Heavier-weight; use when you have ≥80
  responses per PSP.

The discipline is more important than the math. Most operators have
never asked 20 customers a structured price-sensitivity question.

### Surface 2 — Value-metric alignment

Does your price unit scale with your buyer's success? If you charge
per-seat but the value scales with API calls, you've created a
volume-versus-revenue tension that compounds with every customer
expansion.

Common B2B value-metric units:
- Per-seat
- Per-API-call / per-action
- Per-active-record / per-MAU
- Per-revenue-processed
- Per-outcome (closed deals, hired candidates, qualified leads)
- Per-environment / per-workspace
- Hybrid (base + variable)

The right metric is the one that aligns YOUR revenue growth with
THEIR success expansion. Misalignment is a continuous tax.

### Surface 3 — Packaging-vs-pricing diagnosis

Is the problem the price, or the package? Often the headline price
is right; the *bundle* is wrong. Diagnostic questions:

- Are the wrong features bundled together?
- Is the bottom tier so feature-poor it loses sales (vs the decoy
  that helps the upgrade conversation)?
- Is the top tier so feature-rich it caps growth?
- Are the cross-tier feature differences clear, or does the buyer
  need 20 minutes to figure out what they're paying for?

A pricing-page rebuild often delivers more lift than a price change.

---

## The reference-frame stack

Buyers anchor on a reference frame. The frame you pick determines
how the price *feels* — and feeling drives B2B decisions more than
spreadsheets.

Stack (strongest → weakest):

| Rank | Reference frame | Example |
|---|---|---|
| 1 | **Inertia / status quo** | "Right now you're solving this with a contractor + spreadsheet + 3 Slack channels — that's ~12 hrs/week of founder time at $200/hr loaded = $124,800/yr" |
| 2 | **Opportunity cost** | "Every week you delay = 1 fewer customer onboarded = $30K ARR opportunity cost" |
| 3 | **Replacement cost** | "If you built this internally: 2 engineers × 6 months × $250K loaded = $250K to ship + $80K/yr to maintain" |
| 4 | **Competitor cost** | "X charges $499/mo, we charge $399/mo" |

**Most pricing pages anchor on #4 (competitor). It's the weakest
frame and the easiest one for the buyer to dismiss with "I'll keep
shopping."** Anchor on #1 wherever possible.

---

## Prospect Theory applied

Kahneman + Tversky (Nobel 2002) showed that:

1. **Losses loom larger than equivalent gains** (~2.25x in most
   studies). A $1,000 loss hurts more than a $1,000 gain feels good.
2. **People are risk-averse over gains, risk-seeking over losses**.
3. **Reference points are everything.** The frame determines whether
   an outcome is coded as gain or loss.

Pricing implications:

- **De-risking copy beats size-of-win copy** for the 95% of buyers
  not in cycle. "Worth it or refund" outperforms "save 40% on X."
- **Money-back guarantees with clear qualification gates** outperform
  open-ended "money-back" claims (which feel risky to claim).
- **Outcome-tied guarantees with bounded liability** are the highest
  form: "If we don't ship X by date Y, you pay only Z." This shifts
  the loss reference point onto the seller.
- **Anchor against the loss of inertia,** not the gain of switching.

---

## Value-metric engineering

The right value metric:

1. **Scales naturally with customer success** (their growth = their bill grows
   without re-negotiation)
2. **Is easy to count + verify** (no audit disputes)
3. **Aligns with how the buyer talks internally** (matches their P&L line item)
4. **Doesn't create volume-vs-revenue tension** for their team

The wrong value metric:

- Per-seat when the value is per-customer-served (creates incentive
  to share logins)
- Per-API-call when the API calls are noisy + don't correlate with value
- Per-MAU when half the MAU are passive viewers
- Per-revenue-processed for a use case where revenue is volatile

**The metric-shift case study reservoir** — operators who switched
from per-seat to per-active-customer (or per-outcome) typically see
30-100% ACV expansion AND lower churn, because the metric now grows
with the customer.

---

## The pocket-price waterfall

Headline price ≠ revenue. The waterfall surfaces every step where
margin leaks between list price and final pocket:

```
List price
- Ramp discount (first-year)
- Volume discount
- Bundle discount
- Annual prepay discount
- Strategic / champion discount
- Promotional / quarterly close discount
- Off-invoice rebates
- Credits / SLA penalties
- Payment-term cost (NET-60 vs NET-30)
- Implementation discount (often "free")
= Pocket price
```

Most operators have never built this. The exercise alone often
recovers 5-15% margin via discount-policy tightening — no headline
price change required.

**The discipline: every discount step needs a documented reason and
an approval threshold.** Anything else is margin leaking through the
sales team's discretion.

---

## Three-tier contrast-set architecture

The structure that outperforms in 80%+ of B2B SaaS / services tests:

```
Tier 1 (Decoy)      Tier 2 (Target)      Tier 3 (Anchor)
$99/mo              $299/mo              $999/mo
Designed to make    Where you WANT       Sets the price
T2 look obviously   85%+ of buyers       reference. Buyer
better. Same value- to land. Most         compares T2 down,
metric, much less   features, best       not up.
of it.              value/$.
```

Key design rules:

1. **The decoy is asymmetrically dominated** — same value metric,
   strictly less of it. The decoy is not a real option; its job is
   to make T2 obvious. (Ariely, *Predictably Irrational*.)
2. **T3 anchors high** — sets the reference frame so T2 reads
   reasonable, not expensive.
3. **Feature differentiation is clean** — buyer can grok the tier
   differences in <30 seconds.
4. **Value-metric increases continuously** across tiers (more
   seats, more calls, more outcomes), but at decreasing per-unit
   marginal price (so T3 reads as "even better deal IF you need it").
5. **No "Enterprise — call us" tier in B2B SaaS** under ~$30K ACV
   unless you have a real strategic-customer motion. Below that,
   it's friction without lift.

---

## Pricing-page A/B as falsifiable hypothesis discipline

Claude Hopkins (*Scientific Advertising*, 1923) showed that pricing
copy is testable. Modern application:

- **Every test starts with a named hypothesis** — not a "let's see
  if this works" change.
- **Hypotheses cite the predicted lift direction + magnitude** —
  "this change should lift conversion 8-12% if reference-frame
  thesis is correct."
- **Tests run to statistical significance** (or the test is
  documented as inconclusive — never decided on vibes).
- **Failed tests are catalogued** — the failure registry is the
  compounding moat.

The discipline is what compounds — not any individual win.

---

## The pricing decision tribunal

For high-stakes pricing decisions (anything material to ARR), run a
four-stage tribunal:

1. **Hypothesize** — name the pricing hypothesis specifically:
   "If we shift from $299 flat to $0.05 per API call with a $99
   minimum, we expect mid-market ACV +25% and free-tier conversion
   +15%, with downside risk concentrated in low-volume customers
   (~5% of base, ~2% of ARR)."
2. **Test** — controlled tests without public damage:
   private beta, grandfather-clause for existing customers, ramp to
   10% of new sign-ups before full rollout.
3. **Adjudicate** — the verdict matrix: hypothesis predicted
   direction? Magnitude? Side effects? Documented sign-off from
   product + sales + finance.
4. **Audit** — 30/60/90 day audit. Did the change do what the test
   predicted? If no, the test was wrong (not the rollout). Update
   the diagnostic framework.

The discipline is what makes pricing changes safe-to-ship at speed.

---

## Lineage

For deeper reading, see `pricing-lineage.md`. The short list:

- **Hermann Simon** (foundational: *Confessions of the Pricing Man*,
  *Power Pricing*; Simon-Kucher founder; 50+ years of empirical work)
- **Daniel Kahneman + Amos Tversky** (Prospect Theory, Nobel 2002)
- **Theodore Levitt** ("Marketing Myopia", value-metric origin)
- **Steve Blank** (Customer Development for WTP discovery)
- **Clayton Christensen** (Jobs-to-be-Done value-metric definition)
- **Geoffrey Moore** (*Crossing the Chasm* — pricing by segment)
- **Robert Cialdini** (Anchoring + Contrast)
- **Dan Ariely** (*Predictably Irrational* — decoy effect)
- **Madhavan Ramanujam** (*Monetizing Innovation* — modern
  Simon-Kucher practitioner)
- **Peter Drucker** (price as managerial discipline)
- **Claude Hopkins** (*Scientific Advertising* — testing discipline)
