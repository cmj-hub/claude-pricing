---
name: pricing-onboarding
description: First-run interactive setup for the pricing skill pack. Walks the operator through brand-config.json (current tiers, ICP, value metric, infrastructure) and the pricing section of SOUL.md (voice + stance on pricing + stories you cite) in ~10 minutes. Refuses to let the operator skip — generic pricing output is worse than no pricing output. Loaded automatically by the main pricing skill when brand-config.json or SOUL.md is missing.
user-invocable: false
allowed-tools: Read Write
license: MIT
models: ""

---

# Pricing Onboarding — sub-skill

Interactive setup. ~10 minutes. Outputs:

- `brand-config.json` at the project root — the `customer` and
  `pricing` blocks, merged into the existing file
- `SOUL.md` at the project root — the pricing sections, added or
  updated in place

Both files are shared by every pack in the GTM operator suite. This
skill owns `customer` and `pricing` only.

The skill REFUSES to draft real pricing recommendations until both
files exist with the required pricing fields populated.

## Activation

The main `pricing` skill routes here when:

- `brand-config.json` doesn't exist OR
- `brand-config.json` exists but `pricing.*` is empty OR
- `SOUL.md` doesn't exist OR
- `SOUL.md` exists but the pricing-stance section is empty

## Workflow

### Step 1 — Welcome + scope

Output:

```
Pricing setup — ~10 minutes
─────────────────────────────────────────────────────────────────

I'll ask you 12 questions about your current pricing, then create:

  brand-config.json   ← your tiers, value metric, customers, ops
  SOUL.md             ← your voice and stance on pricing decisions

The skill won't draft real pricing recommendations without these
files. Generic pricing copy is worse than none. Ready? (y/n)
```

Wait for confirmation. If `n`, exit with a brief explanation of why
this matters.

### Step 2 — Brand-config questions

Ask in batches of 2-3, not one at a time:

**Batch 1 — Current state (3 questions):**
1. What's your current pricing? (List the tiers + prices + cadence — e.g., "$99/$299/$999 monthly")
2. What's your headline value metric — what scales with customer success? (per-seat / per-API / per-record / per-outcome / hybrid)
3. What's your average ACV today, and is it trending up, down, or flat in the last 6 months?

**Batch 2 — Customers (3 questions):**
4. Who's your primary Pain Signal Profile (PSP)? If `customer.psps[]`
   or the shared `psp` block already exists, read it back and ask the
   operator to confirm instead. If neither exists, say the psp pack
   produces it (`/psp:psp`; install with
   `/plugin install psp@gtm-operator-skills`) and offer to run it
   first. If the operator declines, take a 1-2 sentence working PSP
   for `customer.psps[]` and mark it as unvalidated. Never invent one.
5. What's your typical buyer's biggest pricing objection in cycle? (verbatim if you have it)
6. What pricing did you walk away from in the last 6 months that you wish you'd held? (and why did you discount?)

**Batch 3 — Diagnostic surface (3 questions):**
7. Do you know your WTP distribution per PSP — or would the answer to "What would you pay for this?" be different across your buyer segments? (Yes/Best guess/No)
8. Have you ever run a structured WTP survey (Van Westendorp / Gabor-Granger / conjoint) in the last 18 months?
9. What's your current discount policy? (Documented thresholds, or "sales discretion")

**Batch 4 — Reference frames (3 questions):**
10. What does your buyer use INSTEAD if they don't buy from you? (the inertia anchor)
11. What's the highest-priced product or alternative they're already paying for? (anchor candidate)
12. Do you have an outcome guarantee or risk-reversal mechanism today? (e.g., "money-back if X")

### Step 3 — Voice setup (SOUL.md pricing section)

After brand-config is captured, prompt:

```
Now let's capture your pricing voice. 3 short questions:

A. What's your stance on pricing? (1-2 sentences. e.g., "Pricing is
   a discipline, not a strategy. I refuse to lead with cost-plus
   or competitor anchoring.")
B. What 3 phrases would you NEVER use when talking about price?
   (e.g., "investment", "value-add", "best-in-class")
C. What 2-3 stories or receipts do you cite when explaining why
   your price is fair? (Specific receipts: customer X saved Y; team
   Z hit metric W.)
```

### Step 4 — Write the files

Shared-files contract:

- One `brand-config.json` and one `SOUL.md` at the operator's project
  root, shared by every pack.
- Merge at the field level. Read the existing file first, add or
  update only `customer` and `pricing`, and leave every other key
  exactly as it was. Never rewrite the file from
  `brand-config.example.json`; use it only as the shape reference.
  Never delete another pack's keys (`psp`, `evp`, `tone`, ...).
- Show the diff and ask before changing a field that already has a
  value.
- `operator` and `icp` are shared: fill gaps only.
- Never write the `psp` block. The psp pack owns it.

`SOUL.md`: append or update only the pricing sections from the
template (`## My stance on pricing`, `## How I talk about price`,
the phrases and stories sections). Never rewrite another pack's
section. If the file does not exist, create it with the pricing
sections only.

### Step 5 — Confirm + route

Show a summary:

```
✓ brand-config.json written/updated
✓ SOUL.md written/updated

State check:
  ✅ Step 1 — brand-config + SOUL ready
  ✅ Step 2 — Current tiers documented
  ⬜ Step 3 — Pain Signal Profile (run /psp:psp)
  ⬜ Step 4 — WTP discovery (next: /pricing diagnose)
  ...

Recommended next action: Run /pricing diagnose to see where your
margin is leaking before any tier rebuild. (~15 minutes.)

Run it now? (y/n)
```

## Validation rules

Before writing the files, validate:

- All 12 brand-config questions have non-empty answers
- All 3 SOUL questions have non-empty answers  
- Tier prices are real numbers, not placeholders
- WTP "Yes/Best guess/No" answer determines whether to require a
  WTP-source field

If validation fails, loop back to the unanswered question — don't
write half-filled files.

## Self-check

- [ ] `brand-config.json` exists and parses as valid JSON
- [ ] `brand-config.json` has populated `pricing.currentTiers`, `pricing.valueMetric`, and `customer.psps[]` or the `psp` block
- [ ] Every key outside `customer` and `pricing` is unchanged (gaps in `operator` / `icp` may be filled)
- [ ] `SOUL.md` exists and has the pricing-stance section
- [ ] Operator confirmed both files via `y` response
- [ ] State checklist re-evaluated post-write

## Reference

- `../../brand-config.example.json` — schema for the JSON file
- `../../SOUL.md` — template for the voice file
- `../pricing-kickoff/SKILL.md` — where the operator returns after setup
