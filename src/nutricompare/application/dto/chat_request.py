from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Request DTO for nutrition chat queries.
    """

    user_question: str = Field(
        ...,
        min_length=1,
        description="User nutrition question",
    )
