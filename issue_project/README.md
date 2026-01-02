# Insurance Claim Calculator System

A Python-based insurance claim calculation system for automobile insurance. This project implements complex business rules including deductible tiers, liability ratios, and driving experience bonuses.

## Project Overview

This is a minimal reproducible project that demonstrates a **Functional Bug** scenario where the system:
- Gives wrong output due to boundary condition errors
- Ignores specified constraints (driving years bonus)
- Features don't behave as specified in requirements

## Project Structure

```
issue_project/
├── src/
│   ├── __init__.py
│   └── insurance_claim.py       # Core calculation logic (WITH BUGS)
├── tests/
│   ├── __init__.py
│   └── test_claim_calculator.py # Comprehensive test suite
├── README.md                     # This file
├── KNOWN_ISSUE.md               # Bug documentation
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

Execute all tests including the failing ones:

```powershell
pytest tests/ -v
```

### Expected Test Results

**Passing Tests**: 9 tests should pass (basic functionality works)

**Failing Tests**: 5 tests should FAIL, exposing the bugs:
- `test_deductible_exactly_2000_FAILING` - Boundary condition error
- `test_driving_bonus_5_years_FAILING` - Missing 10% bonus
- `test_driving_bonus_10_years_FAILING` - Missing 15% bonus
- `test_driving_bonus_3_years_FAILING` - Missing 5% bonus
- `test_combined_boundary_and_bonus_bug_FAILING` - Both bugs combined

## Example Usage

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

print(f"Payout: {payout} CNY")
# Current (buggy): 1440 CNY
# Expected: 1320 CNY
```

## Known Issues

This project intentionally contains bugs for demonstration purposes. See [KNOWN_ISSUE.md](KNOWN_ISSUE.md) for details.

**Summary**:
1. Boundary condition error at loss_amount = 2000
2. Missing driving years bonus calculation

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
