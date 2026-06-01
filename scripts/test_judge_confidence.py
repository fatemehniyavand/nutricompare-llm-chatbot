from nutricompare.application.services.judge_confidence_service import (
    JudgeConfidenceService,
)


def main() -> None:
    service = JudgeConfidenceService()

    examples = [
        ("model_b", 8.0, 9.0),
        ("model_a", 9.5, 7.0),
        ("tie", 8.0, 8.0),
        ("model_a", 7.5, 7.0),
    ]

    for winner, model_a_score, model_b_score in examples:
        confidence = service.calculate(
            winner=winner,
            model_a_score=model_a_score,
            model_b_score=model_b_score,
        )

        print("=" * 60)
        print(f"Winner: {winner}")
        print(f"Model A Score: {model_a_score}")
        print(f"Model B Score: {model_b_score}")
        print(f"Confidence: {confidence}")


if __name__ == "__main__":
    main()
