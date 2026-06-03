from typing import Optional

from nutricompare.application.services.calorie_extractor import CalorieExtractor
from nutricompare.application.services.csv_logger import CSVLogger
from nutricompare.application.services.meal_command_handler import MealCommandHandler
from nutricompare.application.services.meal_tracking_service import MealTrackingService
from nutricompare.domain.entities.model_response import ModelResponse
from nutricompare.domain.entities.nutrition_answer import NutritionAnswer
from nutricompare.prompts.system_prompts import (
    NUTRITION_ASSISTANT_SYSTEM_PROMPT,
)


class ChatService:
    """
    Main orchestration service for multi-LLM nutrition chat.
    """

    def __init__(
        self,
        model_a_client,
        model_b_client,
        settings,
        input_guard_service,
        meal_tracking_service: Optional[MealTrackingService] = None,
        meal_command_handler: Optional[MealCommandHandler] = None,
        csv_logger: Optional[CSVLogger] = None,
    ):
        self.model_a_client = model_a_client
        self.model_b_client = model_b_client
        self.settings = settings
        self.input_guard_service = input_guard_service
        self.meal_tracking_service = meal_tracking_service or MealTrackingService()
        self.meal_command_handler = meal_command_handler or MealCommandHandler(
            self.meal_tracking_service
        )
        self.csv_logger = csv_logger or CSVLogger()
        self.calorie_extractor = CalorieExtractor()

    def ask_question(self, user_question: str) -> NutritionAnswer:
        """
        Validate input, handle meal-memory commands, ask both models,
        extract calories, save meal memory, and log interaction.
        """

        command_response = self.meal_command_handler.handle(user_question)

        if command_response is not None:
            model_a_response = ModelResponse(
                model_name="meal_memory",
                provider="internal",
                answer=command_response,
            )

            model_b_response = ModelResponse(
                model_name="meal_memory",
                provider="internal",
                answer=command_response,
            )

            self.csv_logger.log(
                user_input=user_question,
                intent="meal_memory_command",
                openai_answer=None,
                groq_answer=None,
                judge_winner=None,
                total_calories=None,
                confidence="system",
            )

            return NutritionAnswer(
                user_question=user_question,
                model_a_response=model_a_response,
                model_b_response=model_b_response,
            )

        guard_result = self.input_guard_service.check(user_question)

        if not guard_result.is_allowed:
            blocked_response = guard_result.message or "This question is not supported."

            model_a_response = ModelResponse(
                model_name="system_guard",
                provider="internal",
                answer=blocked_response,
            )

            model_b_response = ModelResponse(
                model_name="system_guard",
                provider="internal",
                answer=blocked_response,
            )

            self.csv_logger.log(
                user_input=user_question,
                intent=getattr(guard_result, "intent", "blocked"),
                openai_answer=None,
                groq_answer=None,
                judge_winner=None,
                total_calories=None,
                confidence="blocked",
            )

            return NutritionAnswer(
                user_question=user_question,
                model_a_response=model_a_response,
                model_b_response=model_b_response,
            )

        meal_entry = self.meal_tracking_service.process_meal_input(
            user_input=user_question,
            total_calories=None,
        )

        parsed_foods_text = self._format_parsed_foods(meal_entry)

        enriched_prompt = f"""
User intent: {guard_result.intent}

Parsed food items:
{parsed_foods_text}

User question:
{user_question}
"""

        model_a_answer = self.model_a_client.generate(
            system_prompt=NUTRITION_ASSISTANT_SYSTEM_PROMPT,
            user_prompt=enriched_prompt,
            temperature=self.settings.default_temperature,
            max_tokens=self.settings.max_tokens,
        )

        model_b_answer = self.model_b_client.generate(
            system_prompt=NUTRITION_ASSISTANT_SYSTEM_PROMPT,
            user_prompt=enriched_prompt,
            temperature=self.settings.default_temperature,
            max_tokens=self.settings.max_tokens,
        )

        calories_a = self.calorie_extractor.extract_total_calories(
            model_a_answer
        )

        calories_b = self.calorie_extractor.extract_total_calories(
            model_b_answer
        )

        estimated_calories = self._merge_calorie_estimates(
            calories_a=calories_a,
            calories_b=calories_b,
        )

        meal_entry.total_calories = estimated_calories

        model_a_response = ModelResponse(
            model_name=self.settings.model_a_name,
            provider=self.settings.model_a_provider,
            answer=model_a_answer,
        )

        model_b_response = ModelResponse(
            model_name=self.settings.model_b_name,
            provider=self.settings.model_b_provider,
            answer=model_b_answer,
        )

        self.csv_logger.log(
            user_input=user_question,
            intent=guard_result.intent,
            openai_answer=model_a_answer
            if self.settings.model_a_provider.lower() == "openai"
            else model_b_answer,
            groq_answer=model_a_answer
            if self.settings.model_a_provider.lower() == "groq"
            else model_b_answer,
            judge_winner=None,
            total_calories=meal_entry.total_calories,
            confidence=meal_entry.confidence,
        )

        return NutritionAnswer(
            user_question=user_question,
            model_a_response=model_a_response,
            model_b_response=model_b_response,
        )

    def _merge_calorie_estimates(
        self,
        calories_a: Optional[float],
        calories_b: Optional[float],
    ) -> Optional[float]:
        if calories_a is not None and calories_b is not None:
            return round((calories_a + calories_b) / 2, 2)

        if calories_a is not None:
            return calories_a

        if calories_b is not None:
            return calories_b

        return None

    def _format_parsed_foods(self, meal_entry) -> str:
        if not meal_entry.foods:
            return "No structured food items detected."

        lines = []

        for food in meal_entry.foods:
            quantity = food.quantity if food.quantity is not None else "unknown"
            unit = food.unit if food.unit is not None else "unknown"

            lines.append(
                f"- name: {food.name}, quantity: {quantity}, unit: {unit}"
            )

        lines.append(f"Parsing confidence: {meal_entry.confidence}")
        return "\n".join(lines)
