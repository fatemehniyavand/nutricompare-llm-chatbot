import re


class NutritionIntentClassifier:
    """
    Classifies user input for a nutrition-only assistant.
    """

    UNSAFE_KEYWORDS = {
        "starve",
        "starvation",
        "eat nothing",
        "stop eating",
        "500 calories",
        "400 calories",
        "300 calories",
        "anorexia",
        "bulimia",
        "purge",
        "laxative",
        "extreme diet",
        "lose weight fast",
        "crash diet",
    }

    CALORIE_KEYWORDS = {
        "calorie",
        "calories",
        "kcal",
        "how many calories",
        "estimate calories",
        "calorie estimate",
    }

    NUTRITION_KEYWORDS = {
        "nutrition",
        "nutrient",
        "protein",
        "carb",
        "carbs",
        "carbohydrate",
        "fat",
        "fiber",
        "vitamin",
        "mineral",
        "diet",
        "meal",
        "food",
        "healthy",
        "breakfast",
        "lunch",
        "dinner",
        "snack",
        "weight loss",
        "muscle gain",
        "gym",
        "bodybuilding",
        "egg",
        "eggs",
        "rice",
        "chicken",
        "beef",
        "fish",
        "milk",
        "banana",
        "apple",
        "bread",
        "pasta",
        "salad",
        "vegetable",
        "fruit",
        "yogurt",
        "cheese",
        "potato",
        "oats",
        "beans",
        "lentils",
        "sugar",
        "salt",
        "water",
    }

    @classmethod
    def classify(cls, text: str) -> str:
        normalized = text.lower().strip()

        if not normalized:
            return "empty"

        if cls._contains_any(normalized, cls.UNSAFE_KEYWORDS):
            return "unsafe"

        if cls._looks_like_calorie_estimation(normalized):
            return "calorie_estimation"

        if cls._contains_any(normalized, cls.NUTRITION_KEYWORDS):
            return "nutrition_qa"

        return "out_of_domain"

    @classmethod
    def _contains_any(cls, text: str, keywords: set[str]) -> bool:
        return any(keyword in text for keyword in keywords)

    @classmethod
    def _looks_like_calorie_estimation(cls, text: str) -> bool:
        has_calorie_keyword = cls._contains_any(text, cls.CALORIE_KEYWORDS)

        has_quantity = bool(
            re.search(
                r"\b\d+(\.\d+)?\s*(g|gram|grams|kg|ml|cup|cups|egg|eggs|slice|slices)\b",
                text,
            )
        )

        has_food = cls._contains_any(text, cls.NUTRITION_KEYWORDS)

        return has_calorie_keyword or (has_quantity and has_food)
