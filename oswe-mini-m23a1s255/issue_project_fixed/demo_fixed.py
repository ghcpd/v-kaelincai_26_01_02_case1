"""Demo for the fixed insurance claim calculator"""
from src.insurance_claim import calculate_claim

if __name__ == "__main__":
    examples = [
        dict(loss_amount=2000, insurance_type="comprehensive", liability_level="full", driving_years=5, policy_limit=50000),
        dict(loss_amount=5000, insurance_type="comprehensive", liability_level="full", driving_years=3, policy_limit=50000),
        dict(loss_amount=15000, insurance_type="third_party", liability_level="primary", driving_years=7, policy_limit=20000),
    ]

    for req in examples:
        payout = calculate_claim(**req)
        print(f"Request={req} -> Payout={payout} CNY")
