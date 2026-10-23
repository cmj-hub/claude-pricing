# Private pricing input contracts

The bundled customer and willingness-to-pay datasets have been withdrawn. No replacement dataset is distributed. Existing JSON files in this folder illustrate draft validation; they are not measured customer or survey records.

The waterfall scorer requires `customer_id`, `list_price`, and `cadence` (monthly or annual). Optional inputs are `discount_steps_json`, `payment_terms_days`, `implementation_fee` and `credits_applied`. A discount step has a name, percentage and optional reason. Supply only your own authorized private records.

The survey scorer requires `respondent_id`, `too_cheap`, `bargain`, `expensive` and `too_expensive`; `psp` optionally groups responses. Values must be measured responses supplied by the operator, never invented to make a pricing recommendation.

These are software input contracts, not spreadsheets or resources. Do not generate a sample CSV or publish/repackage private or withdrawn rows in any format.
