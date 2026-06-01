import re
from typing import List, Optional

from nutricompare.domain.entities.parsed_food import ParsedFood


class FoodParser:
    """
    Parses nutrition-related user input into structured food items.
    """

    def parse(self, text: str) -> List[ParsedFood]:
        cleaned = self._clean_text(text)
        segments = self._split_into_segments(cleaned)

        foods: List[ParsedFood] = []

        for segment in segments:
            parsed_food = self._parse_segment(segment)
            if parsed_food:
                foods.append(parsed_food)

        return self._deduplicate(foods)

    def _clean_text(self, text: str) -> str:
        text = text.lower().strip()

        replacements = {
            ",": " and ",
            "+": " and ",
            "&": " and ",
            " with ": " and ",
            " plus ": " and ",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        removable_phrases = [
            "how many calories are in",
            "how many calories in",
            "how much calories are in",
            "how much calories in",
            "calories in",
            "i ate",
            "i eat",
            "i had",
            "i have",
            "for breakfast",
            "for lunch",
            "for dinner",
        ]

        for phrase in removable_phrases:
            text = text.replace(phrase, " ")

        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _split_into_segments(self, text: str) -> List[str]:
        segments = re.split(r"\band\b", text)
        return [
            segment.strip()
            for segment in segments
            if segment.strip()
        ]

    def _parse_segment(self, segment: str) -> Optional[ParsedFood]:
        gram_patterns = [
            r"^(?P<food>[a-zA-Z\s]+?)\s*(?P<quantity>\d+(?:\.\d+)?)\s*(?P<unit>g|gram|grams)$",
            r"^(?P<quantity>\d+(?:\.\d+)?)\s*(?P<unit>g|gram|grams)\s+(?P<food>[a-zA-Z\s]+)$",
        ]

        for pattern in gram_patterns:
            match = re.match(pattern, segment)
            if match:
                return ParsedFood(
                    name=self._normalize_food_name(match.group("food")),
                    quantity=float(match.group("quantity")),
                    unit="g",
                )

        piece_patterns = [
            r"^(?P<quantity>\d+(?:\.\d+)?)\s+(?P<food>[a-zA-Z\s]+)$",
            r"^(?P<food>[a-zA-Z\s]+)\s+(?P<quantity>\d+(?:\.\d+)?)\s*(?P<unit>piece|pieces|pcs)$",
        ]

        for pattern in piece_patterns:
            match = re.match(pattern, segment)
            if match:
                return ParsedFood(
                    name=self._normalize_food_name(match.group("food")),
                    quantity=float(match.group("quantity")),
                    unit="piece",
                )

        if re.match(r"^[a-zA-Z\s]+$", segment):
            return ParsedFood(
                name=self._normalize_food_name(segment),
                quantity=None,
                unit=None,
            )

        return None

    def _normalize_food_name(self, name: str) -> str:
        name = name.strip().lower()
        name = re.sub(r"\s+", " ", name)
        return name

    def _deduplicate(self, foods: List[ParsedFood]) -> List[ParsedFood]:
        seen = set()
        unique_foods = []

        for food in foods:
            key = (
                food.normalized_name(),
                food.quantity,
                food.unit,
            )

            if key not in seen:
                seen.add(key)
                unique_foods.append(food)

        return unique_foods
