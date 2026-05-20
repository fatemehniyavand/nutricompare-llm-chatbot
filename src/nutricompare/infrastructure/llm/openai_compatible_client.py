from openai import OpenAI

from nutricompare.application.interfaces.llm_client import LLMClient


class OpenAICompatibleClient(LLMClient):
    """
    LLM client for OpenAI-compatible APIs.

    Works with providers such as:
    - OpenAI
    - Groq
    - OpenRouter
    - TogetherAI
    - Any provider exposing an OpenAI-compatible chat completions API
    """

    def __init__(
        self,
        model_name: str,
        api_key: str,
        base_url: str,
        provider: str = "openai",
    ):
        self.model_name = model_name
        self.provider = provider
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 1200,
    ) -> str:
        """
        Generate a text response using a chat completion model.
        """

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        content = response.choices[0].message.content

        if content is None:
            return ""

        return content.strip()
