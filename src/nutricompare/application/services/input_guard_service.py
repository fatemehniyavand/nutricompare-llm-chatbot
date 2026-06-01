from nutricompare.application.dto.guard_result import GuardResult
from nutricompare.domain.services.nutrition_intent_classifier import (
    NutritionIntentClassifier,
)


class InputGuardService:
    """
    Validates whether a user query belongs to the nutrition domain
    and blocks unsafe diet-related requests.
    """

    UNSAFE_PATTERNS = [
        "300 calories per day",
        "only 300 calories",
        "0 calories",
        "zero calories",
        "stop eating",
        "not eat for",
        "without eating",
        "water and coffee only",
        "coffee only",
        "water only",
        "survive on water",
        "lose 20kg",
        "lose 20 kg",
        "lose weight in one week",
        "make myself vomit",
        "vomit after eating",
    ]

    def check(self, user_question: str) -> GuardResult:
        normalized_question = user_question.lower().strip()

        if self._matches_unsafe_pattern(normalized_question):
            return GuardResult(
                is_allowed=False,
                intent="unsafe",
                message=(
                    "I cannot help with extreme dieting or unsafe eating behavior. "
                    "For health, weight, or eating disorder concerns, please speak with a qualified professional."
                ),
            )

        intent = NutritionIntentClassifier.classify(user_question)

        if intent == "empty":
            return GuardResult(
                is_allowed=False,
                intent=intent,
                message="Please enter a nutrition-related question.",
            )

        if intent == "out_of_domain":
            return GuardResult(
                is_allowed=False,
                intent=intent,
                message=(
                    "I can only answer nutrition-related questions, such as calorie "
                    "estimation, meals, diet, nutrients, protein, vitamins, and healthy eating."
                ),
            )

        if intent == "unsafe":
            return GuardResult(
                is_allowed=False,
                intent=intent,
                message=(
                    "I cannot help with extreme dieting or unsafe eating behavior. "
                    "For health, weight, or eating disorder concerns, please speak with a qualified professional."
                ),
            )

        return GuardResult(
            is_allowed=True,
            intent=intent,
            message=None,
        )

    def _matches_unsafe_pattern(self, normalized_question: str) -> bool:
        return any(
            pattern in normalized_question
            for pattern in self.UNSAFE_PATTERNS
        )
