from pathlib import Path
from datetime import datetime

import pandas as pd
import streamlit as st

from main import build_application
from nutricompare.application.analytics.judge_leaderboard import JudgeLeaderboard
from nutricompare.application.dto.chat_request import ChatRequest
from nutricompare.application.dto.evaluation_request import EvaluationRequest
from nutricompare.application.services.judge_confidence_service import JudgeConfidenceService
from nutricompare.application.services.question_history_service import QuestionHistoryService
from nutricompare.application.reports.judge_report_exporter import JudgeReportExporter, JudgeReport, ModelScore


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


def get_display_winner(winner, model_a_name, model_b_name):
    if winner == "model_a":
        return f"🏆 {model_a_name}"

    if winner == "model_b":
        return f"🏆 {model_b_name}"

    return winner


def render_analytics_tab():
    st.subheader("📊 System Analytics")

    csv_path = Path("logs/judge_reports/judge_reports.csv")

    if not csv_path.exists():
        st.info("No analytics available yet. Run a few comparisons first.")
        return

    df = pd.read_csv(csv_path)
    leaderboard = JudgeLeaderboard(str(csv_path)).build()

    most_common_winner = "N/A"
    if leaderboard.wins:
        most_common_winner = max(leaderboard.wins, key=leaderboard.wins.get)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Comparisons", leaderboard.total_comparisons)
    col2.metric("Average Confidence", f"{leaderboard.average_confidence}%")
    col3.metric("Models Compared", len(leaderboard.average_scores))
    col4.metric("Most Common Winner", most_common_winner)

    st.divider()

    st.subheader("🏆 Model Wins")

    if leaderboard.wins:
        win_df = pd.DataFrame(
            {
                "Model": list(leaderboard.wins.keys()),
                "Wins": list(leaderboard.wins.values()),
                "Win Rate (%)": [
                    leaderboard.win_rates.get(model, 0)
                    for model in leaderboard.wins.keys()
                ],
            }
        )

        col_chart, col_table = st.columns([2, 1])

        with col_chart:
            st.bar_chart(win_df.set_index("Model")["Wins"])

        with col_table:
            st.dataframe(win_df, use_container_width=True, hide_index=True)
    else:
        st.info("No winner data available yet.")

    st.subheader("📈 Win Rate")

    if leaderboard.win_rates:
        win_rate_df = pd.DataFrame(
            {
                "Model": list(leaderboard.win_rates.keys()),
                "Win Rate (%)": list(leaderboard.win_rates.values()),
            }
        )

        st.bar_chart(win_rate_df.set_index("Model"))
    else:
        st.info("No win-rate data available yet.")

    st.subheader("📊 Average Model Scores")

    if leaderboard.average_scores:
        score_df = pd.DataFrame(
            {
                "Model": list(leaderboard.average_scores.keys()),
                "Average Score": list(leaderboard.average_scores.values()),
            }
        )

        st.bar_chart(score_df.set_index("Model"))
        st.dataframe(score_df, use_container_width=True, hide_index=True)
    else:
        st.info("No score data available yet.")

    st.subheader("🎯 Judge Confidence Over Time")

    if "created_at" in df.columns and "confidence" in df.columns:
        confidence_df = df[["created_at", "confidence"]].copy()
        confidence_df["confidence"] = pd.to_numeric(
            confidence_df["confidence"],
            errors="coerce",
        )
        confidence_df = confidence_df.dropna()

        if not confidence_df.empty:
            st.line_chart(confidence_df.set_index("created_at"))
        else:
            st.info("No numeric confidence values available.")
    else:
        st.info("No confidence data available.")

    st.divider()

    st.subheader("🧾 Recent Judge Reports")

    if "created_at" in df.columns:
        df = df.sort_values("created_at", ascending=False)

    st.dataframe(df, use_container_width=True)

    st.divider()

    st.subheader("⬇️ Export Data")

    st.download_button(
        label="Download Judge Reports CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="nutricompare_judge_reports.csv",
        mime="text/csv",
    )


