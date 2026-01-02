# FIX REPORT

## Summary
Fixed the Insurance Claim Calculator to correct functional bugs reported in the original project. The fixes address:
- Deductible boundary condition for loss_amount == 2000
- Missing driving-years bonus application in payout calculation

All unit tests in `tests/test_claim_calculator.py` now pass (16/16).

## Bugs Fixed

1. File: `src/insurance_claim.py` — function: `_calculate_deductible`
   - Problem: `loss_amount == 2000` incorrectly fell into the percentage tier because the condition used `< 2000`.
   - Fix: Changed condition to `if loss_amount <= 2000:` so 2000 uses the fixed 500 deductible.

2. File: `src/insurance_claim.py` — function: `calculate_payout`
   - Problem: Driving-years bonus was not applied (missing call to bonus helper), so eligible claimants did not receive their bonus.
   - Fix: Apply `_apply_driving_bonus` to the payout after liability coefficient and before policy/minimum rules.

## Test Results
All tests passing:
- pytest tests/ -v -> 16 passed, 0 failed

## Verification (examples)
- Loss=2000, comprehensive, full, 5 years -> payout = (2000 - 500) * 0.80 * 1.00 * 1.10 = 1320.00
- Loss=5000, comprehensive, full, 3 years -> payout = (5000 - 500) * 0.80 * 1.00 * 1.05 = 3780.00
- Loss=10000, comprehensive, full, 10 years -> payout = (10000 - 1000) * 0.80 * 1.00 * 1.15 = 8280.00

## Notes
- Public API unchanged: `ClaimCalculator`, `ClaimRequest`, and `calculate_claim` behave as before.
- Tests were left unchanged and serve as the authoritative specification for behavior.
