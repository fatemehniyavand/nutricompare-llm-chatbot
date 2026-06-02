from dataclasses import dataclass
from pathlib import Path
import csv
from difflib import SequenceMatcher


@dataclass
class SimilarQuestionResult:
    found: bool
    similarity: float
    previous_question: str
    previous_winner: str
    previous_confidence: str
    previous_reasoning: str


class QuestionHistoryService:
    """
    Detects whether the user has already asked a similar question before.
    """

    def __init__(
        self,
        csv_path: str = "logs/judge_reports/judge_reports.csv",
        threshold: float = 0.8,
    ):
        self.csv_path = Path(csv_path)
        self.threshold = threshold

    def find_similar_question(self, user_question: str) -> SimilarQuestionResult:
        if not self.csv_path.exists():
            return self._empty()

        normalized_input = self._normalize(user_question)
        best_match = self._empty()

        with open(self.csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                previous_question = row.get("question", "")
                normalized_previous = self._normalize(previous_question)

                if not normalized_previous:
                    continue

                similarity = SequenceMatcher(
                    None,
                    normalized_input,
                    normalized_previous,
                ).ratio()

                if similarity >= self.threshold and similarity > best_match.similarity:
                    best_match = SimilarQuestionResult(
                        found=True,
                        similarity=round(similarity * 100, 2),
                        previous_question=previous_question,
                        previous_winner=row.get("winner", "N/A"),
                        previous_confidence=row.get("confidence", "N/A"),
                        previous_reasoning=row.get("judge_reasoning", "N/A"),
                    )

        return best_match

    def _normalize(self, text: str) -> str:
        return " ".join(text.lower().strip().split())

    def _empty(self) -> SimilarQuestionResult:
        return SimilarQuestionResult(
            found=False,
            similarity=0.0,
            previous_question="",
            previous_winner="",
            previous_confidence="",
            previous_reasoning="",
        )
