# Project Summary - Insurance Claim Calculator

## Overview
Complete Python project with intentionally planted functional bugs for testing and demonstration purposes.

## Directory Structure
```
issue_project/
├── src/
│   ├── __init__.py                  # Package initialization
│   └── insurance_claim.py           # Core calculator (183 lines, WITH BUGS)
├── tests/
│   ├── __init__.py                  # Test package initialization
│   └── test_claim_calculator.py     # Test suite (16 tests, 5 failing)
├── demo_bugs.py                     # Interactive bug demonstration
├── README.md                        # Setup and usage guide
├── KNOWN_ISSUE.md                   # Detailed bug documentation
└── requirements.txt                 # Python dependencies (pytest)
```

## Quick Start Command

```powershell
# One command to setup and run:
pip install -r requirements.txt; pytest tests/ -v
```

## Test Results Summary

**Total Tests**: 16
- ✅ **Passing**: 11 tests (basic functionality works)
- ❌ **Failing**: 5 tests (expose the bugs)

### Failing Tests
1. `test_deductible_exactly_2000_FAILING` - Boundary bug
2. `test_driving_bonus_3_years_FAILING` - Missing 5% bonus
3. `test_driving_bonus_5_years_FAILING` - Missing 10% bonus
4. `test_driving_bonus_10_years_FAILING` - Missing 15% bonus
5. `test_combined_boundary_and_bonus_bug_FAILING` - Both bugs combined

## Bugs Planted

### Bug #1: Boundary Condition Error
- **Location**: [src/insurance_claim.py](src/insurance_claim.py#L100-L107)
- **Issue**: `if loss_amount < 2000:` should be `if loss_amount <= 2000:`
- **Impact**: When loss = exactly 2000, uses wrong deductible tier (200 instead of 500)

### Bug #2: Missing Driving Years Bonus
- **Location**: [src/insurance_claim.py](src/insurance_claim.py#L79-L81)
- **Issue**: Code never calls `_apply_driving_bonus()` method
- **Impact**: All experienced drivers (3+ years) receive no bonus (5%, 10%, or 15%)

## Reproduction Steps

### Option 1: Run Tests
```powershell
pytest tests/ -v
```

### Option 2: Interactive Demo
```powershell
python demo_bugs.py
```

### Option 3: Manual Code
```python
from src.insurance_claim import calculate_claim

# Shows both bugs:
payout = calculate_claim(
    loss_amount=2000,
    insurance_type="comprehensive",
    liability_level="full",
    driving_years=5,
    policy_limit=50000
)

print(f"Payout: {payout}")  # 1440 (buggy)
# Expected: 1320
```

## Fix Verification

After applying the fixes documented in [KNOWN_ISSUE.md](KNOWN_ISSUE.md):
```powershell
pytest tests/ -v
# Expected: 16/16 passing ✅
```

## Technical Details

- **Language**: Python 3.8+
- **Testing**: pytest 7.4.0+
- **Dependencies**: Minimal (only pytest for testing)
- **Code Quality**: Type hints, docstrings, enums for type safety
- **Complexity**: Medium business logic, simple bug implementation

## Educational Value

This project demonstrates:
- ✅ Boundary condition errors in real business logic
- ✅ Missing feature implementation (calculated method exists but not called)
- ✅ Test-driven bug discovery
- ✅ Clear documentation of expected vs actual behavior
- ✅ Minimal reproducible example principle
