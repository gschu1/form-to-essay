"""Pydantic schema for input specification."""

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class StyleSpec(BaseModel):
    """Style specification for essay generation."""

    model_config = ConfigDict(populate_by_name=True)

    tone: Optional[list[str]] = Field(default=None, description="Tone descriptors")
    formality_register: Optional[str] = Field(
        default=None, alias="register", description="Formality level"
    )
    banned_words: Optional[list[str]] = Field(default=None, description="Words to avoid")
    allowed_hedges: Optional[list[str]] = Field(
        default=None, description="Allowed hedging phrases"
    )


class ConstraintsSpec(BaseModel):
    """Constraints for essay content."""

    must_include: Optional[list[str]] = Field(
        default=None, description="Topics/phrases that must appear"
    )
    must_avoid: Optional[list[str]] = Field(
        default=None, description="Topics/phrases to avoid"
    )


class EssaySpec(BaseModel):
    """Complete essay specification from JSON input."""

    language: str = Field(description="Language code (e.g., 'en')")
    reading_time_minutes: int = Field(gt=0, description="Target reading time in minutes")
    topic: str = Field(description="Essay topic")
    audience: str = Field(description="Target audience description")
    style: StyleSpec = Field(description="Style preferences")
    constraints: ConstraintsSpec = Field(description="Content constraints")
    persona: str = Field(default="reflective", description="Writing persona")
    mode: Literal["reflective", "facts"] = Field(
        default="reflective", description="Essay mode"
    )
    sources: Optional[list[str]] = Field(
        default=None, description="Source URLs or citations"
    )

    def get_effective_banned_words(self, policy_banned: list[str]) -> list[str]:
        """Merge policy banned words with spec-specific banned words."""
        spec_banned = self.style.banned_words or []
        combined = list(set(policy_banned + spec_banned))
        return combined

