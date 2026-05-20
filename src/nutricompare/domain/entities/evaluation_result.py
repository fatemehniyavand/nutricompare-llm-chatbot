from pydantic import BaseModel, Field


class EvaluationResult(BaseModel):
    """
    Represents the judge model evaluation result.
    """

    winner: str = Field(..., description="model_a, model_b, or tie")
    model_a_score: float = Field(..., ge=0, le=10)
    model_b_score: float = Field(..., ge=0, le=10)
    explanation: str
    raw_evaluation: str
