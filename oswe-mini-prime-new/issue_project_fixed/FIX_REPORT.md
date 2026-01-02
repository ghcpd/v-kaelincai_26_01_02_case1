# FIX REPORT

## Summary
I analyzed the original `issue_project` and found two functional bugs:
1. Boundary condition error in `_calculate_deductible()` causing `loss_amount == 2000` to be treated as the 10% tier.
2. Missing call to `_apply_driving_bonus()` inside `calculate_payout()` resulting in driving experience bonuses being ignored.

Both bugs were fixed with minimal, localized changes to preserve the public API.

## Bugs Fixed

- File: `src/insurance_claim.py`
  - Function: `ClaimCalculator._calculate_deductible()`
    - Problem: Used `if loss_amount < 2000:` which excluded the exact boundary value 2000 from the fixed deductible tier.
    - Fix: Changed to `if loss_amount <= 2000:` so losses equal to 2000 use the 500 CNY fixed deductible.
  - Function: `ClaimCalculator.calculate_payout()`
    - Problem: Did not apply driving years bonus—`_apply_driving_bonus()` was never called.
    - Fix: Added call to `_apply_driving_bonus(amount_after_liability, request.driving_years)` and used its result for subsequent policy limit and minimum payout checks.

## Test Results
All tests in `tests/test_claim_calculator.py` were copied into the fixed project and now pass.

Running:
```
cd issue_project_fixed
pytest tests/ -v
```
Result: 16 passed, 0 failed ✅

## Verification Examples
- Example 1:
  - Input: loss=2000, insurance=comprehensive, liability=full, driving_years=5, policy_limit=50000
  - Calculation: (2000 - 500) * 0.80 * 1.00 * 1.10 = 1320.0
  - Output: 1320.0 (correct)

- Example 2:
  - Input: loss=10000, insurance=comprehensive, liability=full, driving_years=10, policy_limit=50000
  - Calculation: (10000 - 1000) * 0.80 * 1.00 * 1.15 = 8280.0
  - Output: 8280.0 (correct)

## Notes
- I preserved the public API (`ClaimCalculator`, `ClaimRequest`, `calculate_claim`) and did not alter test cases.
- The fixes are minimal and targeted to the bugs described in `KNOWN_ISSUE.md`.
