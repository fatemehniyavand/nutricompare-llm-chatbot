class JudgeConfidenceService:
    """
    Converts judge scores into a simple confidence label.
    """

    def calculate(
        self,
        winner: str,
        model_a_score: float,
        model_b_score: float,
    ) -> str:
        score_gap = abs(model_a_score - model_b_score)
        best_score = max(model_a_score, model_b_score)

        if winner == "tie":
            return "low"

        if best_score >= 9 and score_gap >= 1:
            return "high"

        if best_score >= 8 and score_gap >= 1:
            return "medium"

        return "low"
