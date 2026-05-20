from typing import List

from src.domain.entities.parsed_food import ParsedFood


class ConfidenceScorer:
    """
    Calculates a simple confidence score based on parsing quality.
    """

    def score(self, foods: List[ParsedFood]) -> str:
        if not foods:
            return "low"

        total_items = len(foods)
        items_with_quantity = sum(1 for food in foods if food.has_quantity())

        if items_with_quantity == total_items:
            return "high"

        if items_with_quantity > 0:
            return "medium"

        return "low"
