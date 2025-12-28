"""Compliance router orchestrates all checks."""

import uuid
from pathlib import Path

from json_to_essay.compliance.checks import (
    check_banned_words,
    check_factual_claims,
    check_pii_post,
    check_pii_pre,
    check_prompt_injection,
)
from json_to_essay.compliance.policy import Policy
from json_to_essay.schemas.report import ComplianceReport
from json_to_essay.schemas.spec import EssaySpec


def run_pre_checks(spec: EssaySpec, policy: Policy) -> ComplianceReport:
    """
    Run pre-generation compliance checks on the spec.

    Args:
        spec: The essay specification
        policy: Compliance policy

    Returns:
        Compliance report with pre-check results
    """
    run_id = str(uuid.uuid4())
    report = ComplianceReport(status="pass", run_id=run_id)

    # Check all text fields in spec for PII
    spec_text = f"{spec.topic} {spec.audience} {spec.persona}"
    if spec.constraints.must_include:
        spec_text += " " + " ".join(spec.constraints.must_include)
    if spec.constraints.must_avoid:
        spec_text += " " + " ".join(spec.constraints.must_avoid)

    check_pii_pre(spec_text, policy, report)
    check_prompt_injection(spec_text, policy, report)

    report.update_status()
    return report


def run_post_checks(
    essay: str, spec: EssaySpec, policy: Policy, pre_report: ComplianceReport
) -> ComplianceReport:
    """
    Run post-generation compliance checks on the essay.

    Args:
        essay: Generated essay text
        spec: Original specification
        policy: Compliance policy
        pre_report: Pre-check report (to reuse run_id)

    Returns:
        Updated compliance report with all checks
    """
    report = pre_report  # Reuse same report

    # Get effective banned words
    banned_words = spec.get_effective_banned_words(policy.get_banned_words())

    check_banned_words(essay, banned_words, policy, report)
    check_pii_post(essay, policy, report)
    check_factual_claims(essay, spec, policy, report)

    report.update_status()
    return report

