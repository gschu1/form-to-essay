"""Provider factory for creating LLM providers."""

from typing import Optional

from json_to_essay.providers.base import LLMProvider
from json_to_essay.providers.mock_provider import MockProvider
from json_to_essay.providers.openai_provider import OpenAIProvider
from json_to_essay.settings import get_settings


def create_provider(
    provider_type: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> LLMProvider:
    """
    Create an LLM provider based on configuration.

    Args:
        provider_type: Provider type ("mock" or "openai"). If None, uses settings.
        api_key: OpenAI API key (if None, uses settings)
        model: Model name (if None, uses settings)

    Returns:
        LLM provider instance

    Raises:
        ValueError: If provider is "openai" but API key is missing
    """
    settings = get_settings()

    # Determine provider type
    if provider_type is None:
        provider_type = settings.get_provider_type()
    else:
        provider_type = provider_type.lower()

    # Create provider
    if provider_type == "openai":
        if api_key is None:
            api_key = settings.openai_api_key
        if not api_key:
            raise ValueError(
                "PROVIDER=openai requires OPENAI_API_KEY to be set. "
                "Please set it in your .env file or environment."
            )
        if model is None:
            model = settings.openai_model
        return OpenAIProvider(api_key=api_key, model=model)

    # Default to mock
    return MockProvider()

