"""Compliance check implementations."""

from json_to_essay.compliance.policy import Policy
from json_to_essay.schemas.report import ComplianceReport
from json_to_essay.schemas.spec import EssaySpec
from json_to_essay.util.text import (
    contains_banned_words,
    detect_pii,
    detect_prompt_injection,
    detect_strong_factual_claims,
)


def check_pii_pre(text: str, policy: Policy, report: ComplianceReport) -> None:
    """Pre-check: Detect PII in input spec."""
    if not policy.is_pii_enabled():
        report.add_check("pii_pre", True, {"enabled": False})
        return

    findings = detect_pii(text)
    if findings:
        for finding in findings:
            severity = "error" if policy.should_block_on_pii() else "warn"
            report.add_reason(
                code="PII_DETECTED",
                message=f"PII detected in input: {finding['type']}",
                severity=severity,
                evidence=finding["value"],
            )
        report.add_check("pii_pre", False, {"findings": findings})
    else:
        report.add_check("pii_pre", True, {})


def check_prompt_injection(text: str, policy: Policy, report: ComplianceReport) -> None:
    """Pre-check: Detect prompt injection patterns."""
    patterns = policy.get_prompt_injection_patterns()
    if not patterns:
        report.add_check("prompt_injection", True, {"enabled": False})
        return

    matched = detect_prompt_injection(text, patterns)
    if matched:
        report.add_reason(
            code="PROMPT_INJECTION",
            message="Potential prompt injection detected",
            severity="error",
            evidence=matched,
        )
        report.add_check("prompt_injection", False, {"matched": matched})
    else:
        report.add_check("prompt_injection", True, {})


def check_banned_words(
    text: str, banned_words: list[str], policy: Policy, report: ComplianceReport
) -> None:
    """Post-check: Detect banned words in essay."""
    if not banned_words:
        report.add_check("banned_words", True, {"no_words_configured": True})
        return

    found = contains_banned_words(text, banned_words)
    if found:
        severity = "error" if policy.should_block_on_banned_words() else "warn"
        policy_source = str(policy.policy_path) if hasattr(policy, "policy_path") else "default"
        report.add_reason(
            code="BANNED_WORD",
            message=f"Flagged words detected: {', '.join(found)}",
            severity=severity,
            evidence=f"Matched terms: {', '.join(found)} (from policy: {policy_source})",
        )
        report.add_check(
            "banned_words",
            False,
            {
                "found": found,
                "policy_source": policy_source,
                "note": "This is a heuristic flag list. Words may appear in legitimate contexts.",
            },
        )
    else:
        report.add_check("banned_words", True, {})


def check_pii_post(text: str, policy: Policy, report: ComplianceReport) -> None:
    """Post-check: Detect PII in generated essay."""
    if not policy.is_pii_enabled():
        report.add_check("pii_post", True, {"enabled": False})
        return

    findings = detect_pii(text)
    if findings:
        for finding in findings:
            severity = "error" if policy.should_block_on_pii() else "warn"
            report.add_reason(
                code="PII_IN_OUTPUT",
                message=f"PII detected in output: {finding['type']}",
                severity=severity,
                evidence=finding["value"],
            )
        report.add_check("pii_post", False, {"findings": findings})
    else:
        report.add_check("pii_post", True, {})


def check_factual_claims(
    text: str, spec: EssaySpec, policy: Policy, report: ComplianceReport
) -> None:
    """Post-check: Detect strong factual claims without sources."""
    if spec.mode == "reflective":
        # In reflective mode, warn but don't block
        claims = detect_strong_factual_claims(text)
        if claims:
            report.add_reason(
                code="STRONG_CLAIMS_REFLECTIVE",
                message="Strong factual claims detected in reflective mode",
                severity="warn",
                evidence=f"{len(claims)} claims found",
            )
            report.add_check("factual_claims", False, {"claims": claims, "mode": "reflective"})
        else:
            report.add_check("factual_claims", True, {"mode": "reflective"})
        return

    # In facts mode
    if not spec.sources and policy.facts_mode_requires_sources():
        claims = detect_strong_factual_claims(text)
        if claims:
            report.add_reason(
                code="FACTS_WITHOUT_SOURCES",
                message="Facts mode requires sources, but strong claims detected without sources",
                severity="error",
                evidence=f"{len(claims)} claims found",
            )
            report.add_check("factual_claims", False, {"claims": claims, "mode": "facts"})
        else:
            report.add_check("factual_claims", True, {"mode": "facts"})
    else:
        report.add_check("factual_claims", True, {"mode": "facts", "sources_provided": bool(spec.sources)})

