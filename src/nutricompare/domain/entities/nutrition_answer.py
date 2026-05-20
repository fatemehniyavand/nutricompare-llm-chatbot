from pydantic import BaseModel

from nutricompare.domain.entities.evaluation_result import EvaluationResult
from nutricompare.domain.entities.model_response import ModelResponse


class NutritionAnswer(BaseModel):
    """
    Full response returned by the multi-LLM nutrition assistant.
    """

    user_question: str
    model_a_response: ModelResponse
    model_b_response: ModelResponse
    evaluation: EvaluationResult | None = None
