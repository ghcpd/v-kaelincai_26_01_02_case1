"""
Insurance Claim Calculator Module

This module calculates insurance claim payouts based on multiple business rules including
insurance type, deductible tiers, liability ratios, and driving experience bonuses.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class InsuranceType(Enum):
    """Types of insurance coverage"""
    COMPREHENSIVE = "comprehensive"  # 全险
    THIRD_PARTY = "third_party"      # 三者险
    COMPULSORY = "compulsory"        # 交强险


class LiabilityLevel(Enum):
    """Liability levels for accidents"""
    FULL = "full"                    # 全责
    PRIMARY = "primary"              # 主要责任
    EQUAL = "equal"                  # 同等责任
    SECONDARY = "secondary"          # 次要责任
    NONE = "none"                    # 无责


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
    """
    Calculator for insurance claim payouts.
    
    Implements all business rules correctly:
    - Base payout ratios by insurance type
    - Deductible tiers with correct boundary conditions
    - Liability coefficients
    - Driving years bonus calculation
    - Special constraints and minimum payouts
    """
    
    # Base payout ratios by insurance type
    BASE_RATIOS = {
        InsuranceType.COMPREHENSIVE: 0.80,
        InsuranceType.THIRD_PARTY: 0.60,
        InsuranceType.COMPULSORY: 0.50,
    }
    
    # Liability coefficients
    LIABILITY_COEFFICIENTS = {
        LiabilityLevel.FULL: 1.00,
        LiabilityLevel.PRIMARY: 0.70,
        LiabilityLevel.EQUAL: 0.50,
        LiabilityLevel.SECONDARY: 0.30,
        LiabilityLevel.NONE: 0.00,
    }
    
    # Minimum payout threshold
    MINIMUM_PAYOUT = 500.0
    
    def calculate_payout(self, request: ClaimRequest) -> float:
        """
        Calculate the final payout amount for an insurance claim.
        
        Args:
            request: ClaimRequest object containing all claim details
            
        Returns:
            Final payout amount in CNY
        """
        # Check for violations - zero payout
        if request.is_drunk_driving or request.is_unlicensed:
            return 0.0
        
        # Check for zero liability
        if request.liability_level == LiabilityLevel.NONE:
            return 0.0
        
        # Calculate deductible amount
        deductible = self._calculate_deductible(request.loss_amount)
        
        # Calculate base amount after deductible
        base_amount = request.loss_amount - deductible
        
        # Apply insurance type ratio
        base_ratio = self.BASE_RATIOS[request.insurance_type]
        amount_after_base = base_amount * base_ratio
        
        # Apply liability coefficient
        liability_coef = self.LIABILITY_COEFFICIENTS[request.liability_level]
        amount_after_liability = amount_after_base * liability_coef
        
        # Apply driving years bonus
        amount_after_bonus = self._apply_driving_bonus(amount_after_liability, request.driving_years)
        
        # Check policy limit
        if amount_after_bonus > request.policy_limit:
            final_amount = request.policy_limit
        else:
            final_amount = amount_after_bonus
        
        # Apply minimum payout rule (except for violations)
        if final_amount > 0 and final_amount < self.MINIMUM_PAYOUT:
            final_amount = self.MINIMUM_PAYOUT
        
        return round(final_amount, 2)
    
    def _calculate_deductible(self, loss_amount: float) -> float:
        """
        Calculate deductible based on loss amount tiers.
        
        - Loss ≤ 2000: Fixed 500 CNY
        - 2000 < Loss ≤ 10000: 10% of loss
        - Loss > 10000: 15% of loss
        
        Args:
            loss_amount: Total loss amount
            
        Returns:
            Deductible amount
        """
        # BUG: Should be loss_amount <= 2000, not loss_amount < 2000
        if loss_amount <= 2000:
            return 500.0
        elif loss_amount <= 10000:
            return loss_amount * 0.10
        else:
            return loss_amount * 0.15
    
    def _apply_driving_bonus(self, amount: float, driving_years: int) -> float:
        """
        Apply driving experience bonus to the payout amount.
        
        Args:
            amount: Current payout amount
            driving_years: Years of driving experience
            
        Returns:
            Amount after applying bonus
        """
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
    """
    Convenience function to calculate insurance claim payout.
    
    Args:
        loss_amount: Total loss amount in CNY
        insurance_type: Type of insurance ("comprehensive", "third_party", "compulsory")
        liability_level: Liability level ("full", "primary", "equal", "secondary", "none")
        driving_years: Years of driving experience
        policy_limit: Maximum payout limit
        is_drunk_driving: Whether the driver was drunk
        is_unlicensed: Whether the driver was unlicensed
        
    Returns:
        Final payout amount in CNY
    """
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
