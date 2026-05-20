from nutricompare.application.services.chat_service import ChatService
from nutricompare.application.services.evaluation_service import (
    EvaluationService,
)
from nutricompare.application.services.input_guard_service import (
    InputGuardService,
)
from nutricompare.application.use_cases.ask_nutrition_question import (
    AskNutritionQuestionUseCase,
)
from nutricompare.application.use_cases.compare_llm_answers import (
    CompareLLMAnswersUseCase,
)
from nutricompare.application.use_cases.run_batch_evaluation import (
    RunBatchEvaluationUseCase,
)
from nutricompare.infrastructure.config.settings import get_settings
from nutricompare.infrastructure.llm.llm_factory import LLMFactory
from nutricompare.infrastructure.logging.logger import app_logger


def build_application():
    """
    Build and wire the application dependencies.
    """

    settings = get_settings()

    app_logger.info("Loading application settings...")

    llm_factory = LLMFactory(settings)

    app_logger.info("Creating model clients...")

    model_a_client = llm_factory.create_model_a()
    model_b_client = llm_factory.create_model_b()
    judge_client = llm_factory.create_judge_model()

    app_logger.info("Creating services...")

    input_guard_service = InputGuardService()

    chat_service = ChatService(
        model_a_client=model_a_client,
        model_b_client=model_b_client,
        settings=settings,
        input_guard_service=input_guard_service,
    )

    evaluation_service = EvaluationService(
        judge_client=judge_client,
        settings=settings,
    )

    app_logger.info("Creating use cases...")

    ask_question_use_case = AskNutritionQuestionUseCase(
        chat_service=chat_service,
    )

    compare_answers_use_case = CompareLLMAnswersUseCase(
        evaluation_service=evaluation_service,
    )

    batch_evaluation_use_case = RunBatchEvaluationUseCase(
        ask_question_use_case=ask_question_use_case,
        compare_answers_use_case=compare_answers_use_case,
    )

    app_logger.info("Application successfully initialized.")

    return {
        "settings": settings,
        "ask_question_use_case": ask_question_use_case,
        "compare_answers_use_case": compare_answers_use_case,
        "batch_evaluation_use_case": batch_evaluation_use_case,
        "input_guard_service": input_guard_service,
    }


if __name__ == "__main__":
    container = build_application()

    app_logger.info("NutriCompare AI is ready.")
