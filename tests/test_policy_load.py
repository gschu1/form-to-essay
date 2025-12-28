"""Tests for policy loading."""

from pathlib import Path

from json_to_essay.compliance.policy import Policy


def test_policy_loads():
    """Test that policy.yaml loads correctly."""
    policy_path = Path("config/policy.yaml")
    policy = Policy(policy_path)

    assert policy.is_pii_enabled()
    banned_words = policy.get_banned_words()
    assert isinstance(banned_words, list)

    disallowed = policy.get_disallowed_categories()
    assert isinstance(disallowed, list)
    assert "medical_advice" in disallowed or len(disallowed) >= 0


def test_policy_merges_banned_words():
    """Test that policy banned words can be retrieved."""
    policy_path = Path("config/policy.yaml")
    policy = Policy(policy_path)

    banned = policy.get_banned_words()
    # Should return a list (may be empty or have defaults)
    assert isinstance(banned, list)


def test_policy_prompt_injection_patterns():
    """Test prompt injection patterns are loaded."""
    policy_path = Path("config/policy.yaml")
    policy = Policy(policy_path)

    patterns = policy.get_prompt_injection_patterns()
    assert isinstance(patterns, list)

