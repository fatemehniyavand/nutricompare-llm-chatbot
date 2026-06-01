import json
import re
from typing import Any, Dict, Optional


class CalorieExtractor:
    """
    Extracts estimated total calories from LLM-generated nutrition answers.
    Supports JSON output first, then robust text fallback.
    """

    def extract_total_calories(self, text: str) -> Optional[float]:
        if not text:
            return None

        json_value = self._extract_from_json(text)
        if json_value is not None:
            return json_value

        normalized_text = text.lower()

        total_line_value = self._extract_from_total_line(normalized_text)
        if total_line_value is not None:
            return total_line_value

        equation_value = self._extract_from_equation(normalized_text)
        if equation_value is not None:
            return equation_value

        per_serving_value = self._extract_from_per_serving_sentence(normalized_text)
        if per_serving_value is not None:
            return per_serving_value

        return self._fallback_extract_largest_calorie_number(normalized_text)

    def _extract_from_json(self, text: str) -> Optional[float]:
        json_blocks = re.findall(
            r"```json\s*(\{.*?\})\s*```",
            text,
            flags=re.DOTALL,
        )

        raw_candidates = json_blocks[:]

        inline_json = re.findall(
            r"(\{[^{}]*total_calories[^{}]*\})",
            text,
            flags=re.DOTALL,
        )
        raw_candidates.extend(inline_json)

        for raw_json in raw_candidates:
            try:
                data: Dict[str, Any] = json.loads(raw_json)
                value = data.get("total_calories")

                if isinstance(value, (int, float)):
                    return float(value)

                if isinstance(value, str):
                    numeric_match = re.search(r"\d+(?:\.\d+)?", value)
                    if numeric_match:
                        return float(numeric_match.group(0))

            except json.JSONDecodeError:
                continue

        return None

    def _extract_from_total_line(self, text: str) -> Optional[float]:
        total_patterns = [
            r"(total estimated calories.*)",
            r"(total calories.*)",
            r"(total estimated calorie count.*)",
            r"(total calorie count.*)",
            r"(total.*calories.*)",
            r"(so.*total.*)",
        ]

        for pattern in total_patterns:
            match = re.search(pattern, text)
            if not match:
                continue

            line = match.group(1).split("\n")[0]
            numbers = re.findall(r"\d+(?:\.\d+)?", line)

            if numbers:
                return float(numbers[-1])

        return None

    def _extract_from_equation(self, text: str) -> Optional[float]:
        match = re.search(
            r"=\s*(?P<calories>\d+(?:\.\d+)?)\s*(?:kcal|calories|calorie)",
            text,
        )

        if match:
            return float(match.group("calories"))

        return None

    def _extract_from_per_serving_sentence(self, text: str) -> Optional[float]:
        patterns = [
            r"(?:contains|has|is|around|about|approximately)\s+(?P<calories>\d+(?:\.\d+)?)\s*(?:kcal|calories|calorie)",
            r"(?P<calories>\d+(?:\.\d+)?)\s*(?:kcal|calories|calorie)\s+(?:per|for)\s+\d+",
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return float(match.group("calories"))

        return None

    def _fallback_extract_largest_calorie_number(self, text: str) -> Optional[float]:
        matches = re.findall(
            r"(?P<calories>\d+(?:\.\d+)?)\s*(?:kcal|calories|calorie)",
            text,
        )

        if not matches:
            return None

        values = [float(value) for value in matches]
        return max(values)
