"""
Copied test suite from the original project (unchanged).
All tests in this file should pass against the fixed implementation.
"""

import pytest
from src.insurance_claim import (
    ClaimCalculator,
    ClaimRequest,
    InsuranceType,
    LiabilityLevel,
    calculate_claim
)


class TestDeductibleCalculation:
    """Test deductible calculation logic"""

    def setup_method(self):
        self.calculator = ClaimCalculator()

    def test_deductible_below_2000(self):
        """Test deductible for loss amount below 2000"""
        deductible = self.calculator._calculate_deductible(1500)
        assert deductible == 500.0, "Loss <= 2000 should have 500 fixed deductible"

    def test_deductible_exactly_2000_FAILING(self):
        """
        FAILING TEST: Boundary condition error

        When loss_amount is exactly 2000, should use 500 fixed deductible,
        but current implementation incorrectly uses 10% tier.

        Expected: 500
        Actual: 200 (2000 * 0.10)
        """
        deductible = self.calculator._calculate_deductible(2000)
        assert deductible == 500.0, f"Loss exactly 2000 should have 500 fixed deductible, got {deductible}"

    def test_deductible_between_2000_and_10000(self):
        """Test deductible for loss amount between 2000 and 10000"""
        deductible = self.calculator._calculate_deductible(5000)
        assert deductible == 500.0, "Loss 2000-10000 should have 10% deductible"

    def test_deductible_above_10000(self):
        """Test deductible for loss amount above 10000"""
        deductible = self.calculator._calculate_deductible(15000)
        assert deductible == 2250.0, "Loss > 10000 should have 15% deductible"


class TestBasicCalculation:
    """Test basic claim calculation scenarios"""

    def setup_method(self):
        self.calculator = ClaimCalculator()

    def test_comprehensive_full_liability_no_bonus(self):
        """Test comprehensive insurance with full liability, no driving bonus"""
        request = ClaimRequest(
            loss_amount=5000,
            insurance_type=InsuranceType.COMPREHENSIVE,
            liability_level=LiabilityLevel.FULL,
            driving_years=1,
            policy_limit=50000
        )
        # (5000 - 500) * 0.80 * 1.00 = 3600
        payout = self.calculator.calculate_payout(request)
        assert payout == 3600.0

    def test_third_party_primary_liability(self):
        """Test third party insurance with primary liability"""
        request = ClaimRequest(
            loss_amount=8000,
            insurance_type=InsuranceType.THIRD_PARTY,
            liability_level=LiabilityLevel.PRIMARY,
            driving_years=2,
            policy_limit=50000
        )
        # (8000 - 800) * 0.60 * 0.70 = 3024
        payout = self.calculator.calculate_payout(request)
        assert payout == 3024.0

    def test_minimum_payout_threshold(self):
        """Test minimum payout threshold of 500"""
        request = ClaimRequest(
            loss_amount=1000,
            insurance_type=InsuranceType.COMPULSORY,
            liability_level=LiabilityLevel.SECONDARY,
            driving_years=1,
            policy_limit=50000
        )
        # (1000 - 500) * 0.50 * 0.30 = 75, should be raised to 500
        payout = self.calculator.calculate_payout(request)
        assert payout == 500.0


class TestDrivingYearsBonus:
    """Test driving years bonus calculation"""

    def setup_method(self):
        self.calculator = ClaimCalculator()

    def test_driving_bonus_5_years_FAILING(self):
        """
        FAILING TEST: Missing driving years bonus

        For 5 years driving experience, should get 10% bonus.
        Current implementation skips this calculation entirely.

        Expected: (2000 - 500) * 0.80 * 1.00 * 1.10 = 1320
        Actual: (2000 - 500) * 0.80 * 1.00 = 1200
        """
        request = ClaimRequest(
            loss_amount=2000,
            insurance_type=InsuranceType.COMPREHENSIVE,
            liability_level=LiabilityLevel.FULL,
            driving_years=5,
            policy_limit=50000
        )
        payout = self.calculator.calculate_payout(request)
        # BUG: This test will fail because driving bonus is not applied
        # Expected calculation with fix: (2000 - 200) * 0.80 * 1.00 * 1.10 = 1584
        # But there's also the boundary bug, so actual is: (2000 - 200) * 0.80 * 1.00 = 1440
        # With boundary fix: (2000 - 500) * 0.80 * 1.00 = 1200
        # With both fixes: (2000 - 500) * 0.80 * 1.00 * 1.10 = 1320
        assert payout == 1320.0, f"Expected 1320 with 5-year bonus, got {payout}"

    def test_driving_bonus_10_years_FAILING(self):
        """
        FAILING TEST: Missing 15% bonus for 10+ years driving experience

        Expected: (10000 - 1000) * 0.80 * 1.00 * 1.15 = 8280
        Actual: (10000 - 1000) * 0.80 * 1.00 = 7200
        """
        request = ClaimRequest(
            loss_amount=10000,
            insurance_type=InsuranceType.COMPREHENSIVE,
            liability_level=LiabilityLevel.FULL,
            driving_years=10,
            policy_limit=50000
        )
        payout = self.calculator.calculate_payout(request)
        assert payout == 8280.0, f"Expected 8280 with 10-year bonus, got {payout}"

    def test_driving_bonus_3_years_FAILING(self):
        """
        FAILING TEST: Missing 5% bonus for 3-4 years driving experience

        Expected: (5000 - 500) * 0.80 * 1.00 * 1.05 = 3780
        Actual: (5000 - 500) * 0.80 * 1.00 = 3600
        """
        request = ClaimRequest(
            loss_amount=5000,
            insurance_type=InsuranceType.COMPREHENSIVE,
            liability_level=LiabilityLevel.FULL,
            driving_years=3,
            policy_limit=50000
        )
        payout = self.calculator.calculate_payout(request)
        assert payout == 3780.0, f"Expected 3780 with 3-year bonus, got {payout}"


