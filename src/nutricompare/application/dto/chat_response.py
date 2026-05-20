from pydantic import BaseModel

from nutricompare.domain.entities.nutrition_answer import NutritionAnswer


class ChatResponse(BaseModel):
    """
    Response DTO returned to the presentation layer.
    """

    result: NutritionAnswer
