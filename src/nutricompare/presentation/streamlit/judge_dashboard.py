from pathlib import Path
import pandas as pd
import streamlit as st

from nutricompare.application.analytics.judge_leaderboard import JudgeLeaderboard


st.set_page_config(
    page_title="NutriCompare AI Judge Dashboard",
    page_icon="🥗",
    layout="wide",
)

st.title("🥗 NutriCompare AI Judge Dashboard")
st.caption("Multi-LLM nutrition answer comparison with judge scorecards and confidence analytics.")

csv_path = Path("logs/judge_reports/judge_reports.csv")

if not csv_path.exists():
    st.warning("No judge report CSV found yet. Run a few comparisons first.")
    st.stop()

df = pd.read_csv(csv_path)
leaderboard = JudgeLeaderboard(str(csv_path)).build()

col1, col2, col3 = st.columns(3)

col1.metric("Total Comparisons", leaderboard.total_comparisons)
col2.metric("Average Confidence", f"{leaderboard.average_confidence}%")
col3.metric("Models Compared", len(leaderboard.average_scores))

st.divider()

st.subheader("🏆 Model Win Rate")

if leaderboard.win_rates:
    win_rate_df = pd.DataFrame(
        {
            "Model": list(leaderboard.win_rates.keys()),
            "Win Rate (%)": list(leaderboard.win_rates.values()),
        }
    )
    st.bar_chart(win_rate_df.set_index("Model"))
else:
    st.info("No winner data available yet.")

st.subheader("📊 Average Model Scores")

if leaderboard.average_scores:
    score_df = pd.DataFrame(
        {
            "Model": list(leaderboard.average_scores.keys()),
            "Average Score": list(leaderboard.average_scores.values()),
        }
    )
    st.bar_chart(score_df.set_index("Model"))
else:
    st.info("No score data available yet.")

st.subheader("🎯 Judge Confidence Over Time")

if "confidence" in df.columns:
    confidence_df = df[["created_at", "confidence"]].copy()
    confidence_df["confidence"] = pd.to_numeric(confidence_df["confidence"], errors="coerce")
    confidence_df = confidence_df.dropna()
    st.line_chart(confidence_df.set_index("created_at"))
else:
    st.info("No confidence column found.")

st.divider()

st.subheader("🧾 Recent Judge Reports")

st.dataframe(
    df.sort_values("created_at", ascending=False),
    use_container_width=True,
)

st.divider()

st.subheader("🔍 Latest Judge Reasoning")

latest = df.sort_values("created_at", ascending=False).iloc[0]

st.write(f"**Question:** {latest.get('question', '')}")
st.write(f"**Winner:** {latest.get('winner', '')}")
st.write(f"**Confidence:** {latest.get('confidence', '')}%")
st.write(f"**Reasoning:** {latest.get('judge_reasoning', '')}")
