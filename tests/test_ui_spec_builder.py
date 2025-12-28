"""Tests for UI spec builder."""

from json_to_essay.schemas.spec import EssaySpec
from json_to_essay.ui.spec_builder import FormState, build_spec_from_form, validate_spec_dict


def test_build_spec_from_form_minimal():
    """Test building spec from minimal form state."""
    form = FormState(topic="Test topic")
    spec_dict = build_spec_from_form(form)

    # Validate it creates a valid spec
    spec = validate_spec_dict(spec_dict)

    assert spec.topic == "Test topic"
    assert spec.language == "en"
    assert spec.reading_time_minutes > 0
    assert spec.audience is not None


def test_build_spec_from_form_full():
    """Test building spec from full form state."""
    form = FormState(
        topic="The impact of AI on society",
        purpose="analyze",
        audience="expert",
        length="long",
        tone="formal",
        avoid_cliches=True,
        use_concrete_examples=True,
        steelman_opposition=True,
        extra_notes="ethics, privacy",
        include_citations=True,
    )
    spec_dict = build_spec_from_form(form)
    spec = validate_spec_dict(spec_dict)

    assert spec.topic == "The impact of AI on society"
    assert spec.mode == "reflective"  # analyze maps to reflective
    assert spec.reading_time_minutes == 10  # long maps to 10
    assert "expert" in spec.audience.lower()
    assert spec.style.tone is not None
    assert "concrete examples" in spec.constraints.must_include
    assert "steelman" in " ".join(spec.constraints.must_include).lower()
    assert "cliches" in spec.constraints.must_avoid
    assert spec.sources == []


def test_build_spec_purpose_mapping():
    """Test that purpose correctly maps to mode."""
    # Inform should map to facts
    form = FormState(topic="Test", purpose="inform")
    spec_dict = build_spec_from_form(form)
    spec = validate_spec_dict(spec_dict)
    assert spec.mode == "facts"

    # Persuade should map to reflective
    form = FormState(topic="Test", purpose="persuade")
    spec_dict = build_spec_from_form(form)
    spec = validate_spec_dict(spec_dict)
    assert spec.mode == "reflective"


def test_build_spec_length_mapping():
    """Test that length correctly maps to reading time."""
    form = FormState(topic="Test", length="short")
    spec_dict = build_spec_from_form(form)
    spec = validate_spec_dict(spec_dict)
    assert spec.reading_time_minutes == 2

    form = FormState(topic="Test", length="medium")
    spec_dict = build_spec_from_form(form)
    spec = validate_spec_dict(spec_dict)
    assert spec.reading_time_minutes == 5

    form = FormState(topic="Test", length="long")
    spec_dict = build_spec_from_form(form)
    spec = validate_spec_dict(spec_dict)
    assert spec.reading_time_minutes == 10


def test_build_spec_constraints():
    """Test constraint building from checkboxes."""
    form = FormState(
        topic="Test",
        avoid_cliches=True,
        use_concrete_examples=True,
        steelman_opposition=True,
    )
    spec_dict = build_spec_from_form(form)
    spec = validate_spec_dict(spec_dict)

    assert "concrete examples" in spec.constraints.must_include
    assert "steelman" in " ".join(spec.constraints.must_include).lower()
    assert "cliches" in spec.constraints.must_avoid


def test_validate_spec_dict_invalid():
    """Test that invalid spec dict raises error."""
    invalid_dict = {"topic": "Test"}  # Missing required fields

    try:
        validate_spec_dict(invalid_dict)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected

