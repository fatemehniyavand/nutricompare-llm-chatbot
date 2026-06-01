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
        "skip all meals",
        "without food",
        "no food",
        "water only",
        "only water",
        "coffee only",
        "water and coffee only",
        "drink water for a week",
        "100 calorie diet",
        "200 calorie diet",
        "300 calories",
        "400 calories",
        "500 calories",
        "0 calories",
        "zero calories",
        "anorexia",
        "bulimia",
        "purge",
        "throw up",
        "make myself vomit",
        "vomit after eating",
        "laxative",
        "extreme diet",
        "lose weight fast",
        "lose 10kg",
        "lose 15kg",
        "lose 20kg",
        "lose 10 kg",
        "lose 15 kg",
        "lose 20 kg",
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
        "steak",
        "fish",
        "salmon",
        "tuna",
        "tofu",
        "avocado",
        "almond",
        "almonds",
        "peanut",
        "peanut butter",
        "cucumber",
        "carrot",
        "carrots",
        "broccoli",
        "tomato",
        "sauce",
        "milk",
        "banana",
        "apple",
        "orange",
        "bread",
        "butter",
        "pasta",
        "salad",
        "vegetable",
        "vegetables",
        "fruit",
        "fruits",
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
