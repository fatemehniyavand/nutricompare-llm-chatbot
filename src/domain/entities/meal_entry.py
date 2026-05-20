from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from src.domain.entities.parsed_food import ParsedFood


@dataclass
class MealEntry:
    """
    Represents one saved meal interaction.
    """

    user_input: str
    foods: List[ParsedFood]
    total_calories: Optional[float] = None
    confidence: str = "unknown"
    created_at: datetime = field(default_factory=datetime.utcnow)
