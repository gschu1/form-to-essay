"""Essay generation logic."""

from typing import Optional

from json_to_essay.providers.base import LLMProvider
from json_to_essay.schemas.spec import EssaySpec
from json_to_essay.settings import get_settings


def build_prompt(spec: EssaySpec) -> str:
    """
    Build generation prompt from spec.

    Args:
        spec: Essay specification

    Returns:
        Formatted prompt string
    """
    prompt_parts = [
        f"Write an essay on the topic: {spec.topic}",
        f"Target audience: {spec.audience}",
        f"Reading time: approximately {spec.reading_time_minutes} minutes",
    ]

    if spec.style.tone:
        prompt_parts.append(f"Tone: {', '.join(spec.style.tone)}")
    if spec.style.formality_register:
        prompt_parts.append(f"Register: {spec.style.formality_register}")

    if spec.mode == "reflective":
        prompt_parts.append(
            "Mode: reflective. Use hedged language and avoid making strong factual claims. "
            "Prefer phrases like 'perhaps', 'might', 'could', 'it seems'."
        )
    elif spec.mode == "facts":
        if spec.sources:
            prompt_parts.append(f"Mode: facts. Use these sources: {', '.join(spec.sources)}")
        else:
            prompt_parts.append(
                "Mode: facts. Be careful with factual claims and ensure they are well-supported."
            )

    if spec.constraints.must_include:
        prompt_parts.append(f"Must include: {', '.join(spec.constraints.must_include)}")
    if spec.constraints.must_avoid:
        prompt_parts.append(f"Must avoid: {', '.join(spec.constraints.must_avoid)}")

    if spec.style.allowed_hedges:
        prompt_parts.append(f"Preferred hedging phrases: {', '.join(spec.style.allowed_hedges)}")

    prompt_parts.append("\nFormat the essay in Markdown with clear paragraph breaks and headings.")
    prompt_parts.append("Do not include a title unless explicitly requested.")

    return "\n".join(prompt_parts)


def estimate_tokens(reading_time_minutes: int, override: Optional[int] = None) -> int:
    """
    Estimate max tokens based on reading time with conservative defaults.

    Args:
        reading_time_minutes: Target reading time
        override: Optional override value (from env var)

    Returns:
        Estimated max tokens (capped between 400 and 4000)
    """
    if override is not None:
        return max(400, min(override, 4000))

    # Conservative token budgeting based on reading time
    # Using more generous estimates to avoid truncation
    token_map = {
        2: 600,   # short: ~450 words
        5: 1400,  # medium: ~1050 words
        10: 2800, # long: ~2100 words
    }

    # Use mapped value if exact match, otherwise interpolate
    if reading_time_minutes in token_map:
        return token_map[reading_time_minutes]
    elif reading_time_minutes < 2:
        return 400  # Floor
    elif reading_time_minutes < 5:
        # Interpolate between 2 and 5 minutes
        return int(400 + (reading_time_minutes - 1) * 333)
    elif reading_time_minutes < 10:
        # Interpolate between 5 and 10 minutes
        return int(1400 + (reading_time_minutes - 5) * 280)
    else:
        return 2800  # Cap for very long essays


def generate_essay(spec: EssaySpec, provider: LLMProvider) -> tuple[str, dict]:
    """
    Generate essay using provider.

    Args:
        spec: Essay specification
        provider: LLM provider

    Returns:
        Tuple of (essay_text, generation_metadata)
        metadata includes: finish_reason, usage (if available)
    """
    settings = get_settings()
    prompt = build_prompt(spec)
    max_tokens = estimate_tokens(
        spec.reading_time_minutes, override=settings.openai_max_output_tokens
    )
    return provider.generate_essay(prompt, max_tokens=max_tokens)

