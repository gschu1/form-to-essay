"""Main pipeline orchestration."""

import time
from pathlib import Path
from typing import Optional

from json_to_essay.compliance.policy import Policy
from json_to_essay.compliance.router import run_post_checks, run_pre_checks
from json_to_essay.pipeline.generate import generate_essay
from json_to_essay.providers.base import LLMProvider
from json_to_essay.providers.factory import create_provider
from json_to_essay.schemas.artifacts import MetaArtifact
from json_to_essay.schemas.report import ComplianceReport
from json_to_essay.schemas.spec import EssaySpec
from json_to_essay.settings import get_settings
from json_to_essay.util.files import copy_file, write_json, write_text


def run_pipeline(
    spec: EssaySpec,
    spec_path: Path,
    output_dir: Path,
    provider: Optional[LLMProvider] = None,
    policy: Optional[Policy] = None,
) -> tuple[ComplianceReport, MetaArtifact]:
    """
    Run the complete pipeline: pre-checks → generation → post-checks → save artifacts.

    Args:
        spec: Essay specification
        spec_path: Path to input spec file
        output_dir: Output directory for artifacts
        provider: LLM provider (if None, auto-selects)
        policy: Compliance policy (if None, loads from default)

    Returns:
        Tuple of (compliance_report, meta_artifact)
    """
    settings = get_settings()

    # Load policy if not provided
    if policy is None:
        policy = Policy(settings.policy_path)

    # Get provider if not provided
    if provider is None:
        provider = create_provider()

    # Pre-checks
    pre_report = run_pre_checks(spec, policy)

    # If blocked, still generate but mark as blocked
    if pre_report.status == "block":
        pre_report.actions_taken.append("pre_check_blocked")

    # Generate essay
    start_time = time.time()
    essay, gen_metadata = generate_essay(spec, provider)
    duration_ms = int((time.time() - start_time) * 1000)

    # Post-checks
    report = run_post_checks(essay, spec, policy, pre_report)

    # Save artifacts
    output_dir.mkdir(parents=True, exist_ok=True)

    # Copy input spec
    copy_file(spec_path, output_dir / "input_spec.json")

    # Write essay
    write_text(output_dir / "essay.md", essay)

    # Write compliance report
    write_json(output_dir / "compliance_report.json", report.model_dump())

    # Write meta
    provider_type = settings.get_provider_type()
    model_name = gen_metadata.get("model", settings.openai_model if provider_type == "openai" else "mock")
    meta = MetaArtifact.create(
        run_id=report.run_id,
        model=model_name,
        duration_ms=duration_ms,
        spec_path=spec_path,
        output_dir=output_dir,
        compliance_status=report.status,
        finish_reason=gen_metadata.get("finish_reason"),
        usage=gen_metadata.get("usage"),
    )
    write_json(output_dir / "meta.json", meta.model_dump())

    return report, meta

