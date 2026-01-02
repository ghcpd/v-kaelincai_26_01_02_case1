# Insurance Claim Calculator System - FIXED VERSION

A Python-based insurance claim calculation system for automobile insurance. This project implements complex business rules including deductible tiers, liability ratios, and driving experience bonuses.

## Project Overview

This is the **FIXED and CORRECTED** version of the insurance claim calculator. All functional bugs have been identified and resolved.

**Changes from original**:
- ✅ Fixed boundary condition error at loss_amount = 2000
- ✅ Fixed missing driving years bonus calculation
- ✅ All 16 unit tests now pass

## Project Structure

```
issue_project_fixed/
├── src/
│   ├── __init__.py
│   └── insurance_claim.py       # Core calculation logic (FIXED)
├── tests/
│   ├── __init__.py
│   └── test_claim_calculator.py # Comprehensive test suite
├── demo_fixed.py                 # Demo showing correct calculations
├── README.md                      # This file
├── FIX_REPORT.md                  # Detailed bug fixes documentation
└── requirements.txt               # Python dependencies
```

## Business Rules

The system calculates insurance claim payouts based on:

1. **Base Payout Ratio** (by insurance type):
   - Comprehensive: 80%
   - Third Party: 60%
   - Compulsory: 50%

2. **Deductible Tiers**:
   - Loss ≤ 2000: Fixed 500 CNY
   - 2000 < Loss ≤ 10000: 10% of loss
   - Loss > 10000: 15% of loss

3. **Liability Coefficients**:
   - Full: 100%
   - Primary: 70%
   - Equal: 50%
   - Secondary: 30%
   - None: 0%

4. **Driving Years Bonus** (NOW CORRECTLY APPLIED):
   - 3+ years: +5%
   - 5+ years: +10%
   - 10+ years: +15%

5. **Special Constraints**:
   - Drunk driving: Zero payout
   - Unlicensed: Zero payout
   - Exceeds policy limit: Capped at limit
   - Minimum payout: 500 CNY (except violations)

## Quick Start

### Installation

Install dependencies (Python 3.8+ required):

```powershell
pip install -r requirements.txt
```

### Run Tests

Execute all tests - ALL should PASS:

```powershell
pytest tests/ -v
```

### Expected Test Results

**All 16 tests PASS**:
- ✅ test_deductible_below_2000
- ✅ test_deductible_exactly_2000_FAILING (NOW PASSES - boundary fixed)
- ✅ test_deductible_between_2000_and_10000
- ✅ test_deductible_above_10000
- ✅ test_comprehensive_full_liability_no_bonus
- ✅ test_third_party_primary_liability
- ✅ test_minimum_payout_threshold
- ✅ test_driving_bonus_5_years_FAILING (NOW PASSES - bonus fixed)
- ✅ test_driving_bonus_10_years_FAILING (NOW PASSES - bonus fixed)
- ✅ test_driving_bonus_3_years_FAILING (NOW PASSES - bonus fixed)
- ✅ test_drunk_driving_zero_payout
- ✅ test_unlicensed_zero_payout
- ✅ test_payout_exceeds_policy_limit
- ✅ test_calculate_claim_function
- ✅ test_zero_liability_zero_payout
- ✅ test_combined_boundary_and_bonus_bug_FAILING (NOW PASSES - both bugs fixed)

## Example Usage

```python
from src.insurance_claim import calculate_claim

# Calculate a claim with driving experience bonus
payout = calculate_claim(
    loss_amount=2000,
    insurance_type="comprehensive",
    liability_level="full",
    driving_years=5,
    policy_limit=50000
)

print(f"Payout: {payout} CNY")
# FIXED: 1320 CNY (correct calculation)
# - Loss: 2000 CNY
# - Deductible: 500 CNY (for loss ≤ 2000)
# - After deductible: 1500 CNY
# - After insurance ratio (80%): 1200 CNY
# - After driving bonus (5+ years = 10%): 1320 CNY
```

## Test Coverage

Run tests with coverage report:

```powershell
pytest tests/ --cov=src --cov-report=term-missing
```

Expected: >85% code coverage

## Bug Fixes Summary

See [FIX_REPORT.md](FIX_REPORT.md) for detailed documentation of all fixes applied.

**Quick Summary**:
1. **Boundary Condition Bug**: Changed `loss_amount < 2000` to `loss_amount <= 2000` in `_calculate_deductible()`
2. **Missing Bonus Bug**: Added call to `_apply_driving_bonus()` in `calculate_payout()`

## Technology Stack

- Python 3.8+
- pytest (testing framework)
- dataclasses (data structures)
- enum (type safety)

## Files Modified

- `src/insurance_claim.py` - Fixed both bugs
- `tests/test_claim_calculator.py` - Unchanged (tests define correct behavior)

## License

MIT License - For educational and demonstration purposes.

## Version

- **Original (Buggy)**: issue_project/
- **Fixed Version**: issue_project_fixed/ (this directory)
