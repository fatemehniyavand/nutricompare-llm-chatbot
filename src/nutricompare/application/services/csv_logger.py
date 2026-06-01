import csv
from datetime import datetime
from pathlib import Path
from typing import Optional


class CSVLogger:
    """
    Logs chatbot interactions into a CSV file.
    """

    def __init__(self, file_path: str = "storage/interactions.csv") -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_file_exists()

    def log(
        self,
        user_input: str,
        intent: str,
        openai_answer: Optional[str],
        groq_answer: Optional[str],
        judge_winner: Optional[str],
        total_calories: Optional[float],
        confidence: str,
    ) -> None:
        with self.file_path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self._fieldnames())
            writer.writerow(
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "user_input": user_input,
                    "intent": intent,
                    "openai_answer": openai_answer,
                    "groq_answer": groq_answer,
                    "judge_winner": judge_winner,
                    "total_calories": total_calories,
                    "confidence": confidence,
                }
            )

    def _ensure_file_exists(self) -> None:
        if not self.file_path.exists():
            with self.file_path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self._fieldnames())
                writer.writeheader()

    def _fieldnames(self) -> list[str]:
        return [
            "timestamp",
            "user_input",
            "intent",
            "openai_answer",
            "groq_answer",
            "judge_winner",
            "total_calories",
            "confidence",
        ]
