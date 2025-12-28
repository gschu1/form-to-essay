"""Base provider interface for LLM providers."""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate_essay(self, prompt: str, max_tokens: int = 2000) -> tuple[str, dict]:
        """
        Generate an essay from a prompt.

        Args:
            prompt: The generation prompt
            max_tokens: Maximum tokens to generate

        Returns:
            Tuple of (essay_text, metadata_dict)
            metadata should include: finish_reason, model, usage (if available)
        """
        pass

