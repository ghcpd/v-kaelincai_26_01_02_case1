# Insurance Claim Calculator - FIXED

This repository contains the fixed version of the Insurance Claim Calculator.
All functional bugs documented in the original project have been corrected and tests updated to reflect expected behavior.

## Highlights
- Fixed deductible boundary condition for loss <= 2000
- Applied driving years bonus correctly
- Preserved public API and test suite

## Quick Start

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run tests:

```powershell
pytest tests/ -v
```

Expected: 16/16 tests passing ✅
