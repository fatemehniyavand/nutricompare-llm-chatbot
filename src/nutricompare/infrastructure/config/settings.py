from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application configuration.
    Loads values from .env automatically.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ======================================================
    # App
    # ======================================================

    app_name: str = Field(default="NutriCompare AI", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=True, alias="DEBUG")

    # ======================================================
    # Model A
    # ======================================================

    model_a_provider: str = Field(alias="MODEL_A_PROVIDER")
    model_a_name: str = Field(alias="MODEL_A_NAME")
    model_a_api_key: str = Field(alias="MODEL_A_API_KEY")
    model_a_base_url: str = Field(alias="MODEL_A_BASE_URL")

    # ======================================================
    # Model B
    # ======================================================

    model_b_provider: str = Field(alias="MODEL_B_PROVIDER")
    model_b_name: str = Field(alias="MODEL_B_NAME")
    model_b_api_key: str = Field(alias="MODEL_B_API_KEY")
    model_b_base_url: str = Field(alias="MODEL_B_BASE_URL")

    # ======================================================
    # Judge Model
    # ======================================================

    judge_model_provider: str = Field(alias="JUDGE_MODEL_PROVIDER")
    judge_model_name: str = Field(alias="JUDGE_MODEL_NAME")
    judge_model_api_key: str = Field(alias="JUDGE_MODEL_API_KEY")
    judge_model_base_url: str = Field(alias="JUDGE_MODEL_BASE_URL")

    # ======================================================
    # Generation Settings
    # ======================================================

    default_temperature: float = Field(
        default=0.2,
        alias="DEFAULT_TEMPERATURE",
    )

    judge_temperature: float = Field(
        default=0.0,
        alias="JUDGE_TEMPERATURE",
    )

    max_tokens: int = Field(
        default=1200,
        alias="MAX_TOKENS",
    )

    # ======================================================
    # Evaluation
    # ======================================================

    evaluation_output_path: str = Field(
        default="eval/outputs/evaluation_results.csv",
        alias="EVALUATION_OUTPUT_PATH",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.
    """
    return Settings()
