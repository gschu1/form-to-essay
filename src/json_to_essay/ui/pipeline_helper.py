"""Helper functions for UI to call pipeline."""

import tempfile
import uuid
from pathlib import Path
from typing import Optional

from json_to_essay.compliance.policy import Policy
from json_to_essay.pipeline.run import run_pipeline
from json_to_essay.providers.base import LLMProvider
from json_to_essay.schemas.spec import EssaySpec
from json_to_essay.settings import get_settings
from json_to_essay.util.files import write_json


def run_pipeline_from_spec_dict(
    spec_dict: dict,
    output_dir: Path,
    provider: Optional[LLMProvider] = None,
    policy: Optional[Policy] = None,
) -> tuple:
    """
    Run pipeline from a spec dictionary (for UI use).

    Creates a temporary spec file, runs the pipeline, and returns results.

    Args:
        spec_dict: Spec dictionary
        output_dir: Output directory for artifacts
        provider: LLM provider (if None, auto-selects)
        policy: Compliance policy (if None, loads from default)

    Returns:
        Tuple of (compliance_report, meta_artifact)
    """
    # Validate spec dict
    spec = EssaySpec(**spec_dict)

    # Create temp spec file in output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    temp_spec_path = output_dir / f"tmp_spec_{uuid.uuid4().hex[:8]}.json"

    # Write spec to temp file
    write_json(temp_spec_path, spec_dict)

    try:
        # Run pipeline
        report, meta = run_pipeline(
            spec=spec,
            spec_path=temp_spec_path,
            output_dir=output_dir,
            provider=provider,
            policy=policy,
        )
        return report, meta
    finally:
        # Clean up temp spec file (it's already copied to input_spec.json)
        if temp_spec_path.exists():
            temp_spec_path.unlink()

