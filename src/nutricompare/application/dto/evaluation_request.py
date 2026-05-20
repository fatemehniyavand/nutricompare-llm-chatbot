from pydantic import BaseModel


class EvaluationRequest(BaseModel):
    """
    Request DTO for evaluating two model answers.
    """

    user_question: str
    model_a_answer: str
    model_b_answer: str
