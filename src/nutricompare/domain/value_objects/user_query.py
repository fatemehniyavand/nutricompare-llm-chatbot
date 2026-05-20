from pydantic import BaseModel, Field


class UserQuery(BaseModel):
    """
    Validated user query.
    """

    text: str = Field(..., min_length=1)

    @property
    def normalized_text(self) -> str:
        return self.text.strip()

    def is_empty(self) -> bool:
        return len(self.normalized_text) == 0
