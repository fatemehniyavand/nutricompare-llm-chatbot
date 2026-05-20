from src.application.services.food_parser import FoodParser
from src.application.services.confidence_scorer import ConfidenceScorer


def main() -> None:
    parser = FoodParser()
    scorer = ConfidenceScorer()

    examples = [
        "2 eggs and 100g rice",
        "apple 200g",
        "100g chicken and 50g rice",
        "I ate 2 eggs and 200g potato",
    ]

    for example in examples:
        foods = parser.parse(example)
        confidence = scorer.score(foods)

        print("=" * 60)
        print(f"Input: {example}")
        print(f"Confidence: {confidence}")

        for food in foods:
            print(
                {
                    "name": food.name,
                    "quantity": food.quantity,
                    "unit": food.unit,
                }
            )


if __name__ == "__main__":
    main()