class TestViolations:
    """Test violation scenarios (drunk driving, unlicensed)"""

    def setup_method(self):
        self.calculator = ClaimCalculator()

    def test_drunk_driving_zero_payout(self):
        """Drunk driving should result in zero payout"""
        request = ClaimRequest(
            loss_amount=10000,
            insurance_type=InsuranceType.COMPREHENSIVE,
            liability_level=LiabilityLevel.FULL,
            driving_years=5,
            policy_limit=50000,
            is_drunk_driving=True
        )
        payout = self.calculator.calculate_payout(request)
        assert payout == 0.0

    def test_unlicensed_zero_payout(self):
        """Unlicensed driving should result in zero payout"""
        request = ClaimRequest(
            loss_amount=10000,
            insurance_type=InsuranceType.COMPREHENSIVE,
            liability_level=LiabilityLevel.FULL,
            driving_years=5,
            policy_limit=50000,
            is_unlicensed=True
        )
        payout = self.calculator.calculate_payout(request)
        assert payout == 0.0


class TestPolicyLimit:
    """Test policy limit enforcement"""

    def setup_method(self):
        self.calculator = ClaimCalculator()

    def test_payout_exceeds_policy_limit(self):
        """Payout should not exceed policy limit"""
        request = ClaimRequest(
            loss_amount=50000,
            insurance_type=InsuranceType.COMPREHENSIVE,
            liability_level=LiabilityLevel.FULL,
            driving_years=1,
            policy_limit=10000
        )
        payout = self.calculator.calculate_payout(request)
        assert payout == 10000.0, "Payout should be capped at policy limit"


class TestConvenienceFunction:
    """Test the convenience function interface"""

    def test_calculate_claim_function(self):
        """Test the calculate_claim convenience function"""
        payout = calculate_claim(
            loss_amount=5000,
            insurance_type="comprehensive",
            liability_level="full",
            driving_years=1,
            policy_limit=50000
        )
        assert payout == 3600.0


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def setup_method(self):
        self.calculator = ClaimCalculator()

    def test_zero_liability_zero_payout(self):
        """No liability should result in zero payout"""
        request = ClaimRequest(
            loss_amount=10000,
            insurance_type=InsuranceType.COMPREHENSIVE,
            liability_level=LiabilityLevel.NONE,
            driving_years=5,
            policy_limit=50000
        )
        payout = self.calculator.calculate_payout(request)
        assert payout == 0.0

    def test_combined_boundary_and_bonus_bug_FAILING(self):
        """
        FAILING TEST: Combination of both bugs

        This is the exact scenario from the requirements:
        - Loss: 2000 (boundary condition)
        - Insurance: Comprehensive (80%)
        - Liability: Full (100%)
        - Driving years: 5 (10% bonus)

        Expected: (2000 - 500) * 0.80 * 1.00 * 1.10 = 1320
        Actual: (2000 - 200) * 0.80 * 1.00 = 1440

        This exposes BOTH bugs:
        1. Wrong deductible (200 instead of 500)
        2. Missing driving bonus (no 1.10 multiplier)
        """
        request = ClaimRequest(
            loss_amount=2000,
            insurance_type=InsuranceType.COMPREHENSIVE,
            liability_level=LiabilityLevel.FULL,
            driving_years=5,
            policy_limit=50000
        )
        payout = self.calculator.calculate_payout(request)
        assert payout == 1320.0, f"Expected 1320, got {payout}. Bugs: boundary condition + missing bonus"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])