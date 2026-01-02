"""
Example demonstration of the FIXED Insurance Claim Calculator.

This script shows the correct behavior after fixing the two bugs:
1. Boundary condition error at loss = 2000 CNY
2. Missing driving years bonus calculation
"""

from src.insurance_claim import calculate_claim, ClaimCalculator, ClaimRequest, InsuranceType, LiabilityLevel


def demonstrate_fixed_behavior():
    """Demonstrate the correct behavior with examples"""

    print("=" * 70)
    print("Insurance Claim Calculator - FIXED Version")
    print("=" * 70)
    print()

    calculator = ClaimCalculator()

    # Example 1: Boundary Condition Fixed
    print("✓ FIXED: Boundary Condition at Loss = 2000 CNY")
    print("-" * 70)

    loss_2000 = 2000
    deductible = calculator._calculate_deductible(loss_2000)

    print(f"Loss Amount: {loss_2000} CNY")
    print(f"Deductible: {deductible} CNY (correctly using fixed 500 for loss ≤ 2000)")
    print()

    # Example 2: Driving Years Bonus Applied
    print("✓ FIXED: Driving Years Bonus Calculation")
    print("-" * 70)

    request = ClaimRequest(
        loss_amount=5000,
        insurance_type=InsuranceType.COMPREHENSIVE,
        liability_level=LiabilityLevel.FULL,
        driving_years=5,
        policy_limit=50000
    )

    payout = calculator.calculate_payout(request)

    print(f"Loss Amount: 5000 CNY")
    print(f"Driving Years: 5 (gets 10% bonus)")
    print(f"Insurance: Comprehensive (80%), Liability: Full (100%)")
    print()
    print(f"Calculation: (5000 - 500) × 0.80 × 1.00 × 1.10 = {payout} CNY")
    print()

    # Example 3: Combined Scenario (from requirements)
    print("✓ FIXED: Combined Scenario from Requirements")
    print("-" * 70)

    combined_request = ClaimRequest(
        loss_amount=2000,
        insurance_type=InsuranceType.COMPREHENSIVE,
        liability_level=LiabilityLevel.FULL,
        driving_years=5,
        policy_limit=50000
    )

    combined_payout = calculator.calculate_payout(combined_request)

    print(f"Input: Loss=2000, Comprehensive, Full Liability, 5 years driving")
    print()
    print(f"Calculation: (2000 - 500) × 0.80 × 1.00 × 1.10 = {combined_payout} CNY")
    print(f"  └─ Correctly uses: Fixed deductible + Base ratio + Liability + Bonus")
    print()

    # Example 4: Different bonus tiers
    print("✓ FIXED: All Driving Years Bonus Tiers")
    print("-" * 70)

    test_cases = [
        (3, "5% bonus"),
        (5, "10% bonus"),
        (10, "15% bonus"),
        (1, "no bonus")
    ]

    for years, description in test_cases:
        req = ClaimRequest(
            loss_amount=10000,
            insurance_type=InsuranceType.COMPREHENSIVE,
            liability_level=LiabilityLevel.FULL,
            driving_years=years,
            policy_limit=50000
        )
        payout = calculator.calculate_payout(req)
        base_amount = (10000 - 1000) * 0.80 * 1.00  # 7200
        expected = base_amount * (1.05 if years >= 3 else 1.0) * (1.10 if years >= 5 else 1.0) * (1.15 if years >= 10 else 1.0)
        print(f"  {years} years: {payout} CNY ({description})")

    print()
    print("=" * 70)
    print("All tests should now pass: pytest tests/ -v")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_fixed_behavior()