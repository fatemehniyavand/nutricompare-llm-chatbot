from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ParsedFood:
    """
    Represents one parsed food item from user input.
    """

    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None

    def has_quantity(self) -> bool:
        return self.quantity is not None and self.quantity > 0

    def normalized_name(self) -> str:
        return self.name.strip().lower()
