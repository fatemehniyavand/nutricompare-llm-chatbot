from pydantic import BaseModel


class GuardResult(BaseModel):
    """
    Result returned by the input guard.
    """

    is_allowed: bool
    intent: str
    message: str | None = None
