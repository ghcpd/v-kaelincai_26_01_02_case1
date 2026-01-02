"""Demo for fixed Insurance Claim Calculator"""
from src.insurance_claim import calculate_claim


def demo():
    examples = [
        {"loss_amount": 2000, "driving_years": 5, "expected": 1320.0},
        {"loss_amount": 10000, "driving_years": 10, "expected": 8280.0},
        {"loss_amount": 5000, "driving_years": 3, "expected": 3780.0},
    ]

    for ex in examples:
        payout = calculate_claim(
            loss_amount=ex["loss_amount"],
            insurance_type="comprehensive",
            liability_level="full",
            driving_years=ex["driving_years"],
            policy_limit=50000
        )
        print(f"Loss: {ex['loss_amount']}, Years: {ex['driving_years']} -> Payout: {payout} (expected {ex['expected']})")


if __name__ == "__main__":
    demo()
