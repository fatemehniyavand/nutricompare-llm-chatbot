from main import build_application
from nutricompare.application.dto.chat_request import ChatRequest
from nutricompare.application.dto.evaluation_request import EvaluationRequest


def main():
    container = build_application()

    ask_question_use_case = container["ask_question_use_case"]
    compare_answers_use_case = container["compare_answers_use_case"]

    print("NutriCompare AI CLI")
    print("Type 'exit' to quit.")

    while True:
        user_question = input("\nAsk a nutrition question: ").strip()

        if user_question.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        if not user_question:
            print("Please enter a question.")
            continue

        chat_response = ask_question_use_case.execute(
            ChatRequest(user_question=user_question)
        )

        result = chat_response.result

        if result.model_a_response.provider == "internal":
            print("\n================ INPUT GUARD ================")
            print(result.model_a_response.answer)
            continue

        print("\n================ MODEL A ================")
        print(
            f"{result.model_a_response.provider} / "
            f"{result.model_a_response.model_name}"
        )
        print(result.model_a_response.answer)

        print("\n================ MODEL B ================")
        print(
            f"{result.model_b_response.provider} / "
            f"{result.model_b_response.model_name}"
        )
        print(result.model_b_response.answer)

        print("\n================ JUDGE EVALUATION ================")

        evaluation_response = compare_answers_use_case.execute(
            EvaluationRequest(
                user_question=result.user_question,
                model_a_answer=result.model_a_response.answer,
                model_b_answer=result.model_b_response.answer,
            )
        )

        evaluation = evaluation_response.result

        print(f"Winner: {evaluation.winner}")
        print(f"Model A Score: {evaluation.model_a_score}")
        print(f"Model B Score: {evaluation.model_b_score}")
        print(f"Explanation: {evaluation.explanation}")


if __name__ == "__main__":
    main()
