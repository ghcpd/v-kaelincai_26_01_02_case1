# Insurance Claim Calculator System - FIXED

A Python-based insurance claim calculation system for automobile insurance. This project implements complex business rules correctly including deductible tiers, liability ratios, and driving experience bonuses.

## Project Overview

This is the **FIXED** version of the insurance claim calculator. All previously identified bugs have been resolved:

- ✅ Boundary condition error at loss = 2000 CNY (now correctly uses fixed 500 deductible)
- ✅ Missing driving years bonus calculation (now properly applies bonuses)
- ✅ All business rules implemented correctly

## Project Structure

```
issue_project_fixed/
├── src/
│   ├── __init__.py
│   └── insurance_claim.py       # Core calculation logic (FIXED)
├── tests/
│   ├── __init__.py
│   └── test_claim_calculator.py # Comprehensive test suite (all pass)
├── demo_fixed.py                # Demonstration of correct behavior
├── README.md                    # This file
├── FIX_REPORT.md                # Documentation of fixes applied
└── requirements.txt             # Python dependencies
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

4. **Driving Years Bonus**:
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

Execute all tests - they should all pass:

```powershell
pytest tests/ -v
```

### Expected Test Results

**All 16 tests should pass** ✅

### Run Demo

See the correct behavior in action:

```powershell
python demo_fixed.py
```

### Example Usage

```python
from src.insurance_claim import calculate_claim

# Calculate a claim
payout = calculate_claim(
    loss_amount=2000,
    insurance_type="comprehensive",
    liability_level="full",
    driving_years=5,
    policy_limit=50000
)

print(f"Payout: {payout} CNY")  # 1320.0 CNY (correct)
```

## Test Coverage

Run tests with coverage report:

```powershell
pytest tests/ --cov=src --cov-report=term-missing
```

## Technology Stack

- Python 3.8+
- pytest (testing framework)
- dataclasses (data structures)
- enum (type safety)

## License

MIT License - For educational and demonstration purposes.