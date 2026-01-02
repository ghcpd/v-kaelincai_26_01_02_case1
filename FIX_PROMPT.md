# Bug Fix Task - Insurance Claim Calculator

## Task Overview
You are a senior software engineer tasked with fixing a Python insurance claim calculator project that contains functional bugs. Your goal is to analyze the existing buggy project, identify and fix all issues, and create a corrected version in a new directory.

## Source Project Location
The buggy project is located at:
```
issue_project/
├── src/
│   ├── __init__.py
│   └── insurance_claim.py
├── tests/
│   ├── __init__.py
│   └── test_claim_calculator.py
├── demo_bugs.py
├── README.md
├── KNOWN_ISSUE.md
├── PROJECT_SUMMARY.md
├── DELIVERY.md
└── requirements.txt
```

## Your Task

### Step 1: Analyze the Buggy Project
1. Read and understand the business requirements from `README.md`
2. Review the bug documentation in `KNOWN_ISSUE.md` to understand what issues exist
3. Examine the failing tests in `tests/test_claim_calculator.py`
4. Study the buggy implementation in `src/insurance_claim.py`

### Step 2: Create Fixed Version in New Directory
Create a completely new project directory named `issue_project_fixed/` with the following structure:

```
issue_project_fixed/
├── src/
│   ├── __init__.py
│   └── insurance_claim.py          # FIXED version
├── tests/
│   ├── __init__.py
│   └── test_claim_calculator.py    # Same tests (should all pass now)
├── demo_fixed.py                    # Demo showing correct behavior
├── README.md                        # Updated documentation
├── FIX_REPORT.md                    # Document what you fixed and how
└── requirements.txt                 # Same dependencies
```

### Step 3: Fix All Bugs
- Identify and fix ALL functional bugs in the calculator
- Ensure the fixed code maintains the same public API
- Do NOT change test cases - they define the correct behavior
- All 16 tests must pass after your fixes

### Step 4: Verification Requirements
Your fixed version must:
1. Pass all 16 unit tests (currently 5 are failing)
2. Implement all business rules correctly:
   - Base payout ratios (80%, 60%, 50%)
   - Deductible tiers with correct boundary conditions
   - Liability coefficients
   - Driving years bonus (5%, 10%, 15%)
   - Special constraints (violations, policy limits, minimum payout)
3. Produce correct output for all edge cases

### Step 5: Documentation
Create `FIX_REPORT.md` in the new directory with:
1. **Summary**: Brief overview of issues found
2. **Bugs Fixed**: List each bug with:
   - File and function affected
   - Description of the problem
   - Explanation of the fix applied
3. **Test Results**: Show all tests passing
4. **Verification**: Demonstrate correct calculations with examples

## Expected Directory Structure After Completion

```
issue_project_fixed/            # Your fixed version (NEW)
├── src/
│   ├── __init__.py
│   └── insurance_claim.py      # FIXED implementation
├── tests/
│   ├── __init__.py
│   └── test_claim_calculator.py  # All tests should pass
├── demo_fixed.py                # Demo showing correct behavior
├── README.md                    # Updated documentation
├── FIX_REPORT.md                # Your fix documentation
└── requirements.txt             # Dependencies
```

Note: Create this as a sibling directory to `issue_project/`, not inside it.

## Success Criteria

Your fix is complete when:
- [ ] New directory `issue_project_fixed/` is created
- [ ] All source files are copied and bugs are fixed
- [ ] All 16 tests pass: `pytest tests/ -v` shows 16/16 passing
- [ ] Code coverage remains high (>85%)
- [ ] `FIX_REPORT.md` clearly documents all changes
- [ ] Demo script shows correct calculations
- [ ] Original `issue_project/` directory remains untouched

## Important Constraints

1. **DO NOT** modify any files in `issue_project/` directory
2. **DO NOT** change the test cases - they define correct behavior
3. **DO NOT** change the public API (class names, method signatures)
4. **DO** maintain code style and documentation quality
5. **DO** ensure backward compatibility for users of the calculator

## Hints

- Read `KNOWN_ISSUE.md` carefully - it describes the bugs but not the exact fixes
- The failing tests show expected vs actual behavior
- Some bugs may be simple (boundary conditions, missing function calls)
- Focus on making tests pass, not on over-engineering
- The buggy code structure is good - you only need targeted fixes

## Deliverables

1. Complete `issue_project_fixed/` directory with all files
2. `FIX_REPORT.md` documenting your changes
3. Passing test suite (16/16 tests)
4. Updated `README.md` noting this is the fixed version

## Getting Started

Begin by running:
```bash
cd issue_project
pytest tests/ -v
```

This will show you which tests are failing. Then analyze the code and fix the issues in your new directory.


