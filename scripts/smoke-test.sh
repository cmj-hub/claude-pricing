#!/usr/bin/env bash
# Smoke-test the 3 deterministic scripts in claude-pricing.
# Each must exit cleanly on known input and produce expected output shape.
#
# Runs in CI under GitHub Actions (Ubuntu, Python 3.12).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

PASSED=0
FAILED=0

check() {
  local name="$1"; shift
  if "$@"; then
    echo "  ✓ $name"
    PASSED=$((PASSED + 1))
  else
    echo "  ✗ $name (exit $?)"
    FAILED=$((FAILED + 1))
  fi
}

echo "=== pocket_price_waterfall.py ==="
# Build a minimal CSV with 3 customers + assorted discount steps
cat > "$TMP_DIR/customers.csv" <<'CSV'
customer_id,list_price,cadence,discount_steps_json,payment_terms_days,implementation_fee,credits_applied
acme,1200,monthly,"[{""name"":""ramp"",""pct"":0.20,""reason"":""1st year""},{""name"":""volume"",""pct"":0.10,""reason"":""25 seats""}]",30,0,0
beta,500,annual,"[{""name"":""strategic"",""pct"":0.15,""reason"":""design partner""}]",60,500,100
gamma,2400,annual,"[]",30,0,0
CSV
check "pocket-waterfall on 3-customer cohort" \
  python3 "$SCRIPT_DIR/pocket_price_waterfall.py" \
    --input "$TMP_DIR/customers.csv" --output "$TMP_DIR/waterfall.json"
check "output contains top_3_leaks key" \
  grep -q '"top_3_leaks"' "$TMP_DIR/waterfall.json"

echo ""
echo "=== decoy_validator.py ==="
# Healthy three-tier with proper decoy + anchor
cat > "$TMP_DIR/tiers_healthy.json" <<'JSON'
{
  "tiers": [
    {"name": "Starter", "price": 99, "cadence": "monthly",
     "value_metric_unit": "seat", "value_metric_quantity": 5,
     "features": ["SSO", "Basic reporting"]},
    {"name": "Pro", "price": 299, "cadence": "monthly",
     "value_metric_unit": "seat", "value_metric_quantity": 25,
     "features": ["SSO", "Basic reporting", "Audit log", "Priority support"]},
    {"name": "Scale", "price": 999, "cadence": "monthly",
     "value_metric_unit": "seat", "value_metric_quantity": 100,
     "features": ["SSO", "Basic reporting", "Audit log", "Priority support", "Named CSM"]}
  ]
}
JSON
check "decoy-validator on healthy tiers" \
  python3 "$SCRIPT_DIR/decoy_validator.py" --tiers "$TMP_DIR/tiers_healthy.json" --output "$TMP_DIR/decoy_h.json"
check "healthy structure scores ≥85" \
  bash -c "python3 -c 'import json; d=json.load(open(\"$TMP_DIR/decoy_h.json\")); exit(0 if d[\"score\"] >= 85 else 1)'"

# Broken tier set (only 2 tiers, mixed units)
cat > "$TMP_DIR/tiers_broken.json" <<'JSON'
{
  "tiers": [
    {"name": "Basic", "price": 99, "cadence": "monthly",
     "value_metric_unit": "seat", "value_metric_quantity": 5,
     "features": ["A", "B", "C", "D", "E", "F", "G", "H"]},
    {"name": "Pro", "price": 299, "cadence": "monthly",
     "value_metric_unit": "api_call", "value_metric_quantity": 10000,
     "features": ["A"]}
  ]
}
JSON
check "decoy-validator on broken tiers" \
  python3 "$SCRIPT_DIR/decoy_validator.py" --tiers "$TMP_DIR/tiers_broken.json" --output "$TMP_DIR/decoy_b.json"
check "broken structure scores <60" \
  bash -c "python3 -c 'import json; d=json.load(open(\"$TMP_DIR/decoy_b.json\")); exit(0 if d[\"score\"] < 60 else 1)'"

echo ""
echo "=== wtp_distribution.py ==="
# Van Westendorp survey: 20 respondents, clean distribution
{
  echo "respondent_id,psp,too_cheap,bargain,expensive,too_expensive"
  for i in $(seq 1 20); do
    base=$((i * 5 + 50))
    echo "r$i,saas,$((base / 2)),$((base * 3 / 4)),$((base * 5 / 4)),$((base * 7 / 4))"
  done
} > "$TMP_DIR/wtp.csv"
check "wtp-analyzer on 20-response cohort" \
  python3 "$SCRIPT_DIR/wtp_distribution.py" --input "$TMP_DIR/wtp.csv" --output "$TMP_DIR/wtp.json"
check "output contains thresholds + acceptable_range" \
  bash -c "grep -q 'thresholds' '$TMP_DIR/wtp.json' && grep -q 'acceptable_range' '$TMP_DIR/wtp.json'"

echo ""
echo "Passed: $PASSED"
echo "Failed: $FAILED"
[ "$FAILED" -eq 0 ]
