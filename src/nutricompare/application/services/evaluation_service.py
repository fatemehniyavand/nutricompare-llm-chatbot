import re

from nutricompare.domain.entities.evaluation_result import EvaluationResult
from nutricompare.prompts.evaluation_prompts import (
    LLM_JUDGE_SYSTEM_PROMPT,
)


class EvaluationService:
    """
    Service responsible for evaluating two LLM answers using a structured scorecard.
    """

    def __init__(
        self,
        judge_client,
        settings,
    ):
        self.judge_client = judge_client
        self.settings = settings

    def evaluate(
        self,
        user_question: str,
        model_a_answer: str,
        model_b_answer: str,
    ) -> EvaluationResult:
        prompt = f"""
User Question:
{user_question}

Model A Answer:
{model_a_answer}

Model B Answer:
{model_b_answer}
"""

        raw_evaluation = self.judge_client.generate(
            system_prompt=LLM_JUDGE_SYSTEM_PROMPT,
            user_prompt=prompt,
            temperature=self.settings.judge_temperature,
            max_tokens=self.settings.max_tokens,
        )

        model_a_score = self._extract_score(raw_evaluation, "Model A Score")
        model_b_score = self._extract_score(raw_evaluation, "Model B Score")

        winner = self._normalize_winner(
            winner=self._extract_winner(raw_evaluation),
            model_a_score=model_a_score,
            model_b_score=model_b_score,
        )

        return EvaluationResult(
            winner=winner,
            model_a_score=model_a_score,
            model_b_score=model_b_score,
            model_a_correctness=self._extract_score(raw_evaluation, "Model A Correctness"),
            model_b_correctness=self._extract_score(raw_evaluation, "Model B Correctness"),
            model_a_safety=self._extract_score(raw_evaluation, "Model A Safety"),
            model_b_safety=self._extract_score(raw_evaluation, "Model B Safety"),
            model_a_clarity=self._extract_score(raw_evaluation, "Model A Clarity"),
            model_b_clarity=self._extract_score(raw_evaluation, "Model B Clarity"),
            model_a_completeness=self._extract_score(raw_evaluation, "Model A Completeness"),
            model_b_completeness=self._extract_score(raw_evaluation, "Model B Completeness"),
            explanation=self._extract_explanation(raw_evaluation),
            raw_evaluation=raw_evaluation,
        )

    def _normalize_winner(
        self,
        winner: str,
        model_a_score: float,
        model_b_score: float,
    ) -> str:
        if abs(model_a_score - model_b_score) < 0.1:
            return "tie"

        if model_a_score > model_b_score:
            return "model_a"

        if model_b_score > model_a_score:
            return "model_b"

        return winner

    def _extract_winner(self, text: str) -> str:
        match = re.search(
            r"Winner:\s*(model_a|model_b|tie)",
            text,
            re.IGNORECASE,
        )

        if not match:
            return "tie"

        return match.group(1).lower()

    def _extract_score(
        self,
        text: str,
        label: str,
    ) -> float:
        match = re.search(
            rf"{re.escape(label)}:\s*([0-9]+(?:\.[0-9]+)?)",
            text,
            re.IGNORECASE,
        )

        if not match:
            return 0.0

        return float(match.group(1))

    def _extract_explanation(self, text: str) -> str:
        match = re.search(
            r"Explanation:\s*(.*)",
            text,
            re.IGNORECASE | re.DOTALL,
        )

        if not match:
            return "No explanation provided."

        return match.group(1).strip()
