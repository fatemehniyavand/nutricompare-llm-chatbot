from nutricompare.application.dto.chat_request import ChatRequest
from nutricompare.application.dto.evaluation_request import (
    EvaluationRequest,
)


class RunBatchEvaluationUseCase:
    """
    Run evaluation on multiple nutrition questions.
    """

    def __init__(
        self,
        ask_question_use_case,
        compare_answers_use_case,
    ):
        self.ask_question_use_case = ask_question_use_case
        self.compare_answers_use_case = compare_answers_use_case

    def execute(
        self,
        questions: list[str],
    ) -> list[dict]:
        results = []

        for question in questions:
            chat_response = self.ask_question_use_case.execute(
                ChatRequest(
                    user_question=question,
                )
            )

            evaluation_response = self.compare_answers_use_case.execute(
                EvaluationRequest(
                    user_question=question,
                    model_a_answer=chat_response.result.model_a_response.answer,
                    model_b_answer=chat_response.result.model_b_response.answer,
                )
            )

            results.append(
                {
                    "question": question,
                    "model_a_answer": chat_response.result.model_a_response.answer,
                    "model_b_answer": chat_response.result.model_b_response.answer,
                    "evaluation": evaluation_response.result.model_dump(),
                }
            )

        return results
