"""OpenAI provider for essay generation."""

import time
from typing import Optional

from openai import OpenAI
from openai import APITimeoutError, APIError, RateLimitError

from json_to_essay.providers.base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI API provider."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini", timeout: int = 60):
        """
        Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key
            model: Model name to use
            timeout: Request timeout in seconds
        """
        self.client = OpenAI(api_key=api_key, timeout=timeout)
        self.model = model
        self.timeout = timeout

    def generate_essay(self, prompt: str, max_tokens: int = 2000) -> tuple[str, dict]:
        """
        Generate an essay using OpenAI API with retries and error handling.

        Args:
            prompt: The generation prompt
            max_tokens: Maximum tokens to generate

        Returns:
            Tuple of (essay_text, metadata_dict)
            metadata includes: finish_reason, usage (prompt_tokens, completion_tokens, total_tokens), model

        Raises:
            ValueError: If API key is invalid or missing
            RuntimeError: If generation fails after retries
        """
        max_retries = 2
        retry_delay = 1.0

        for attempt in range(max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a thoughtful essay writer. Generate well-structured essays in Markdown format.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=max_tokens,
                    temperature=0.7,
                )

                choice = response.choices[0]
                content = choice.message.content
                if not content:
                    raise RuntimeError("OpenAI API returned empty response")

                # Extract metadata
                metadata = {
                    "finish_reason": choice.finish_reason or "unknown",
                    "model": self.model,
                }

                # Extract usage if available
                if hasattr(response, "usage") and response.usage:
                    metadata["usage"] = {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens,
                    }

                return content, metadata

            except APITimeoutError as e:
                if attempt < max_retries:
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                raise RuntimeError(
                    f"OpenAI API request timed out after {self.timeout}s. "
                    "Please check your connection or try again later."
                ) from e

            except RateLimitError as e:
                if attempt < max_retries:
                    wait_time = retry_delay * (2 ** attempt)
                    time.sleep(wait_time)
                    continue
                raise RuntimeError(
                    "OpenAI API rate limit exceeded. Please wait a moment and try again."
                ) from e

            except APIError as e:
                error_msg = str(e)
                if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
                    raise ValueError(
                        "Invalid or missing OpenAI API key. "
                        "Please check your OPENAI_API_KEY environment variable."
                    ) from e
                if attempt < max_retries:
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                raise RuntimeError(
                    f"OpenAI API error: {error_msg}. Please check your API key and try again."
                ) from e

            except Exception as e:
                if attempt < max_retries:
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                raise RuntimeError(
                    f"Unexpected error calling OpenAI API: {str(e)}"
                ) from e

        raise RuntimeError("Failed to generate essay after retries")

