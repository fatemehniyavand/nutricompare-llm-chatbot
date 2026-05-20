class SafetyPolicy:
    """
    Domain safety rules for nutrition responses.
    """

    HIGH_RISK_KEYWORDS = {
        "starve",
        "starvation",
        "self-harm",
        "suicide",
        "anorexia",
        "bulimia",
        "extreme weight loss",
        "eat nothing",
        "dangerous diet",
    }

    MEDICAL_CONDITION_KEYWORDS = {
        "diabetes",
        "kidney disease",
        "pregnancy",
        "eating disorder",
        "heart disease",
    }

    @classmethod
    def contains_high_risk_content(cls, text: str) -> bool:
        normalized = text.lower()

        return any(
            keyword in normalized
            for keyword in cls.HIGH_RISK_KEYWORDS
        )

    @classmethod
    def contains_medical_context(cls, text: str) -> bool:
        normalized = text.lower()

        return any(
            keyword in normalized
            for keyword in cls.MEDICAL_CONDITION_KEYWORDS
        )

    @classmethod
    def should_recommend_professional_help(cls, text: str) -> bool:
        return (
            cls.contains_high_risk_content(text)
            or cls.contains_medical_context(text)
        )
