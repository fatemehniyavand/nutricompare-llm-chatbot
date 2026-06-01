from datetime import date
from typing import List

from nutricompare.domain.entities.meal_entry import MealEntry


class MealMemoryService:
    """
    Stores meal history during the current application session.
    """

    def __init__(self) -> None:
        self._meals: List[MealEntry] = []

    def add_meal(self, meal: MealEntry) -> None:
        self._meals.append(meal)

    def get_all_meals(self) -> List[MealEntry]:
        return self._meals

    def get_today_meals(self) -> List[MealEntry]:
        today = date.today()
        return [
            meal for meal in self._meals
            if meal.created_at.date() == today
        ]

    def clear(self) -> None:
        self._meals.clear()

    def today_summary(self) -> str:
        today_meals = self.get_today_meals()

        if not today_meals:
            return "No meals saved for today."

        total_calories = sum(
            meal.total_calories or 0
            for meal in today_meals
        )

        lines = [
            "Today's meal summary:",
            f"Meals saved: {len(today_meals)}",
            f"Total calories: {round(total_calories, 2)} kcal",
            "",
            "Meals:",
        ]

        for index, meal in enumerate(today_meals, start=1):
            food_names = ", ".join(food.name for food in meal.foods)
            lines.append(
                f"{index}. {food_names} | {meal.total_calories or 'unknown'} kcal | confidence: {meal.confidence}"
            )

        return "\n".join(lines)
