from datetime import date, datetime
from pathlib import Path
from typing import List
import json

from nutricompare.domain.entities.meal_entry import MealEntry
from nutricompare.domain.entities.parsed_food import ParsedFood


class MealMemoryService:
    """
    Persistent meal memory service.

    Meals are stored in storage/meals.json, so the memory survives
    application restarts.
    """

    def __init__(self, storage_path: str = "storage/meals.json") -> None:
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._meals: List[MealEntry] = self._load_meals()

    def add_meal(self, meal: MealEntry) -> None:
        self._meals.append(meal)
        self._save_meals()

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
        self._save_meals()

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
                f"{index}. {food_names} | "
                f"{meal.total_calories or 'unknown'} kcal | "
                f"confidence: {meal.confidence}"
            )

        return "\n".join(lines)

    def _save_meals(self) -> None:
        data = [self._meal_to_dict(meal) for meal in self._meals]

        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _load_meals(self) -> List[MealEntry]:
        if not self.storage_path.exists():
            return []

        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            return [self._dict_to_meal(item) for item in data]

        except (json.JSONDecodeError, TypeError, KeyError, ValueError):
            return []

    def _meal_to_dict(self, meal: MealEntry) -> dict:
        return {
            "created_at": meal.created_at.isoformat(),
            "total_calories": meal.total_calories,
            "confidence": meal.confidence,
            "foods": [
                {
                    "name": food.name,
                    "quantity": food.quantity,
                    "unit": food.unit,
                    "calories": food.calories,
                }
                for food in meal.foods
            ],
        }

    def _dict_to_meal(self, data: dict) -> MealEntry:
        foods = [
            ParsedFood(
                name=food.get("name", ""),
                quantity=food.get("quantity"),
                unit=food.get("unit"),
                calories=food.get("calories"),
            )
            for food in data.get("foods", [])
        ]

        return MealEntry(
            foods=foods,
            total_calories=data.get("total_calories"),
            confidence=data.get("confidence", "unknown"),
            created_at=datetime.fromisoformat(data["created_at"]),
        )
