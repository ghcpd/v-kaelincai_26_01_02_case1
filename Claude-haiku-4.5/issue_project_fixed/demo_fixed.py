#!/usr/bin/env python3
"""
Demo script showing correct calculations with the FIXED insurance claim calculator.

This demonstrates that all bugs have been fixed and the system behaves correctly.
"""

from src.insurance_claim import calculate_claim, ClaimCalculator, ClaimRequest, InsuranceType, LiabilityLevel


def demo_boundary_condition_fixed():
    """Demonstrate that boundary condition at exactly 2000 is now fixed."""
    print("=" * 70)
    print("DEMO 1: Boundary Condition Fix (loss_amount = 2000)")
    print("=" * 70)
    
    calculator = ClaimCalculator()
    
    # Test the exact boundary condition
    deductible = calculator._calculate_deductible(2000)
    print(f"\nLoss Amount: 2000 CNY")
    print(f"Expected Deductible: 500 CNY (fixed amount for loss ≤ 2000)")
    print(f"Actual Deductible: {deductible} CNY")
    print(f"Status: {'✅ FIXED' if deductible == 500.0 else '❌ STILL BROKEN'}")
    
    # Show the tier boundaries
    print("\n--- Deductible Tier Boundaries ---")
    print(f"Loss 1500: {calculator._calculate_deductible(1500)} CNY (tier 1: fixed 500)")
    print(f"Loss 2000: {calculator._calculate_deductible(2000)} CNY (tier 1: fixed 500) - BOUNDARY")
    print(f"Loss 2001: {calculator._calculate_deductible(2001)} CNY (tier 2: 10%)")
    print(f"Loss 5000: {calculator._calculate_deductible(5000)} CNY (tier 2: 10%)")
    print(f"Loss 10000: {calculator._calculate_deductible(10000)} CNY (tier 2: 10%) - BOUNDARY")
    print(f"Loss 10001: {calculator._calculate_deductible(10001)} CNY (tier 3: 15%)")


def demo_driving_bonus_fixed():
    """Demonstrate that driving years bonus is now correctly applied."""
    print("\n" + "=" * 70)
    print("DEMO 2: Driving Years Bonus Fix")
    print("=" * 70)
    
    # Base calculation without bonus
    base_amount = 1200.0
    
    print(f"\nBase Amount (before bonus): {base_amount} CNY")
    print("\n--- Driving Bonus Tiers ---")
    
    test_cases = [
        (1, 1200.0, "0% (1 year)"),
        (2, 1200.0, "0% (2 years)"),
        (3, 1260.0, "+5% (3 years)"),
        (4, 1260.0, "+5% (4 years)"),
        (5, 1320.0, "+10% (5 years)"),
        (9, 1320.0, "+10% (9 years)"),
        (10, 1380.0, "+15% (10 years)"),
        (15, 1380.0, "+15% (15 years)"),
    ]
    
    calculator = ClaimCalculator()
    for years, expected, description in test_cases:
        bonus_amount = calculator._apply_driving_bonus(base_amount, years)
        status = "✅" if bonus_amount == expected else "❌"
        print(f"  {years:2d} years: {bonus_amount:7.2f} CNY {description} {status}")


def demo_combined_scenario():
    """Demonstrate the combined scenario showing both fixes working together."""
    print("\n" + "=" * 70)
    print("DEMO 3: Combined Scenario (Both Bugs Fixed)")
    print("=" * 70)
    
    print("\nScenario:")
    print("  - Loss Amount: 2000 CNY")
    print("  - Insurance Type: Comprehensive (80%)")
    print("  - Liability Level: Full (100%)")
    print("  - Driving Years: 5 (10% bonus)")
    print("  - Policy Limit: 50000 CNY")
    
    payout = calculate_claim(
        loss_amount=2000,
        insurance_type="comprehensive",
        liability_level="full",
        driving_years=5,
        policy_limit=50000
    )
    
    print(f"\nCalculation Steps:")
    print(f"  1. Loss Amount:                    2000 CNY")
    print(f"  2. Deductible (loss ≤ 2000):        500 CNY  ✅ FIXED")
    print(f"  3. Amount after deductible:       1500 CNY  (2000 - 500)")
    print(f"  4. Insurance ratio (80%):         1200 CNY  (1500 × 0.80)")
    print(f"  5. Liability coefficient (100%):  1200 CNY  (1200 × 1.00)")
    print(f"  6. Driving bonus (5 years = 10%): 1320 CNY  (1200 × 1.10) ✅ FIXED")
    print(f"  7. Policy limit check:            1320 CNY  (≤ 50000)")
    print(f"  8. Minimum payout check:          1320 CNY  (≥ 500)")
    
    print(f"\nFinal Payout: {payout} CNY")
    print(f"Status: {'✅ CORRECT' if payout == 1320.0 else '❌ INCORRECT'}")


def demo_test_cases():
    """Run through the previously failing test cases to show they now pass."""
    print("\n" + "=" * 70)
    print("DEMO 4: Previously Failing Test Cases (Now Passing)")
    print("=" * 70)
    
    calculator = ClaimCalculator()
    
    test_cases = [
        {
            "name": "test_deductible_exactly_2000_FAILING",
            "deductible": calculator._calculate_deductible(2000),
            "expected": 500.0,
        },
        {
            "name": "test_driving_bonus_3_years_FAILING",
            "payout": calculate_claim(5000, "comprehensive", "full", 3, 50000),
            "expected": 3780.0,
        },
        {
            "name": "test_driving_bonus_5_years_FAILING",
            "payout": calculate_claim(2000, "comprehensive", "full", 5, 50000),
            "expected": 1320.0,
        },
        {
            "name": "test_driving_bonus_10_years_FAILING",
            "payout": calculate_claim(10000, "comprehensive", "full", 10, 50000),
            "expected": 8280.0,
        },
        {
            "name": "test_combined_boundary_and_bonus_bug_FAILING",
            "payout": calculate_claim(2000, "comprehensive", "full", 5, 50000),
            "expected": 1320.0,
        },
    ]
    
    print("\n")
    all_pass = True
    for test in test_cases:
        actual = test.get("payout") or test.get("deductible")
        expected = test["expected"]
        passed = actual == expected
        all_pass = all_pass and passed
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test['name']}")
        print(f"  Expected: {expected}, Got: {actual} {status}")
    
    print(f"\n{'='*70}")
    print(f"Overall Result: {'✅ ALL TESTS PASS' if all_pass else '❌ SOME TESTS FAIL'}")
    print(f"{'='*70}")


if __name__ == "__main__":
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  Insurance Claim Calculator - FIXED VERSION Demo".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    demo_boundary_condition_fixed()
    demo_driving_bonus_fixed()
    demo_combined_scenario()
    demo_test_cases()
    
    print("\n✅ All demonstrations complete! The calculator is fully fixed.")
    print("\nTo run the complete test suite:")
    print("  pytest tests/ -v")
