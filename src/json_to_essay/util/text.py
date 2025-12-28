"""Text processing utilities."""

import re
from typing import Optional


def detect_email(text: str) -> Optional[str]:
    """Detect email address in text. Returns first match or None."""
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    match = re.search(pattern, text)
    return match.group(0) if match else None


def detect_phone(text: str) -> Optional[str]:
    """Detect phone number in text. Returns first match or None."""
    # Simple pattern for common formats
    patterns = [
        r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",  # US format
        r"\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b",  # International
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return None


def detect_pii(text: str) -> list[dict[str, str]]:
    """Detect PII in text. Returns list of {type, value} dicts."""
    findings = []
    email = detect_email(text)
    if email:
        findings.append({"type": "email", "value": email})
    phone = detect_phone(text)
    if phone:
        findings.append({"type": "phone", "value": phone})
    return findings


def detect_prompt_injection(text: str, patterns: list[str]) -> Optional[str]:
    """Detect prompt injection patterns. Returns matched pattern or None."""
    text_lower = text.lower()
    for pattern in patterns:
        if pattern.lower() in text_lower:
            return pattern
    return None


def detect_strong_factual_claims(text: str) -> list[str]:
    """Detect strong factual claims (heuristic: assertive verbs + numbers/dates)."""
    # Simple heuristic: look for assertive verbs followed by numbers or dates
    assertive_verbs = [
        "proves",
        "demonstrates",
        "shows",
        "confirms",
        "establishes",
        "reveals",
        "discovered",
        "found",
        "determined",
    ]
    # Look for dates (YYYY, YYYY-MM-DD, etc.) or standalone numbers
    date_pattern = r"\b(19|20)\d{2}(-\d{2}(-\d{2})?)?\b"
    number_pattern = r"\b\d+%?\b"

    findings = []
    sentences = re.split(r"[.!?]+", text)
    for sentence in sentences:
        sentence_lower = sentence.lower()
        has_assertive = any(verb in sentence_lower for verb in assertive_verbs)
        has_fact = bool(re.search(date_pattern, sentence) or re.search(number_pattern, sentence))
        if has_assertive and has_fact:
            findings.append(sentence.strip())
    return findings


def contains_banned_words(text: str, banned_words: list[str]) -> list[str]:
    """Check if text contains banned words. Returns list of found words."""
    text_lower = text.lower()
    found = []
    for word in banned_words:
        if word.lower() in text_lower:
            found.append(word)
    return found

