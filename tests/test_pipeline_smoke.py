"""Smoke tests for the full pipeline."""

from pathlib import Path

from json_to_essay.compliance.policy import Policy
from json_to_essay.pipeline.run import run_pipeline
from json_to_essay.providers.mock_provider import MockProvider
from json_to_essay.schemas.spec import EssaySpec
from json_to_essay.settings import get_settings
from json_to_essay.util.files import read_json


def test_pipeline_smoke_with_mock():
    """Test full pipeline with MockProvider."""
    # Load minimal spec
    spec_path = Path("examples/spec_min.json")
    spec_data = read_json(spec_path)
    spec = EssaySpec(**spec_data)

    # Setup
    settings = get_settings()
    policy = Policy(settings.policy_path)
    provider = MockProvider()

    # Create output directory
    output_dir = Path("outputs/test_smoke")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Run pipeline
    report, meta = run_pipeline(spec, spec_path, output_dir, provider=provider, policy=policy)

    # Verify artifacts exist
    assert (output_dir / "input_spec.json").exists()
    assert (output_dir / "essay.md").exists()
    assert (output_dir / "compliance_report.json").exists()
    assert (output_dir / "meta.json").exists()

    # Verify compliance report is valid
    assert report.run_id == meta.run_id
    assert report.status in ["pass", "warn", "block"]
    assert isinstance(report.checks, dict)

    # Verify essay content
    essay_content = (output_dir / "essay.md").read_text(encoding="utf-8")
    assert len(essay_content) > 0
    assert "#" in essay_content or len(essay_content) > 100  # Has heading or substantial content

    # Verify meta
    assert meta.compliance_status == report.status
    assert meta.duration_ms >= 0
    assert meta.model == "mock"
    assert meta.finish_reason == "stop"  # Mock provider should always finish normally
    assert meta.usage is not None
    assert "completion_tokens" in meta.usage


def test_pipeline_creates_valid_json():
    """Test that compliance_report.json is valid JSON."""
    spec_path = Path("examples/spec_min.json")
    spec_data = read_json(spec_path)
    spec = EssaySpec(**spec_data)

    settings = get_settings()
    policy = Policy(settings.policy_path)
    provider = MockProvider()

    output_dir = Path("outputs/test_json")
    output_dir.mkdir(parents=True, exist_ok=True)

    run_pipeline(spec, spec_path, output_dir, provider=provider, policy=policy)

    # Try to load the JSON
    report_data = read_json(output_dir / "compliance_report.json")
    assert "status" in report_data
    assert "run_id" in report_data
    assert "reasons" in report_data
    assert "checks" in report_data

