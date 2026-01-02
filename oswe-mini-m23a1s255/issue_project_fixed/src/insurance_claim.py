"""
Fixed Insurance Claim Calculator implementation.
- Boundary bug fixed in _calculate_deductible (<= 2000)
- Driving-years bonus is now applied in calculate_payout
- Small robustness additions (no negative base amount)
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class InsuranceType(Enum):
    COMPREHENSIVE = "comprehensive"
    THIRD_PARTY = "third_party"
    COMPULSORY = "compulsory"


class LiabilityLevel(Enum):
    FULL = "full"
    PRIMARY = "primary"
    EQUAL = "equal"
    SECONDARY = "secondary"
    NONE = "none"


@dataclass
class ClaimRequest:
    loss_amount: float
    insurance_type: InsuranceType
    liability_level: LiabilityLevel
    driving_years: int
    policy_limit: float
    is_drunk_driving: bool = False
    is_unlicensed: bool = False


class ClaimCalculator:
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
        # Violations or no-liability => zero payout
        if request.is_drunk_driving or request.is_unlicensed:
            return 0.0
        if request.liability_level == LiabilityLevel.NONE:
            return 0.0

        deductible = self._calculate_deductible(request.loss_amount)
        base_amount = max(request.loss_amount - deductible, 0.0)

        base_ratio = self.BASE_RATIOS[request.insurance_type]
        amount_after_base = base_amount * base_ratio

        liability_coef = self.LIABILITY_COEFFICIENTS[request.liability_level]
        amount_after_liability = amount_after_base * liability_coef

        # FIX: apply driving-years bonus
        amount_after_bonus = self._apply_driving_bonus(amount_after_liability, request.driving_years)

        # Enforce policy limit
        final_amount = min(amount_after_bonus, request.policy_limit)

        # Enforce minimum payout (except violations which already returned 0)
        if 0 < final_amount < self.MINIMUM_PAYOUT:
            final_amount = self.MINIMUM_PAYOUT

        return round(final_amount, 2)

    def _calculate_deductible(self, loss_amount: float) -> float:
        # FIX: boundary condition - loss_amount <= 2000 uses fixed 500
        if loss_amount <= 2000:
            return 500.0
        elif loss_amount <= 10000:
            return loss_amount * 0.10
        else:
            return loss_amount * 0.15

    def _apply_driving_bonus(self, amount: float, driving_years: int) -> float:
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
    request = ClaimRequest(
        loss_amount=loss_amount,
        insurance_type=InsuranceType(insurance_type),
        liability_level=LiabilityLevel(liability_level),
        driving_years=driving_years,
        policy_limit=policy_limit,
        is_drunk_driving=is_drunk_driving,
        is_unlicensed=is_unlicensed,
    )
    return ClaimCalculator().calculate_payout(request)
