# Known Issues

This document describes the intentionally planted bugs in the Insurance Claim Calculator system.

## Issue Type

**Functional Bug** - The feature doesn't behave as specified; the model gives wrong output and ignores constraints.

## Bug #1: Boundary Condition Error in Deductible Calculation

### Description

When the loss amount is exactly 2000 CNY, the system incorrectly calculates the deductible using the wrong tier.

### Location

- **File**: [src/insurance_claim.py](src/insurance_claim.py)
- **Function**: `ClaimCalculator._calculate_deductible()`
- **Line**: ~100-107

### Root Cause

```python
# Current (buggy) code:
if loss_amount < 2000:      # Should be: loss_amount <= 2000
    return 500.0
elif loss_amount <= 10000:
    return loss_amount * 0.10
```

The boundary condition uses `<` instead of `<=`, causing:
- When `loss_amount = 2000`, it falls into the second tier
- Deductible calculated as: 2000 * 0.10 = 200 CNY
- Should be: 500 CNY (fixed deductible)

### Trigger Conditions

**Input**:
```python
loss_amount = 2000  # Exact boundary value
```

**Expected Behavior**:
- Deductible = 500 CNY (fixed amount for loss ≤ 2000)

**Actual Behavior**:
- Deductible = 200 CNY (10% of 2000)
- Difference: -300 CNY in deductible (leads to +240 CNY over-payment at 80% base ratio)

### Reproducing Tests

Run these specific tests to reproduce:
```powershell
pytest tests/test_claim_calculator.py::TestDeductibleCalculation::test_deductible_exactly_2000_FAILING -v
pytest tests/test_claim_calculator.py::TestEdgeCases::test_combined_boundary_and_bonus_bug_FAILING -v
```

### Impact

- Overpayment when loss is exactly 2000 CNY
- Violates business specification
- Affects financial calculations and customer trust

---

## Bug #2: Missing Driving Years Bonus Calculation

### Description

The system completely ignores the driving years bonus, failing to apply the specified bonus percentages based on driving experience.

### Location

- **File**: [src/insurance_claim.py](src/insurance_claim.py)
- **Function**: `ClaimCalculator.calculate_payout()`
- **Line**: ~79-81

### Root Cause

```python
# Current (buggy) code:
amount_after_liability = amount_after_base * liability_coef

# BUG: Missing driving years bonus calculation
# Should add:
# amount_after_bonus = self._apply_driving_bonus(amount_after_liability, request.driving_years)
# final_amount = amount_after_bonus

final_amount = amount_after_liability  # Directly uses amount without bonus
```

The code skips calling `_apply_driving_bonus()` method entirely, even though the method is correctly implemented.

### Trigger Conditions

**Input**:
```python
driving_years >= 3  # Any value triggering bonus
```

**Expected Behavior** (5 years example):
- Base calculation: (2000 - 500) * 0.80 * 1.00 = 1200
- With 10% bonus: 1200 * 1.10 = 1320 CNY

**Actual Behavior**:
- Calculation stops at: 1200 CNY
- Missing: +120 CNY bonus (10%)

### Bonus Tiers Affected

| Driving Years | Expected Bonus | Currently Applied |
|---------------|----------------|-------------------|
| 3-4 years     | +5%           | 0% (ignored)      |
| 5-9 years     | +10%          | 0% (ignored)      |
| 10+ years     | +15%          | 0% (ignored)      |

### Reproducing Tests

Run these specific tests to reproduce:
```powershell
pytest tests/test_claim_calculator.py::TestDrivingYearsBonus -v
```

All 3 tests in this class will fail:
- `test_driving_bonus_3_years_FAILING`
- `test_driving_bonus_5_years_FAILING`
- `test_driving_bonus_10_years_FAILING`

### Impact

- Systematic underpayment for all experienced drivers
- Violates business policy specification
- Unfair treatment of customers with good driving records
- Potential legal/compliance issues

---

## Combined Impact Example

The scenario from requirements demonstrates both bugs:

**Input**:
```
Loss: 2000 CNY
Insurance: Comprehensive (80%)
Liability: Full (100%)
Driving years: 5
```

**Expected Calculation**:
```
Deductible: 500 (fixed for ≤2000)
After deductible: 2000 - 500 = 1500
After base ratio: 1500 * 0.80 = 1200
After liability: 1200 * 1.00 = 1200
After bonus: 1200 * 1.10 = 1320 CNY
```

**Actual (Buggy) Calculation**:
```
Deductible: 200 (wrong tier, 10%)
After deductible: 2000 - 200 = 1800
After base ratio: 1800 * 0.80 = 1440
After liability: 1440 * 1.00 = 1440
After bonus: 1440 (bonus not applied) = 1440 CNY
```

**Discrepancy**: 1440 - 1320 = **+120 CNY** (overpayment due to wrong deductible outweighing missing bonus)

---

## Fix Strategy

### Fix #1: Boundary Condition

**Change** in `_calculate_deductible()`:
```python
# Line ~100
if loss_amount <= 2000:  # Add = sign
    return 500.0
```

### Fix #2: Apply Driving Bonus

**Add** in `calculate_payout()` after line ~78:
```python
# After applying liability coefficient
amount_after_liability = amount_after_base * liability_coef

# ADD THIS LINE:
amount_after_bonus = self._apply_driving_bonus(amount_after_liability, request.driving_years)

# Check policy limit
if amount_after_bonus > request.policy_limit:  # Update variable name
    final_amount = request.policy_limit
else:
    final_amount = amount_after_bonus  # Update variable name
```

### Verification

After applying fixes, all tests should pass:
```powershell
pytest tests/ -v
# Expected: 14/14 tests passing
```

---

## Notes

- These bugs are intentionally planted for demonstration purposes
- The `_apply_driving_bonus()` method is correctly implemented but never called
- Both bugs are simple, localized, and easily reproducible
- Fixes require minimal code changes (2 locations, ~3 lines total)
