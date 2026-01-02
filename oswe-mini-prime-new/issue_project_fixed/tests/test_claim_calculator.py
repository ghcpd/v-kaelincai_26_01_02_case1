# Tests copied from original project - do not modify

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
        deductible = self.calculator._calculate_deductible(1500)
        assert deductible == 500.0, "Loss <= 2000 should have 500 fixed deductible"
    
    def test_deductible_exactly_2000_FAILING(self):
        deductible = self.calculator._calculate_deductible(2000)
        assert deductible == 500.0, f"Loss exactly 2000 should have 500 fixed deductible, got {deductible}"
    
    def test_deductible_between_2000_and_10000(self):
        deductible = self.calculator._calculate_deductible(5000)
        assert deductible == 500.0, "Loss 2000-10000 should have 10% deductible"
    
    def test_deductible_above_10000(self):
        deductible = self.calculator._calculate_deductible(15000)
        assert deductible == 2250.0, "Loss > 10000 should have 15% deductible"


class TestBasicCalculation:
    """Test basic claim calculation scenarios"""
    
    def setup_method(self):
        self.calculator = ClaimCalculator()
    
    def test_comprehensive_full_liability_no_bonus(self):
        request = ClaimRequest(
            loss_amount=5000,
            insurance_type=InsuranceType.COMPREHENSIVE,
            liability_level=LiabilityLevel.FULL,
            driving_years=1,
            policy_limit=50000
        )
        payout = self.calculator.calculate_payout(request)
        assert payout == 3600.0
    
    def test_third_party_primary_liability(self):
        request = ClaimRequest(
            loss_amount=8000,
            insurance_type=InsuranceType.THIRD_PARTY,
            liability_level=LiabilityLevel.PRIMARY,
            driving_years=2,
            policy_limit=50000
        )
        payout = self.calculator.calculate_payout(request)
        assert payout == 3024.0
    
    def test_minimum_payout_threshold(self):
        request = ClaimRequest(
            loss_amount=1000,
            insurance_type=InsuranceType.COMPULSORY,
            liability_level=LiabilityLevel.SECONDARY,
            driving_years=1,
            policy_limit=50000
        )
        payout = self.calculator.calculate_payout(request)
        assert payout == 500.0


class TestDrivingYearsBonus:
    """Test driving years bonus calculation"""
    
    def setup_method(self):
        self.calculator = ClaimCalculator()
    
    def test_driving_bonus_5_years_FAILING(self):
        request = ClaimRequest(
            loss_amount=2000,
            insurance_type=InsuranceType.COMPREHENSIVE,
            liability_level=LiabilityLevel.FULL,
            driving_years=5,
            policy_limit=50000
        )
        payout = self.calculator.calculate_payout(request)
        assert payout == 1320.0, f"Expected 1320 with 5-year bonus, got {payout}"
    
    def test_driving_bonus_10_years_FAILING(self):
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
    def setup_method(self):
        self.calculator = ClaimCalculator()
    
    def test_drunk_driving_zero_payout(self):
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
    def setup_method(self):
        self.calculator = ClaimCalculator()
    
    def test_payout_exceeds_policy_limit(self):
        request = ClaimRequest(
            loss_amount=50000,
            insurance_type=InsuranceType.COMPREHENSIVE,
            liability_level=LiabilityLevel.FULL,
            driving_years=1,
            policy_limit=10000
        )
        payout = self.calculator.calculate_payout(request)
        assert payout == 10000.0


class TestConvenienceFunction:
    def test_calculate_claim_function(self):
        payout = calculate_claim(
            loss_amount=5000,
            insurance_type="comprehensive",
            liability_level="full",
            driving_years=1,
            policy_limit=50000
        )
        assert payout == 3600.0


class TestEdgeCases:
    def setup_method(self):
        self.calculator = ClaimCalculator()
    
    def test_zero_liability_zero_payout(self):
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
        request = ClaimRequest(
            loss_amount=2000,
            insurance_type=InsuranceType.COMPREHENSIVE,
            liability_level=LiabilityLevel.FULL,
            driving_years=5,
            policy_limit=50000
        )
        payout = self.calculator.calculate_payout(request)
        assert payout == 1320.0, f"Expected 1320, got {payout}. Bugs: boundary condition + missing bonus"
