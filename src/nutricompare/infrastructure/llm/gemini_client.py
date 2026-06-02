import google.generativeai as genai

from nutricompare.application.interfaces.llm_client import LLMClient


class GeminiClient(LLMClient):
    """
    Gemini implementation of the LLMClient interface.
    """

    def __init__(
        self,
        provider: str,
        model_name: str,
        api_key: str,
        base_url: str | None = None,
    ):
        self.provider = provider
        self.model_name = model_name
        self.api_key = api_key

        if not self.api_key:
            raise ValueError("Gemini API key is missing.")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 1200,
    ) -> str:
        full_prompt = f"""
System instructions:
{system_prompt}

User request:
{user_prompt}
""".strip()

        response = self.model.generate_content(
            full_prompt,
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            },
        )

        if not response or not getattr(response, "text", None):
            return ""

        return response.text.strip()
