from pydantic import BaseModel

from nutricompare.domain.entities.evaluation_result import EvaluationResult


class EvaluationResponse(BaseModel):
    """
    Response DTO for judge model evaluation.
    """

    result: EvaluationResult
