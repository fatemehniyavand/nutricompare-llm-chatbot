from nutricompare.application.services.calorie_extractor import CalorieExtractor


def main() -> None:
    extractor = CalorieExtractor()

    examples = [
        "Total estimated calories: 270 calories",
        "Total estimated calories: 140 + 130 = 270 calories",
        "Total calorie count is approximately 275 calories.",
        "2 eggs are 140 calories and rice is 130 calories. Total calories: 270.",
    ]

    for example in examples:
        print("=" * 60)
        print(example)
        print("Extracted:", extractor.extract_total_calories(example))


if __name__ == "__main__":
    main()
