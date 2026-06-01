import re
from typing import Optional


class CalorieExtractor:
    """
    Extracts estimated total calories from LLM-generated nutrition answers.
    """

    def extract_total_calories(self, text: str) -> Optional[float]:
        if not text:
            return None

        normalized_text = text.lower()

        total_line_value = self._extract_from_total_line(normalized_text)
        if total_line_value is not None:
            return total_line_value

        equation_value = self._extract_from_equation(normalized_text)
        if equation_value is not None:
            return equation_value

        return self._fallback_extract_largest_calorie_number(normalized_text)

    def _extract_from_total_line(self, text: str) -> Optional[float]:
        total_patterns = [
            r"(total estimated calories.*)",
            r"(total calories.*)",
            r"(total estimated calorie count.*)",
            r"(total calorie count.*)",
        ]

        for pattern in total_patterns:
            match = re.search(pattern, text)
            if not match:
                continue

            line = match.group(1)
            line = line.split("\n")[0]

            numbers = re.findall(r"\d+(?:\.\d+)?", line)

            if numbers:
                return float(numbers[-1])

        return None

    def _extract_from_equation(self, text: str) -> Optional[float]:
        match = re.search(
            r"=\s*(?P<calories>\d+(?:\.\d+)?)\s*(?:kcal|calories)",
            text,
        )

        if match:
            return float(match.group("calories"))

        return None

    def _fallback_extract_largest_calorie_number(self, text: str) -> Optional[float]:
        matches = re.findall(
            r"(?P<calories>\d+(?:\.\d+)?)\s*(?:kcal|calories)",
            text,
        )

        if not matches:
            return None

        values = [float(value) for value in matches]
        return max(values)
