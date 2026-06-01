from pydantic import BaseModel


class EvaluationResult(BaseModel):
    """
    Structured result produced by the LLM judge.
    """

    winner: str
    model_a_score: float
    model_b_score: float

    model_a_correctness: float = 0.0
    model_b_correctness: float = 0.0

    model_a_safety: float = 0.0
    model_b_safety: float = 0.0

    model_a_clarity: float = 0.0
    model_b_clarity: float = 0.0

    model_a_completeness: float = 0.0
    model_b_completeness: float = 0.0

    explanation: str
    raw_evaluation: str
