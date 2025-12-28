"""Policy loading and management."""

from pathlib import Path
from typing import Any

from json_to_essay.util.files import load_yaml


class Policy:
    """Compliance policy loaded from YAML."""

    def __init__(self, policy_path: Path):
        """
        Load policy from YAML file.

        Args:
            policy_path: Path to policy.yaml
        """
        self.policy_path = policy_path
        self.data: dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """Load policy from file."""
        if not self.policy_path.exists():
            # Use defaults if file doesn't exist
            self.data = self._default_policy()
            return
        self.data = load_yaml(self.policy_path)

    def _default_policy(self) -> dict[str, Any]:
        """Return default policy if file is missing."""
        return {
            "banned_words_default": [],
            "disallowed_categories": [],
            "pii": {"enabled": True},
            "prompt_injection": {"enabled": True, "patterns": []},
            "compliance": {
                "facts_mode_requires_sources": True,
                "block_on_pii": False,
                "block_on_banned_words": False,
            },
        }

    def get_banned_words(self) -> list[str]:
        """Get default banned words from policy."""
        return self.data.get("banned_words_default", [])

    def get_disallowed_categories(self) -> list[str]:
        """Get disallowed content categories."""
        return self.data.get("disallowed_categories", [])

    def is_pii_enabled(self) -> bool:
        """Check if PII detection is enabled."""
        return self.data.get("pii", {}).get("enabled", True)

    def get_prompt_injection_patterns(self) -> list[str]:
        """Get prompt injection detection patterns."""
        if not self.data.get("prompt_injection", {}).get("enabled", True):
            return []
        return self.data.get("prompt_injection", {}).get("patterns", [])

    def should_block_on_pii(self) -> bool:
        """Check if PII should block (vs warn)."""
        return self.data.get("compliance", {}).get("block_on_pii", False)

    def should_block_on_banned_words(self) -> bool:
        """Check if banned words should block (vs warn)."""
        return self.data.get("compliance", {}).get("block_on_banned_words", False)

    def facts_mode_requires_sources(self) -> bool:
        """Check if facts mode requires sources."""
        return self.data.get("compliance", {}).get("facts_mode_requires_sources", True)

