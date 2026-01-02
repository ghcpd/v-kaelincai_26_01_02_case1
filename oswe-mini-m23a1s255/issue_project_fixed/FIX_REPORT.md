# FIX_REPORT — Insurance Claim Calculator (fixed)

## Summary ✅
The original `issue_project` contained two functional bugs that caused incorrect payouts for specific inputs: a deductible boundary bug (loss == 2000) and a missing driving-years bonus application. I implemented targeted fixes while preserving the public API and test-suite.

## What I changed (high level)
- Fixed deductible boundary condition in `ClaimCalculator._calculate_deductible`
- Ensured driving-years bonus is applied in `ClaimCalculator.calculate_payout`
- Added small robustness checks (no negative base amount)
- Kept public API and tests unchanged

## Bugs fixed (file/function-level) 🔧
1. File: `src/insurance_claim.py` — `ClaimCalculator._calculate_deductible`
   - Problem: used `if loss_amount < 2000` which mis-classified loss == 2000
   - Fix: changed to `if loss_amount <= 2000` so the fixed 500 CNY deductible applies for loss ≤ 2000

2. File: `src/insurance_claim.py` — `ClaimCalculator.calculate_payout`
   - Problem: `_apply_driving_bonus()` was implemented but never called, so qualified drivers received no bonus
   - Fix: applied driving bonus after liability coefficient and before policy-limit/minimum checks

## Tests & Results ✅
All original tests (unchanged) now pass in the fixed project.

Command run:

```bash
pytest tests/ -q
```

Observed:

```
16 passed in 0.06s
```

## Verification (examples) 💡
- Example from the spec (boundary + bonus):
  - Input: loss=2000, insurance=comprehensive, liability=full, driving_years=5, policy_limit=50000
  - Expected & Actual: 1320.0
  - Calculation: (2000 - 500) * 0.80 * 1.00 * 1.10 = 1320

- Additional examples (from `demo_fixed.py`):
  - loss=5000, comprehensive, full, 3y -> 3780.0
  - loss=15000, third_party, primary, 7y (policy_limit=20000) -> value capped by limit if needed

## How to run
1. Run the test-suite
   ```powershell
   cd issue_project_fixed
   pytest tests/ -v
   ```

2. Run the demo
   ```powershell
   python demo_fixed.py
   ```

## Notes & rationale
- Changes are minimal and localized to the two failing areas described in `KNOWN_ISSUE.md`.
- Public API (class names, function signatures) preserved to maintain backward compatibility.

---
If you want, I can open a PR patch, add more unit tests for additional edge-cases, or prepare a changelog entry. 
