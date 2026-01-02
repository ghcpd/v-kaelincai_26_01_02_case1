"""
Example demonstration of the bugs in the Insurance Claim Calculator.

This script shows the difference between expected and actual behavior
for the two intentionally planted bugs.
"""

from src.insurance_claim import calculate_claim, ClaimCalculator, ClaimRequest, InsuranceType, LiabilityLevel


def demonstrate_bugs():
    """Demonstrate the two bugs with clear examples"""
    
    print("=" * 70)
    print("Insurance Claim Calculator - Bug Demonstration")
    print("=" * 70)
    print()
    
    # Bug #1: Boundary Condition Error
    print("BUG #1: Boundary Condition at Loss = 2000 CNY")
    print("-" * 70)
    
    calculator = ClaimCalculator()
    loss_2000 = 2000
    
    deductible_actual = calculator._calculate_deductible(loss_2000)
    deductible_expected = 500.0
    
    print(f"Loss Amount: {loss_2000} CNY")
    print(f"Expected Deductible: {deductible_expected} CNY (fixed for loss ≤ 2000)")
    print(f"Actual Deductible:   {deductible_actual} CNY (wrongly using 10% tier)")
    print(f"Error: {deductible_actual - deductible_expected:+.2f} CNY")
    print()
    
    # Bug #2: Missing Driving Years Bonus
    print("BUG #2: Missing Driving Years Bonus")
    print("-" * 70)
    
    request = ClaimRequest(
        loss_amount=5000,
        insurance_type=InsuranceType.COMPREHENSIVE,
        liability_level=LiabilityLevel.FULL,
        driving_years=5,
        policy_limit=50000
    )
    
    actual_payout = calculator.calculate_payout(request)
    
    # Manual calculation with bonus
    deductible = 500  # 5000 is in the 2000-10000 tier, so 10%
    after_deductible = 5000 - deductible
    after_base_ratio = after_deductible * 0.80
    after_liability = after_base_ratio * 1.00
    expected_with_bonus = after_liability * 1.10  # 5 years = 10% bonus
    
    print(f"Loss Amount: 5000 CNY")
    print(f"Driving Years: 5 (should get 10% bonus)")
    print(f"Insurance: Comprehensive (80%), Liability: Full (100%)")
    print()
    print(f"Calculation breakdown:")
    print(f"  Loss - Deductible: 5000 - 500 = {after_deductible}")
    print(f"  × Base ratio (80%): {after_deductible} × 0.80 = {after_base_ratio}")
    print(f"  × Liability (100%): {after_base_ratio} × 1.00 = {after_liability}")
    print(f"  × Driving bonus (10%): {after_liability} × 1.10 = {expected_with_bonus}")
    print()
    print(f"Expected Payout: {expected_with_bonus} CNY (with bonus)")
    print(f"Actual Payout:   {actual_payout} CNY (bonus NOT applied)")
    print(f"Missing Amount: {expected_with_bonus - actual_payout:+.2f} CNY")
    print()
    
    # Combined Bug Example (from requirements)
    print("COMBINED BUGS: The Scenario from Requirements")
    print("-" * 70)
    
    combined_request = ClaimRequest(
        loss_amount=2000,
        insurance_type=InsuranceType.COMPREHENSIVE,
        liability_level=LiabilityLevel.FULL,
        driving_years=5,
        policy_limit=50000
    )
    
    actual_combined = calculator.calculate_payout(combined_request)
    
    # Expected calculation (with both bugs fixed)
    expected_deductible = 500  # Should be fixed 500
    actual_deductible_used = 200  # But system uses 10%
    
    expected_calc = (2000 - 500) * 0.80 * 1.00 * 1.10
    actual_calc = (2000 - 200) * 0.80 * 1.00  # Wrong deductible + no bonus
    
    print(f"Input: Loss=2000, Comprehensive, Full Liability, 5 years driving")
    print()
    print(f"EXPECTED Calculation:")
    print(f"  (2000 - 500) × 0.80 × 1.00 × 1.10 = {expected_calc} CNY")
    print(f"  └─ Uses: Fixed deductible + Base ratio + Liability + Bonus")
    print()
    print(f"ACTUAL (Buggy) Calculation:")
    print(f"  (2000 - 200) × 0.80 × 1.00 = {actual_combined} CNY")
    print(f"  └─ Uses: Wrong deductible (10%) + NO bonus applied")
    print()
    print(f"Net Error: {actual_combined - expected_calc:+.2f} CNY")
    print(f"  ├─ Wrong deductible: +{(200 - 500) * 0.80} CNY")
    print(f"  └─ Missing bonus: -{expected_calc - (2000-500)*0.80} CNY")
    print()
    
    print("=" * 70)
    print("Run 'pytest tests/ -v' to see all failing test cases")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_bugs()
