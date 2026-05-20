from pydantic import BaseModel, Field


class ModelScore(BaseModel):
    """
    Score assigned to a model by the evaluator.
    """

    value: float = Field(..., ge=0, le=10)
