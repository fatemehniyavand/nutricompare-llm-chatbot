class EvaluationPolicy:
    """
    Domain rules for evaluation logic.
    """

    MIN_SCORE = 0
    MAX_SCORE = 10

    @classmethod
    def is_valid_score(cls, value: float) -> bool:
        return cls.MIN_SCORE <= value <= cls.MAX_SCORE

    @classmethod
    def normalize_winner(cls, winner: str) -> str:
        normalized = winner.strip().lower()

        allowed = {
            "model_a",
            "model_b",
            "tie",
        }

        if normalized not in allowed:
            return "tie"

        return normalized
