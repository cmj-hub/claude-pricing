# Pricing lineage — the thinkers this framework distills

The JMC Pricing Surgery framework synthesizes 70+ years of pricing
thought. The agent loads slices of this on demand when citing
mechanism or making a recommendation that relies on a specific
empirical result.

---

## Tier 1 — Foundational

### Hermann Simon

- *Confessions of the Pricing Man* (2015)
- *Power Pricing* (1996, with Robert Dolan)
- Founder of Simon-Kucher & Partners, the world's leading pricing-strategy firm

**Key contributions:**
- Pricing-as-discipline frame: "Pricing is the most under-managed lever in business"
- The 1% / 11% asymmetry (1% price improvement → ~11% profit improvement)
- Profit-impact priority: price > variable cost > volume > fixed cost
- "True confessions" — the discipline is what compounds, not any single price change

**Applied in this pack:** Core frame across the entire orchestrator
+ the `pricing-audit` 30-point rubric.

### Daniel Kahneman + Amos Tversky

- *Prospect Theory* (1979, Econometrica)
- Kahneman: *Thinking, Fast and Slow* (2011); Nobel 2002

**Key contributions:**
- Losses loom larger than gains (~2.25x in most studies)
- Reference dependence — outcomes are coded relative to a reference point
- Risk aversion over gains, risk seeking over losses
- The endowment effect — once owned, value increases

**Applied in this pack:** `pricing-reference-frames` (loss-aversion
copy) + the framework's "anchor on inertia, not competitor" rule.

### Theodore Levitt

- *Marketing Myopia* (1960, HBR)
- *The Marketing Imagination* (1983)

**Key contributions:**
- "People don't want quarter-inch drills; they want quarter-inch holes"
- Value-metric origin: charge for the outcome, not the artifact
- Customer-job orientation predates JTBD by 50 years

**Applied in this pack:** `pricing-value-metric` (the 4-criterion
right-metric rubric).

---

## Tier 2 — Practitioners

### Steve Blank

- *The Four Steps to the Epiphany* (2005)
- *The Startup Owner's Manual* (2012)

**Key contributions:**
- Customer Development framework — get out of the building
- Willingness-to-pay discovery as a structured process, not an guess
- Customer-validation before scaling

**Applied in this pack:** `pricing-diagnostic` Surface 1 (WTP
distribution) and the `pricing-onboarding` PSP discovery flow.

### Clayton Christensen

- *The Innovator's Dilemma* (1997)
- *Competing Against Luck* (2016, JTBD)

**Key contributions:**
- Jobs-to-Be-Done framework
- Value metric = the unit of the job customer is hiring product to do
- Disruption requires understanding the job, not the demographics

**Applied in this pack:** `pricing-value-metric` value-metric
selection (Surface 2 of the diagnostic).

### Geoffrey Moore

- *Crossing the Chasm* (1991)
- *Inside the Tornado* (1995)

**Key contributions:**
- Pricing-by-segment discipline — different PSPs, different prices
- Early-market vs mainstream-market pricing dynamics
- The chasm pricing trap (innovators tolerate higher prices than early majority)

**Applied in this pack:** PSP-segmented pricing throughout
(`brand-config.json` `customer.psps[]` model).

### Madhavan Ramanujam

- *Monetizing Innovation* (2016, with Georg Tacke)
- Modern Simon-Kucher practitioner

**Key contributions:**
- Pricing-as-product-design: design pricing BEFORE designing product
- 4 monetization failures: feature shocks, minivations, hidden gems, undead products
- Willingness-to-pay testing as a pre-product discipline

**Applied in this pack:** The framework's "diagnose first, intervene
last" stance + the integration with the `claude-evp` companion pack.

### Robert Cialdini

- *Influence* (1984, revised 2021)
- *Pre-Suasion* (2016)

**Key contributions:**
- Anchoring as the foundational reference-frame mechanic
- Contrast principle — the second offer is anchored by the first
- Scarcity, reciprocity, social proof — applied with caution in B2B pricing

**Applied in this pack:** `pricing-reference-frames` anchoring +
`pricing-contrast-set` three-tier architecture.

### Dan Ariely

- *Predictably Irrational* (2008)
- The Economist subscription experiment (decoy effect demonstration)

**Key contributions:**
- Decoy effect / asymmetric dominance (the third option that makes
  the second look obvious)
- Anchoring extends to arbitrary numbers (social security digits experiment)
- Pain of paying — payment friction shapes WTP

**Applied in this pack:** `pricing-contrast-set` decoy-tier design
+ the `decoy_validator.py` script's asymmetric-dominance check.

### Peter Drucker

- *Management: Tasks, Responsibilities, Practices* (1973)

**Key contributions:**
- Price as a managerial discipline, not a finance function
- "What does the customer value, and what does he buy?"
- Pricing-as-strategy, not pricing-as-tactic

**Applied in this pack:** The orchestrator's framing of pricing as
the highest-leverage CEO-owned lever (not delegated to sales or finance).

### Claude Hopkins

- *Scientific Advertising* (1923)

**Key contributions:**
- Pricing copy is testable — falsifiable-hypothesis discipline
- The failure registry is more valuable than the win registry
- Specifics outperform vagueness

**Applied in this pack:** The `pricing-tribunal` four-stage workflow
(Hypothesize → Test → Adjudicate → Audit) and the failed-test registry.

---

## How to use this lineage

When the skill makes a recommendation, it should be able to cite
which thinker the recommendation traces back to. Example:

> "Recommend anchoring on inertia rather than competitor cost. This
> is Hermann Simon's foundational frame; loss aversion (Kahneman +
> Tversky) explains why it works for the 95% of buyers not in cycle."

If a recommendation can't be traced to one of these (or a similarly-
rigorous source), the agent should flag it as opinion, not framework.

The discipline is the citation; the citation is the discipline.
