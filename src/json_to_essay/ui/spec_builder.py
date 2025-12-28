"""Spec builder for converting form data to EssaySpec."""

from dataclasses import dataclass
from typing import Optional

from json_to_essay.schemas.spec import EssaySpec


@dataclass
class FormState:
    """Form state for UI input."""

    topic: str
    purpose: str = "inform"  # inform, persuade, analyze, explain
    audience: str = "general"  # general, expert, student, executive
    length: str = "medium"  # short, medium, long
    tone: str = "neutral"  # neutral, argumentative, playful, formal
    avoid_cliches: bool = False
    use_concrete_examples: bool = False
    steelman_opposition: bool = False
    extra_notes: Optional[str] = None
    include_citations: bool = False


# Mapping dictionaries
PURPOSE_TO_MODE = {
    "inform": "facts",
    "persuade": "reflective",
    "analyze": "reflective",
    "explain": "reflective",
}

LENGTH_TO_MINUTES = {
    "short": 2,
    "medium": 5,
    "long": 10,
}

AUDIENCE_MAP = {
    "general": "educated general",
    "expert": "technical experts",
    "student": "students",
    "executive": "executive audience",
}

TONE_TO_STYLE = {
    "neutral": ["balanced", "objective"],
    "argumentative": ["persuasive", "assertive"],
    "playful": ["light", "engaging"],
    "formal": ["formal", "academic"],
}


def build_spec_from_form(form_state: FormState) -> dict:
    """
    Build an EssaySpec-compatible dict from form state.

    Args:
        form_state: Form state from UI

    Returns:
        Dictionary matching EssaySpec schema
    """
    # Map purpose to mode
    mode = PURPOSE_TO_MODE.get(form_state.purpose, "reflective")

    # Map length to reading time
    reading_time = LENGTH_TO_MINUTES.get(form_state.length, 5)

    # Map audience
    audience = AUDIENCE_MAP.get(form_state.audience, "general")

    # Map tone to style
    tone_list = TONE_TO_STYLE.get(form_state.tone, ["neutral"])

    # Build constraints
    must_include = []
    must_avoid = []

    if form_state.use_concrete_examples:
        must_include.append("concrete examples")
    if form_state.steelman_opposition:
        must_include.append("steelman opposing arguments")
    if form_state.avoid_cliches:
        must_avoid.append("cliches")

    # Add extra notes to constraints if provided
    if form_state.extra_notes:
        # Try to parse as must_include items (comma-separated)
        notes_items = [n.strip() for n in form_state.extra_notes.split(",") if n.strip()]
        must_include.extend(notes_items)

    # Build style
    style = {
        "tone": tone_list,
    }

    # Set register based on tone
    if form_state.tone == "formal":
        style["register"] = "formal"
    elif form_state.tone == "playful":
        style["register"] = "informal"
    else:
        style["register"] = "professional"

    # Build constraints
    constraints = {}
    if must_include:
        constraints["must_include"] = must_include
    if must_avoid:
        constraints["must_avoid"] = must_avoid

    # Build spec dict
    spec_dict = {
        "language": "en",
        "reading_time_minutes": reading_time,
        "topic": form_state.topic,
        "audience": audience,
        "style": style,
        "constraints": constraints,
        "persona": "reflective",
        "mode": mode,
    }

    # Add sources if citations requested (empty list signals intent)
    if form_state.include_citations:
        spec_dict["sources"] = []

    return spec_dict


def validate_spec_dict(spec_dict: dict) -> EssaySpec:
    """
    Validate and create EssaySpec from dict.

    Args:
        spec_dict: Spec dictionary

    Returns:
        Validated EssaySpec instance

    Raises:
        ValueError: If spec is invalid
    """
    try:
        return EssaySpec(**spec_dict)
    except Exception as e:
        raise ValueError(f"Invalid spec: {e}") from e

