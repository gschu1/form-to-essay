"""Tests for spec schema validation."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from json_to_essay.schemas.spec import EssaySpec
from json_to_essay.util.files import read_json


def test_spec_min_validates():
    """Test that spec_min.json validates correctly."""
    spec_path = Path("examples/spec_min.json")
    spec_data = read_json(spec_path)
    spec = EssaySpec(**spec_data)

    assert spec.language == "en"
    assert spec.reading_time_minutes == 3
    assert spec.topic == "The value of quiet reflection in a noisy world"
    assert spec.mode == "reflective"
    assert spec.persona == "reflective"


def test_spec_required_fields():
    """Test that required fields are enforced."""
    with pytest.raises(ValidationError):
        EssaySpec(
            language="en",
            reading_time_minutes=3,
            # Missing topic, audience, style, constraints
        )


def test_spec_optional_fields():
    """Test that optional fields work correctly."""
    spec = EssaySpec(
        language="en",
        reading_time_minutes=3,
        topic="Test",
        audience="general",
        style={},
        constraints={},
    )
    assert spec.persona == "reflective"  # Default
    assert spec.mode == "reflective"  # Default
    assert spec.sources is None


def test_spec_get_effective_banned_words():
    """Test merging of banned words."""
    spec = EssaySpec(
        language="en",
        reading_time_minutes=3,
        topic="Test",
        audience="general",
        style={"banned_words": ["word1", "word2"]},
        constraints={},
    )
    policy_banned = ["word2", "word3"]
    effective = spec.get_effective_banned_words(policy_banned)
    assert "word1" in effective
    assert "word2" in effective
    assert "word3" in effective
    assert len(effective) == 3

