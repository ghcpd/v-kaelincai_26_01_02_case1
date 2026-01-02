# issue_project_fixed — Insurance Claim Calculator (FIXED)

This repository contains the fixed version of the Insurance Claim Calculator. It preserves the original public API and fixes the functional bugs described in the upstream `issue_project`.

Key fixes:
- Corrected deductible boundary (loss == 2000)
- Applied driving-years bonus correctly

Run the test-suite:

```powershell
cd issue_project_fixed
pytest tests/ -v
```