def main():
    container = get_container()

    ask_question_use_case = container["ask_question_use_case"]
    compare_answers_use_case = container["compare_answers_use_case"]
    meal_tracking_service = container["meal_tracking_service"]
    judge_confidence_service = JudgeConfidenceService()
    question_history_service = QuestionHistoryService(threshold=0.6)
    judge_report_exporter = JudgeReportExporter()

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
            **Intent Classifier**  
            ↓  
            **Model A + Model B**  
            ↓  
            **LLM Judge**  
            ↓  
            **Confidence Layer**  
            ↓  
            **Final Selected Answer**  
            ↓  
            **Meal Memory + Logs**
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

    tab_chat, tab_analytics = st.tabs(["💬 Chat", "📊 Analytics"])

    with tab_chat:
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

            similar_question = question_history_service.find_similar_question(
                user_question.strip()
            )

            if similar_question.found:
                st.session_state["similar_question_notice"] = similar_question

                st.warning(
                    "⚠️ Similar question found in history "
                    f"({similar_question.similarity}% similarity)."
                )

                with st.expander("View previous similar question", expanded=True):
                    st.write(f"**Previous question:** {similar_question.previous_question}")
                    st.write(f"**Previous winner:** {similar_question.previous_winner}")
                    st.write(f"**Previous confidence:** {similar_question.previous_confidence}")
                    st.write(f"**Previous judge reasoning:** {similar_question.previous_reasoning}")
            else:
                st.session_state.pop("similar_question_notice", None)

            with st.spinner("Asking the models..."):
                chat_response = ask_question_use_case.execute(
                    ChatRequest(user_question=user_question.strip())
                )

            result = chat_response.result

            if result.model_a_response.provider == "internal":
                st.warning(result.model_a_response.answer)
                return

            st.divider()
            st.subheader("Side-by-Side Model Answers")

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

            model_a_display = (
                f"{result.model_a_response.provider} / "
                f"{result.model_a_response.model_name}"
            )

            model_b_display = (
                f"{result.model_b_response.provider} / "
                f"{result.model_b_response.model_name}"
            )

            winner_display = get_display_winner(
                winner=evaluation.winner,
                model_a_name=model_a_display,
                model_b_name=model_b_display,
            )

            st.divider()
            st.subheader("Judge Evaluation")

            metric_col_1, metric_col_2, metric_col_3, metric_col_4 = st.columns(4)

            with metric_col_1:
                st.metric("Winner", winner_display)

            with metric_col_2:
                st.metric("Model A Score", evaluation.model_a_score)

            with metric_col_3:
                st.metric("Model B Score", evaluation.model_b_score)

            with metric_col_4:
                st.metric("Confidence", judge_confidence.upper())

            st.info(evaluation.explanation)

            model_a_report = ModelScore(
                model_name=model_a_display,
                answer=result.model_a_response.answer,
                correctness=evaluation.model_a_correctness,
                safety=evaluation.model_a_safety,
                clarity=evaluation.model_a_clarity,
                completeness=evaluation.model_a_completeness,
            )

            model_b_report = ModelScore(
                model_name=model_b_display,
                answer=result.model_b_response.answer,
                correctness=evaluation.model_b_correctness,
                safety=evaluation.model_b_safety,
                clarity=evaluation.model_b_clarity,
                completeness=evaluation.model_b_completeness,
            )

            judge_report = JudgeReport(
                question=result.user_question,
                model_a=model_a_report,
                model_b=model_b_report,
                winner=winner_display.replace("🏆 ", ""),
                confidence=judge_confidence.upper(),
                judge_reasoning=evaluation.explanation,
                created_at=datetime.now().isoformat(timespec="seconds"),
            )

            exported_paths = judge_report_exporter.export_all(judge_report)

            with st.expander("Saved Judge Report"):
                st.write(exported_paths)

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

    with tab_analytics:
        render_analytics_tab()


if __name__ == "__main__":
    main()
