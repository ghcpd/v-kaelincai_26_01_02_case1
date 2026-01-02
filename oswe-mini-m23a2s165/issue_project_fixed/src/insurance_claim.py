"""
Fixed Insurance Claim Calculator Module

This module calculates insurance claim payouts based on the business rules described
in the project README. The implementation preserves the original public API but
fixes the functional bugs from the buggy version.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class InsuranceType(Enum):
    """Types of insurance coverage"""
    COMPREHENSIVE = "comprehensive"
    THIRD_PARTY = "third_party"
    COMPULSORY = "compulsory"


class LiabilityLevel(Enum):
    """Liability levels for accidents"""
    FULL = "full"
    PRIMARY = "primary"
    EQUAL = "equal"
    SECONDARY = "secondary"
    NONE = "none"


@dataclass
class ClaimRequest:
    """Data structure for a claim request"""
    loss_amount: float
    insurance_type: InsuranceType
    liability_level: LiabilityLevel
    driving_years: int
    policy_limit: float
    is_drunk_driving: bool = False
    is_unlicensed: bool = False


class ClaimCalculator:
    """Calculator for insurance claim payouts (fixed implementation)."""

    BASE_RATIOS = {
        InsuranceType.COMPREHENSIVE: 0.80,
        InsuranceType.THIRD_PARTY: 0.60,
        InsuranceType.COMPULSORY: 0.50,
    }

    LIABILITY_COEFFICIENTS = {
        LiabilityLevel.FULL: 1.00,
        LiabilityLevel.PRIMARY: 0.70,
        LiabilityLevel.EQUAL: 0.50,
        LiabilityLevel.SECONDARY: 0.30,
        LiabilityLevel.NONE: 0.00,
    }

    MINIMUM_PAYOUT = 500.0

    def calculate_payout(self, request: ClaimRequest) -> float:
        """Calculate the final payout amount for an insurance claim.

        Preserves the original public API but fixes the following issues:
        - applies the driving-years bonus
        - enforces deductible boundary correctly via _calculate_deductible
        """
        # Violations => zero payout
        if request.is_drunk_driving or request.is_unlicensed:
            return 0.0

        # No liability => zero payout
        if request.liability_level == LiabilityLevel.NONE:
            return 0.0

        # Deductible
        deductible = self._calculate_deductible(request.loss_amount)

        base_amount = request.loss_amount - deductible

        # Apply insurance base ratio
        base_ratio = self.BASE_RATIOS[request.insurance_type]
        amount_after_base = base_amount * base_ratio

        # Apply liability coefficient
        liability_coef = self.LIABILITY_COEFFICIENTS[request.liability_level]
        amount_after_liability = amount_after_base * liability_coef

        # Apply driving years bonus (fixed: previously missing)
        amount_after_bonus = self._apply_driving_bonus(amount_after_liability, request.driving_years)

        final_amount = amount_after_bonus

        # Enforce policy limit
        if final_amount > request.policy_limit:
            final_amount = request.policy_limit

        # Minimum payout (except violations)
        if final_amount > 0 and final_amount < self.MINIMUM_PAYOUT:
            final_amount = self.MINIMUM_PAYOUT

        return round(final_amount, 2)

    def _calculate_deductible(self, loss_amount: float) -> float:
        """Calculate deductible based on loss amount tiers.

        Fixed the boundary condition so that loss_amount == 2000 uses the fixed 500
        deductible (previously it fell into the 10% tier).
        """
        if loss_amount <= 2000:
            return 500.0
        elif loss_amount <= 10000:
            return loss_amount * 0.10
        else:
            return loss_amount * 0.15

    def _apply_driving_bonus(self, amount: float, driving_years: int) -> float:
        """Apply driving experience bonus to the payout amount."""
        if driving_years >= 10:
            bonus_rate = 1.15
        elif driving_years >= 5:
            bonus_rate = 1.10
        elif driving_years >= 3:
            bonus_rate = 1.05
        else:
            bonus_rate = 1.00

        return amount * bonus_rate


def calculate_claim(loss_amount: float,
                   insurance_type: str,
                   liability_level: str,
                   driving_years: int,
                   policy_limit: float,
                   is_drunk_driving: bool = False,
                   is_unlicensed: bool = False) -> float:
    """Convenience function to calculate insurance claim payout (same public API)."""
    request = ClaimRequest(
        loss_amount=loss_amount,
        insurance_type=InsuranceType(insurance_type),
        liability_level=LiabilityLevel(liability_level),
        driving_years=driving_years,
        policy_limit=policy_limit,
        is_drunk_driving=is_drunk_driving,
        is_unlicensed=is_unlicensed
    )

    calculator = ClaimCalculator()
    return calculator.calculate_payout(request)
