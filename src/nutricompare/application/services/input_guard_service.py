from nutricompare.application.dto.guard_result import GuardResult
from nutricompare.domain.services.nutrition_intent_classifier import (
    NutritionIntentClassifier,
)


class InputGuardService:
    """
    Validates whether a user query belongs to the nutrition domain.
    """

    def check(self, user_question: str) -> GuardResult:
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
