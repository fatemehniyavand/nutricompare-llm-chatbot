import streamlit as st

from main import build_application
from nutricompare.application.dto.chat_request import ChatRequest
from nutricompare.application.dto.evaluation_request import EvaluationRequest
from nutricompare.application.services.judge_confidence_service import JudgeConfidenceService


st.set_page_config(
    page_title="NutriCompare AI",
    page_icon="🥗",
    layout="wide",
)


@st.cache_resource
def get_container():
    return build_application()


def get_final_answer(winner, model_a_answer, model_b_answer):
    if winner == "model_a":
        return model_a_answer

    if winner == "model_b":
        return model_b_answer

    return model_a_answer


def main():
    container = get_container()

    ask_question_use_case = container["ask_question_use_case"]
    compare_answers_use_case = container["compare_answers_use_case"]
    meal_tracking_service = container["meal_tracking_service"]
    judge_confidence_service = JudgeConfidenceService()

    st.title("🥗 NutriCompare AI")
    st.caption("A Multi-LLM Nutrition Assistant with Judge-Based Answer Selection")

    with st.sidebar:
        st.header("System Flow")
        st.markdown(
            """
            **User Input**  
            ↓  
            **Nutrition Guard**  
            ↓  
            **Model A + Model B**  
            ↓  
            **LLM Judge**  
            ↓  
            **Final Selected Answer**  
            ↓  
            **Meal Memory**
            """
        )

        st.divider()

        st.subheader("Meal Memory")
        if st.button("Show today's summary"):
            st.session_state["today_summary"] = meal_tracking_service.get_today_summary()

        if st.button("Clear meal memory"):
            st.session_state["today_summary"] = meal_tracking_service.clear_memory()

        if "today_summary" in st.session_state:
            st.text(st.session_state["today_summary"])

    st.subheader("Try an example")

    example = st.selectbox(
        "Choose a sample nutrition question",
        [
            "",
            "2 eggs and 100g rice",
            "How many calories are in 100g chicken breast?",
            "What are good sources of protein?",
            "Give me a safe weight-loss meal idea",
            "I want to eat only 300 calories per day",
        ],
    )

    user_question = st.text_area(
        "Ask a nutrition question",
        value=example,
        placeholder="Example: 2 eggs and 100g rice",
        height=120,
    )

    submit = st.button("Compare answers", type="primary")

    if submit:
        if not user_question.strip():
            st.warning("Please enter a nutrition-related question.")
            return

        with st.spinner("Asking the models..."):
            chat_response = ask_question_use_case.execute(
                ChatRequest(user_question=user_question.strip())
            )

        result = chat_response.result

        if result.model_a_response.provider == "internal":
            st.warning(result.model_a_response.answer)
            return

        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader("Model A")
            st.caption(
                f"{result.model_a_response.provider} / "
                f"{result.model_a_response.model_name}"
            )
            st.markdown(result.model_a_response.answer)

        with col_b:
            st.subheader("Model B")
            st.caption(
                f"{result.model_b_response.provider} / "
                f"{result.model_b_response.model_name}"
            )
            st.markdown(result.model_b_response.answer)

        with st.spinner("Judging the answers..."):
            evaluation_response = compare_answers_use_case.execute(
                EvaluationRequest(
                    user_question=result.user_question,
                    model_a_answer=result.model_a_response.answer,
                    model_b_answer=result.model_b_response.answer,
                )
            )

        evaluation = evaluation_response.result

        judge_confidence = judge_confidence_service.calculate(
            winner=evaluation.winner,
            model_a_score=evaluation.model_a_score,
            model_b_score=evaluation.model_b_score,
        )

        st.divider()
        st.subheader("Judge Evaluation")

        metric_col_1, metric_col_2, metric_col_3, metric_col_4 = st.columns(4)

        with metric_col_1:
            st.metric("Winner", evaluation.winner)

        with metric_col_2:
            st.metric("Model A Score", evaluation.model_a_score)

        with metric_col_3:
            st.metric("Model B Score", evaluation.model_b_score)

        with metric_col_4:
            st.metric("Confidence", judge_confidence.upper())

        st.info(evaluation.explanation)

        final_answer = get_final_answer(
            winner=evaluation.winner,
            model_a_answer=result.model_a_response.answer,
            model_b_answer=result.model_b_response.answer,
        )

        st.divider()
        st.subheader("Final Selected Answer")
        st.success(final_answer)

        st.divider()
        st.subheader("Today Summary")
        st.text(meal_tracking_service.get_today_summary())


if __name__ == "__main__":
    main()
