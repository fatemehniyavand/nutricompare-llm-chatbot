from typing import Optional

from nutricompare.application.services.meal_tracking_service import MealTrackingService


class MealCommandHandler:
    """
    Handles user commands related to meal memory.
    """

    def __init__(self, meal_tracking_service: MealTrackingService) -> None:
        self.meal_tracking_service = meal_tracking_service

    def handle(self, user_input: str) -> Optional[str]:
        normalized_input = user_input.strip().lower()

        if normalized_input in {"today summary", "today's summary", "daily summary"}:
            return self.meal_tracking_service.get_today_summary()

        if normalized_input in {"show history", "meal history", "show meal history"}:
            return self.meal_tracking_service.get_history_text()

        if normalized_input in {"clear memory", "clear meals", "reset meals"}:
            return self.meal_tracking_service.clear_memory()

        return None
