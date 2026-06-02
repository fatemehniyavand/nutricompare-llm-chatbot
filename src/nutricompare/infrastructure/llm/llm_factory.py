from nutricompare.application.interfaces.llm_client import LLMClient
from nutricompare.infrastructure.config.settings import Settings
from nutricompare.infrastructure.llm.openai_compatible_client import OpenAICompatibleClient
from nutricompare.infrastructure.llm.gemini_client import GeminiClient


class LLMFactory:
    """
    Factory responsible for creating LLM clients from application settings.
    """

    SUPPORTED_OPENAI_COMPATIBLE_PROVIDERS = {
        "openai",
        "groq",
        "openrouter",
        "togetherai",
        "together",
    }

    def __init__(self, settings: Settings):
        self.settings = settings

    def _create_openai_compatible_client(
        self,
        provider: str,
        model_name: str,
        api_key: str,
        base_url: str,
    ) -> LLMClient:
        return OpenAICompatibleClient(
            provider=provider,
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
        )

    def create_model_a(self) -> LLMClient:
        return self.create_client(
            provider=self.settings.model_a_provider,
            model_name=self.settings.model_a_name,
            api_key=self.settings.model_a_api_key,
            base_url=self.settings.model_a_base_url,
        )

    def create_model_b(self) -> LLMClient:
        return self.create_client(
            provider=self.settings.model_b_provider,
            model_name=self.settings.model_b_name,
            api_key=self.settings.model_b_api_key,
            base_url=self.settings.model_b_base_url,
        )

    def create_judge_model(self) -> LLMClient:
        return self.create_client(
            provider=self.settings.judge_model_provider,
            model_name=self.settings.judge_model_name,
            api_key=self.settings.judge_model_api_key,
            base_url=self.settings.judge_model_base_url,
        )

    def create_client(
        self,
        provider: str,
        model_name: str,
        api_key: str,
        base_url: str,
    ) -> LLMClient:
        normalized_provider = provider.strip().lower()

        if normalized_provider in self.SUPPORTED_OPENAI_COMPATIBLE_PROVIDERS:
            return self._create_openai_compatible_client(
                provider=normalized_provider,
                model_name=model_name,
                api_key=api_key,
                base_url=base_url,
            )

        if normalized_provider == "gemini":
            return GeminiClient(
                provider=normalized_provider,
                model_name=model_name,
                api_key=api_key,
                base_url=base_url,
            )

        raise ValueError(
            f"Unsupported LLM provider: {provider}. "
            f"Supported providers: {sorted(self.SUPPORTED_OPENAI_COMPATIBLE_PROVIDERS | {'gemini'})}"
        )
