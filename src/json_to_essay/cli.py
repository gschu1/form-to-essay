"""CLI interface for json-to-essay."""

import sys
from pathlib import Path

import typer
from pydantic import ValidationError

from json_to_essay.compliance.policy import Policy
from json_to_essay.pipeline.run import run_pipeline
from json_to_essay.schemas.spec import EssaySpec
from json_to_essay.settings import get_settings
from json_to_essay.util.files import read_json
from json_to_essay.util.log import setup_logger

app = typer.Typer(
    help="JSON to Essay: Generate essays from JSON specs with compliance checking",
    no_args_is_help=True,
    add_completion=False,
    invoke_without_command=False,
)
logger = setup_logger()


@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context) -> None:
    """Main callback - shows help if no command is provided."""
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


@app.command(name="render")
def render(
    spec_path: str = typer.Argument(..., help="Path to JSON spec file"),
    output_dir: str = typer.Option(
        None,
        "--output-dir",
        "-o",
        help="Output directory (default: outputs/<run_id>)",
    ),
) -> None:
    """
    Render an essay from a JSON spec.

    Args:
        spec_path: Path to input JSON spec
        output_dir: Output directory for artifacts
    """
    try:
        # Convert to Path objects
        spec_path = Path(spec_path)
        
        # Load spec
        if not spec_path.exists():
            logger.error(f"Spec file not found: {spec_path}")
            sys.exit(1)

        spec_data = read_json(spec_path)
        try:
            spec = EssaySpec(**spec_data)
        except ValidationError as e:
            logger.error(f"Invalid spec: {e}")
            sys.exit(1)

        # Set output directory
        settings = get_settings()
        if output_dir is None:
            import uuid
            run_id = str(uuid.uuid4())[:8]
            output_dir = settings.output_base_dir / run_id
        else:
            output_dir = Path(output_dir)

        logger.info(f"Processing spec: {spec_path}")
        logger.info(f"Output directory: {output_dir}")

        # Load policy
        policy = Policy(settings.policy_path)

        # Run pipeline
        report, meta = run_pipeline(spec, spec_path, output_dir, policy=policy)

        # Print summary
        print(f"\n[OK] Run ID: {report.run_id}")
        print(f"[OK] Compliance status: {report.status.upper()}")
        print(f"[OK] Artifacts saved to: {output_dir}")
        if report.reasons:
            print(f"\n[WARN] Found {len(report.reasons)} compliance issues:")
            for reason in report.reasons:
                print(f"  [{reason.severity.upper()}] {reason.code}: {reason.message}")

        # Exit code based on status
        if report.status == "block":
            logger.error("Pipeline blocked due to compliance issues")
            sys.exit(2)
        elif report.status == "warn":
            logger.warning("Pipeline completed with warnings")
            sys.exit(0)
        else:
            logger.info("Pipeline completed successfully")
            sys.exit(0)

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()

