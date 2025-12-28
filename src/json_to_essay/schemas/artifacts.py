"""Pydantic schema for metadata artifacts."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class MetaArtifact(BaseModel):
    """Metadata about a run."""

    run_id: str = Field(description="Unique run identifier")
    timestamp: str = Field(description="ISO format timestamp")
    model: str = Field(description="Model used for generation")
    duration_ms: int = Field(description="Generation duration in milliseconds")
    spec_path: str = Field(description="Path to input spec")
    output_dir: str = Field(description="Output directory path")
    compliance_status: str = Field(description="Final compliance status")
    finish_reason: Optional[str] = Field(
        default=None, description="Generation finish reason (e.g., 'stop', 'length')"
    )
    usage: Optional[dict] = Field(
        default=None, description="Token usage (prompt_tokens, completion_tokens, total_tokens)"
    )

    @classmethod
    def create(
        cls,
        run_id: str,
        model: str,
        duration_ms: int,
        spec_path: str | Path,
        output_dir: str | Path,
        compliance_status: str,
        finish_reason: Optional[str] = None,
        usage: Optional[dict] = None,
    ) -> "MetaArtifact":
        """Create a meta artifact with current timestamp."""
        return cls(
            run_id=run_id,
            timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            model=model,
            duration_ms=duration_ms,
            spec_path=str(spec_path),
            output_dir=str(output_dir),
            compliance_status=compliance_status,
            finish_reason=finish_reason,
            usage=usage,
        )

