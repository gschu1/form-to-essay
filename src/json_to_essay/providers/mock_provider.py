"""Mock LLM provider for testing."""

from json_to_essay.providers.base import LLMProvider


class MockProvider(LLMProvider):
    """Mock provider that returns deterministic essay text."""

    def generate_essay(self, prompt: str, max_tokens: int = 2000) -> tuple[str, dict]:
        """
        Generate a mock essay.

        Args:
            prompt: The generation prompt (ignored for mock)
            max_tokens: Maximum tokens (ignored for mock)

        Returns:
            Tuple of (essay_text, metadata_dict)
            metadata includes: finish_reason="stop", usage (mock values), model="mock"
        """
        essay_text = """# Reflections on Quiet Contemplation

In our increasingly connected world, the value of quiet reflection has become more precious than ever. The constant stream of notifications, the endless scroll of information, and the pressure to remain perpetually engaged have made moments of stillness rare commodities.

## The Nature of Reflection

Reflection, at its core, is an act of balance. It requires us to step back from the immediate demands of daily life and consider our experiences with a measure of distance. This process is not about escaping reality, but rather about engaging with it more deeply.

## Finding Balance

The challenge lies in maintaining this balance—between action and contemplation, between engagement and solitude. Perhaps the most valuable lesson is that reflection need not be a grand gesture. Small moments of pause, brief intervals of thought, can accumulate into a more considered approach to life.

## Conclusion

In embracing reflection, we find not escape, but a richer engagement with the world around us. The quiet moments are not voids to be filled, but spaces where understanding can grow.
"""

        metadata = {
            "finish_reason": "stop",
            "model": "mock",
            "usage": {
                "prompt_tokens": 100,
                "completion_tokens": 200,
                "total_tokens": 300,
            },
        }

        return essay_text, metadata

