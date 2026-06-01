from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json
import csv


@dataclass
class ModelScore:
    model_name: str
    answer: str
    correctness: float
    safety: float
    clarity: float
    completeness: float

    @property
    def average_score(self) -> float:
        return round(
            (self.correctness + self.safety + self.clarity + self.completeness) / 4,
            2
        )


@dataclass
class JudgeReport:
    question: str
    model_a: ModelScore
    model_b: ModelScore
    winner: str
    confidence: float
    judge_reasoning: str
    created_at: str


class JudgeReportExporter:
    def __init__(self, output_dir: str = "logs/judge_reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_json(self, report: JudgeReport) -> str:
        filename = self._filename("json")
        path = self.output_dir / filename

        data = asdict(report)
        data["model_a"]["average_score"] = report.model_a.average_score
        data["model_b"]["average_score"] = report.model_b.average_score

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return str(path)

    def save_csv(self, report: JudgeReport) -> str:
        filename = "judge_reports.csv"
        path = self.output_dir / filename
        file_exists = path.exists()

        with open(path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow([
                    "created_at",
                    "question",
                    "model_a",
                    "model_a_score",
                    "model_b",
                    "model_b_score",
                    "winner",
                    "confidence",
                    "judge_reasoning"
                ])

            writer.writerow([
                report.created_at,
                report.question,
                report.model_a.model_name,
                report.model_a.average_score,
                report.model_b.model_name,
                report.model_b.average_score,
                report.winner,
                report.confidence,
                report.judge_reasoning
            ])

        return str(path)

    def save_markdown(self, report: JudgeReport) -> str:
        filename = self._filename("md")
        path = self.output_dir / filename

        content = f"""# NutriCompare AI Judge Report

## User Question

{report.question}

---

## Model A: {report.model_a.model_name}

**Answer:**

{report.model_a.answer}

### Scorecard

| Criterion | Score |
|---|---:|
| Correctness | {report.model_a.correctness} |
| Safety | {report.model_a.safety} |
| Clarity | {report.model_a.clarity} |
| Completeness | {report.model_a.completeness} |
| Average | {report.model_a.average_score} |

---

## Model B: {report.model_b.model_name}

**Answer:**

{report.model_b.answer}

### Scorecard

| Criterion | Score |
|---|---:|
| Correctness | {report.model_b.correctness} |
| Safety | {report.model_b.safety} |
| Clarity | {report.model_b.clarity} |
| Completeness | {report.model_b.completeness} |
| Average | {report.model_b.average_score} |

---

## Final Judge Decision

**Winner:** {report.winner}

**Confidence:** {report.confidence}%

**Reasoning:**

{report.judge_reasoning}

---

Generated at: {report.created_at}
"""

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return str(path)

    def export_all(self, report: JudgeReport) -> dict:
        return {
            "json": self.save_json(report),
            "csv": self.save_csv(report),
            "markdown": self.save_markdown(report),
        }

    def _filename(self, extension: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"judge_report_{timestamp}.{extension}"
