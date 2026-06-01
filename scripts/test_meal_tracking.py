from src.application.services.meal_tracking_service import MealTrackingService


def main() -> None:
    service = MealTrackingService()

    examples = [
        ("2 eggs and 100g rice", 286),
        ("apple 200g", 104),
        ("100g chicken and 50g rice", 230),
    ]

    for user_input, calories in examples:
        meal = service.process_meal_input(
            user_input=user_input,
            total_calories=calories,
        )

        print("=" * 60)
        print(f"Input: {meal.user_input}")
        print(f"Confidence: {meal.confidence}")
        print(f"Total calories: {meal.total_calories}")

        for food in meal.foods:
            print(
                {
                    "name": food.name,
                    "quantity": food.quantity,
                    "unit": food.unit,
                }
            )

    print("=" * 60)
    print(service.get_today_summary())


if __name__ == "__main__":
    main()
