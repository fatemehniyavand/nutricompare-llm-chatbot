from dataclasses import dataclass
from pathlib import Path
import csv
from collections import Counter, defaultdict


@dataclass
class LeaderboardResult:
    total_comparisons: int
    wins: dict
    win_rates: dict
    average_confidence: float
    average_scores: dict


class JudgeLeaderboard:
    def __init__(self, csv_path: str = "logs/judge_reports/judge_reports.csv"):
        self.csv_path = Path(csv_path)

    def build(self) -> LeaderboardResult:
        if not self.csv_path.exists():
            return LeaderboardResult(
                total_comparisons=0,
                wins={},
                win_rates={},
                average_confidence=0.0,
                average_scores={},
            )

        wins = Counter()
        scores = defaultdict(list)
        confidences = []
        total = 0

        with open(self.csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                total += 1

                winner = row.get("winner", "").strip()
                if winner:
                    wins[winner] += 1

                confidence = self._to_float(row.get("confidence"))
                if confidence is not None:
                    confidences.append(confidence)

                model_a = row.get("model_a", "").strip()
                model_b = row.get("model_b", "").strip()

                model_a_score = self._to_float(row.get("model_a_score"))
                model_b_score = self._to_float(row.get("model_b_score"))

                if model_a and model_a_score is not None:
                    scores[model_a].append(model_a_score)

                if model_b and model_b_score is not None:
                    scores[model_b].append(model_b_score)

        win_rates = {
            model: round((count / total) * 100, 2)
            for model, count in wins.items()
        } if total else {}

        average_scores = {
            model: round(sum(values) / len(values), 2)
            for model, values in scores.items()
            if values
        }

        average_confidence = (
            round(sum(confidences) / len(confidences), 2)
            if confidences else 0.0
        )

        return LeaderboardResult(
            total_comparisons=total,
            wins=dict(wins),
            win_rates=win_rates,
            average_confidence=average_confidence,
            average_scores=average_scores,
        )

    def print_summary(self) -> None:
        result = self.build()

        print("\nNutriCompare AI Judge Leaderboard")
        print("=" * 40)
        print(f"Total comparisons: {result.total_comparisons}")
        print(f"Average judge confidence: {result.average_confidence}%")

        print("\nWins:")
        for model, count in result.wins.items():
            rate = result.win_rates.get(model, 0)
            print(f"- {model}: {count} wins ({rate}%)")

        print("\nAverage model scores:")
        for model, score in result.average_scores.items():
            print(f"- {model}: {score}/10")

    @staticmethod
    def _to_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
