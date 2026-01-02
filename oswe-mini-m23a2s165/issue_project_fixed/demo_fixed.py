"""Demo for the fixed Insurance Claim Calculator."""
from src.insurance_claim import calculate_claim


def main():
    examples = [
        (2000, "comprehensive", "full", 5, 50000),
        (5000, "comprehensive", "full", 3, 50000),
        (10000, "comprehensive", "full", 10, 50000),
        (1000, "compulsory", "secondary", 1, 50000),
    ]

    for loss, itype, liability, years, limit in examples:
        payout = calculate_claim(loss, itype, liability, years, limit)
        print(f"loss={loss}, type={itype}, liability={liability}, years={years} -> payout={payout}")


if __name__ == "__main__":
    main()