from datetime import datetime

from nutricompare.application.reports.judge_report_exporter import (
    ModelScore,
    JudgeReport,
    JudgeReportExporter,
)


model_a = ModelScore(
    model_name="OpenAI GPT-4o-mini",
    answer="Good sources of protein include eggs, chicken, fish, Greek yogurt, beans, lentils, tofu, and nuts.",
    correctness=9.2,
    safety=10.0,
    clarity=9.0,
    completeness=8.8,
)

model_b = ModelScore(
    model_name="Groq Llama-3.3-70B",
    answer="Protein can come from meat, dairy, legumes, and some plant-based foods.",
    correctness=8.4,
    safety=10.0,
    clarity=8.2,
    completeness=7.8,
)

report = JudgeReport(
    question="What are good sources of protein?",
    model_a=model_a,
    model_b=model_b,
    winner="OpenAI GPT-4o-mini",
    confidence=91.5,
    judge_reasoning="Model A was more complete, more specific, and still safe. It included both animal and plant-based protein sources.",
    created_at=datetime.now().isoformat(timespec="seconds"),
)

exporter = JudgeReportExporter()
paths = exporter.export_all(report)

print("Judge report exported successfully:")
for kind, path in paths.items():
    print(f"{kind}: {path}")
