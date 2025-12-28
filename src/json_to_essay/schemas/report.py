"""Pydantic schema for compliance report."""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class Reason(BaseModel):
    """A compliance reason/issue."""

    code: str = Field(description="Error/warning code")
    message: str = Field(description="Human-readable message")
    severity: Literal["info", "warn", "error"] = Field(description="Severity level")
    evidence: Optional[str] = Field(default=None, description="Evidence or context")


class CheckResult(BaseModel):
    """Result of a single compliance check."""

    passed: bool = Field(description="Whether the check passed")
    details: dict = Field(default_factory=dict, description="Additional details")


class ComplianceReport(BaseModel):
    """Compliance report for a generated essay."""

    status: Literal["pass", "warn", "block"] = Field(description="Overall status")
    reasons: list[Reason] = Field(default_factory=list, description="List of issues")
    checks: dict[str, CheckResult] = Field(
        default_factory=dict, description="Individual check results"
    )
    actions_taken: list[str] = Field(
        default_factory=list, description="Actions taken during processing"
    )
    run_id: str = Field(description="Unique run identifier")

    def add_reason(
        self, code: str, message: str, severity: str, evidence: Optional[str] = None
    ) -> None:
        """Add a reason to the report."""
        self.reasons.append(
            Reason(code=code, message=message, severity=severity, evidence=evidence)
        )

    def add_check(self, name: str, passed: bool, details: dict = None) -> None:
        """Add a check result."""
        self.checks[name] = CheckResult(passed=passed, details=details or {})

    def update_status(self) -> None:
        """Update overall status based on reasons."""
        if any(r.severity == "error" for r in self.reasons):
            self.status = "block"
        elif any(r.severity == "warn" for r in self.reasons):
            self.status = "warn"
        else:
            self.status = "pass"

