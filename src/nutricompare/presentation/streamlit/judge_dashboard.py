from pathlib import Path
import pandas as pd
import streamlit as st

from nutricompare.application.analytics.judge_leaderboard import JudgeLeaderboard


st.set_page_config(
    page_title="NutriCompare AI Judge Dashboard",
    page_icon="🥗",
    layout="wide",
)


def get_most_common_winner(wins: dict) -> str:
    if not wins:
        return "N/A"
    return max(wins.items(), key=lambda item: item[1])[0]


def main():
    st.title("🥗 NutriCompare AI Judge Dashboard")
    st.caption(
        "Multi-LLM nutrition answer comparison with judge scorecards, "
        "confidence analytics, and model performance tracking."
    )

    csv_path = Path("logs/judge_reports/judge_reports.csv")

    if not csv_path.exists():
        st.warning("No judge report CSV found yet. Run a few comparisons first.")
        st.stop()

    df = pd.read_csv(csv_path)
    leaderboard = JudgeLeaderboard(str(csv_path)).build()

    most_common_winner = get_most_common_winner(leaderboard.wins)

    st.subheader("📊 System Analytics")

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

        col_wins, col_table = st.columns([2, 1])

        with col_wins:
            st.bar_chart(win_df.set_index("Model")["Wins"])

        with col_table:
            st.dataframe(win_df, use_container_width=True, hide_index=True)
    else:
        st.info("No winner data available yet.")

    st.subheader("📈 Model Win Rate")

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

    if "confidence" in df.columns and "created_at" in df.columns:
        confidence_df = df[["created_at", "confidence"]].copy()
        confidence_df["confidence"] = pd.to_numeric(
            confidence_df["confidence"],
            errors="coerce",
        )
        confidence_df = confidence_df.dropna()

        if not confidence_df.empty:
            st.line_chart(confidence_df.set_index("created_at"))
        else:
            st.info("No numeric confidence values available yet.")
    else:
        st.info("No confidence column found.")

    st.divider()

    st.subheader("🧾 Recent Judge Reports")

    if "created_at" in df.columns:
        sorted_df = df.sort_values("created_at", ascending=False)
    else:
        sorted_df = df

    st.dataframe(
        sorted_df,
        use_container_width=True,
    )

    st.divider()

    st.subheader("🔍 Latest Judge Reasoning")

    latest = sorted_df.iloc[0]

    st.write(f"**Question:** {latest.get('question', '')}")
    st.write(f"**Winner:** {latest.get('winner', '')}")
    st.write(f"**Confidence:** {latest.get('confidence', '')}%")
    st.info(latest.get("judge_reasoning", ""))

    st.divider()

    st.subheader("⬇️ Export Evaluation Data")

    csv_bytes = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Judge Reports CSV",
        data=csv_bytes,
        file_name="nutricompare_judge_reports.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()
