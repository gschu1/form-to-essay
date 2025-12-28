"""Tests for banned words policy - ensure 'harmful' is not flagged by default."""

from pathlib import Path

from json_to_essay.compliance.checks import check_banned_words
from json_to_essay.compliance.policy import Policy
from json_to_essay.schemas.report import ComplianceReport


def test_harmful_not_in_default_banned_words():
    """Test that 'harmful' is NOT in the default banned words list."""
    policy_path = Path("config/policy.yaml")
    policy = Policy(policy_path)

    banned_words = policy.get_banned_words()
    assert "harmful" not in banned_words, "harmful should not be in default banned words"


def test_harmful_in_essay_does_not_trigger_warning():
    """Test that using 'harmful' in an essay does NOT trigger a warning with default policy."""
    policy_path = Path("config/policy.yaml")
    policy = Policy(policy_path)

    report = ComplianceReport(status="pass", run_id="test-123")
    text_with_harmful = "Some technologies can be harmful if misused, but that doesn't mean we should avoid them entirely."

    banned_words = policy.get_banned_words()
    check_banned_words(text_with_harmful, banned_words, policy, report)

    # Should NOT find "harmful" in the flagged words
    banned_reasons = [r for r in report.reasons if "BANNED_WORD" in r.code]
    assert len(banned_reasons) == 0, "harmful should not trigger a warning with default policy"


def test_explicit_banned_word_still_works():
    """Test that explicitly adding a word to banned list still works."""
    policy_path = Path("config/policy.yaml")
    policy = Policy(policy_path)

    report = ComplianceReport(status="pass", run_id="test-123")
    text_with_hate = "This essay contains hate and violence."

    banned_words = policy.get_banned_words()
    check_banned_words(text_with_hate, banned_words, policy, report)

    # Should find "hate" and "violence"
    banned_reasons = [r for r in report.reasons if "BANNED_WORD" in r.code]
    assert len(banned_reasons) > 0, "Should detect explicitly banned words"
    assert any("hate" in r.evidence.lower() or "violence" in r.evidence.lower() for r in banned_reasons)

