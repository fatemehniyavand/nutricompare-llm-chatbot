from nutricompare.application.dto.chat_request import ChatRequest
from nutricompare.application.dto.chat_response import ChatResponse
from nutricompare.application.services.chat_service import ChatService


class AskNutritionQuestionUseCase:
    """
    Use case for asking nutrition questions to multiple LLMs.
    """

    def __init__(
        self,
        chat_service: ChatService,
    ):
        self.chat_service = chat_service

    def execute(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        result = self.chat_service.ask_question(
            user_question=request.user_question,
        )

        return ChatResponse(
            result=result,
        )
