from nutricompare.application.dto.evaluation_request import EvaluationRequest
from nutricompare.application.dto.evaluation_response import EvaluationResponse
from nutricompare.application.services.evaluation_service import (
    EvaluationService,
)


class CompareLLMAnswersUseCase:
    """
    Use case for evaluating and comparing LLM answers.
    """

    def __init__(
        self,
        evaluation_service: EvaluationService,
    ):
        self.evaluation_service = evaluation_service

    def execute(
        self,
        request: EvaluationRequest,
    ) -> EvaluationResponse:
        result = self.evaluation_service.evaluate(
            user_question=request.user_question,
            model_a_answer=request.model_a_answer,
            model_b_answer=request.model_b_answer,
        )

        return EvaluationResponse(
            result=result,
        )
