from typing import Optional

from src.application.services.confidence_scorer import ConfidenceScorer
from src.application.services.food_parser import FoodParser
from src.application.services.meal_memory_service import MealMemoryService
from src.domain.entities.meal_entry import MealEntry


class MealTrackingService:
    """
    Coordinates food parsing, confidence scoring, and meal memory.
    """

    def __init__(
        self,
        food_parser: Optional[FoodParser] = None,
        confidence_scorer: Optional[ConfidenceScorer] = None,
        meal_memory_service: Optional[MealMemoryService] = None,
    ) -> None:
        self.food_parser = food_parser or FoodParser()
        self.confidence_scorer = confidence_scorer or ConfidenceScorer()
        self.meal_memory_service = meal_memory_service or MealMemoryService()

    def process_meal_input(self, user_input: str, total_calories: Optional[float] = None) -> MealEntry:
        foods = self.food_parser.parse(user_input)
        confidence = self.confidence_scorer.score(foods)

        meal = MealEntry(
            user_input=user_input,
            foods=foods,
            total_calories=total_calories,
            confidence=confidence,
        )

        if foods:
            self.meal_memory_service.add_meal(meal)

        return meal

    def get_today_summary(self) -> str:
        return self.meal_memory_service.today_summary()

    def clear_memory(self) -> str:
        self.meal_memory_service.clear()
        return "Meal memory cleared."

    def get_history_text(self) -> str:
        meals = self.meal_memory_service.get_all_meals()

        if not meals:
            return "No meal history found."

        lines = ["Meal history:"]

        for index, meal in enumerate(meals, start=1):
            food_names = ", ".join(food.name for food in meal.foods)
            lines.append(
                f"{index}. {food_names} | {meal.total_calories or 'unknown'} kcal | confidence: {meal.confidence}"
            )

        return "\n".join(lines)
