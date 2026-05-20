from abc import ABC, abstractmethod


class LLMClient(ABC):
    """
    Abstract interface for all language model clients.

    Any provider such as OpenAI, Groq, OpenRouter, TogetherAI, or local models
    must implement this interface.
    """

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 1200,
    ) -> str:
        """
        Generate a text response from a language model.
        """
        raise NotImplementedError
