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
    ):
        self.model_a_client = model_a_client
        self.model_b_client = model_b_client
        self.settings = settings
        self.input_guard_service = input_guard_service

    def ask_question(self, user_question: str) -> NutritionAnswer:
        """
        Validate input, then ask both models the same nutrition question.
        """

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

            return NutritionAnswer(
                user_question=user_question,
                model_a_response=model_a_response,
                model_b_response=model_b_response,
            )

        enriched_prompt = f"""
User intent: {guard_result.intent}

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

        return NutritionAnswer(
            user_question=user_question,
            model_a_response=model_a_response,
            model_b_response=model_b_response,
        )
