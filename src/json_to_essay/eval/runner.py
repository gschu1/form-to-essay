"""Evaluation runner for testing multiple specs."""

import sys
from pathlib import Path
from typing import Optional

from json_to_essay.compliance.policy import Policy
from json_to_essay.pipeline.run import run_pipeline
from json_to_essay.schemas.spec import EssaySpec
from json_to_essay.settings import get_settings
from json_to_essay.util.files import read_json
from json_to_essay.util.log import setup_logger

logger = setup_logger()


def run_eval(examples_dir: Optional[Path] = None) -> int:
    """
    Run evaluation on all spec files in examples directory.

    Args:
        examples_dir: Directory containing spec files (default: examples/)

    Returns:
        Exit code (0 if all pass/warn, nonzero if any block)
    """
    if examples_dir is None:
        examples_dir = Path("examples")

    if not examples_dir.exists():
        logger.error(f"Examples directory not found: {examples_dir}")
        return 1

    # Find all JSON spec files
    spec_files = sorted(examples_dir.glob("spec_*.json"))
    if not spec_files:
        logger.warning(f"No spec files found in {examples_dir}")
        return 1

    settings = get_settings()
    policy = Policy(settings.policy_path)

    # Print header
    print(f"{'Spec File':<30} {'Status':<10} {'Notes':<50}")
    print("-" * 90)

    exit_code = 0
    results = []

    for spec_path in spec_files:
        try:
            # Load spec
            spec_data = read_json(spec_path)
            spec = EssaySpec(**spec_data)

            # Create output directory
            output_dir = settings.output_base_dir / "eval" / spec_path.stem
            output_dir.mkdir(parents=True, exist_ok=True)

            # Run pipeline
            report, _ = run_pipeline(spec, spec_path, output_dir, policy=policy)

            # Collect notes
            notes = []
            if report.reasons:
                note_parts = []
                for reason in report.reasons[:2]:  # Limit to first 2
                    note_parts.append(f"{reason.code}")
                notes.append(", ".join(note_parts))
            if len(report.reasons) > 2:
                notes.append(f"+{len(report.reasons) - 2} more")

            note_str = "; ".join(notes) if notes else "OK"

            # Track status
            if report.status == "block":
                exit_code = 1

            status_display = report.status.upper()
            results.append((spec_path.name, status_display, note_str))

            print(f"{spec_path.name:<30} {status_display:<10} {note_str:<50}")

        except Exception as e:
            logger.exception(f"Error processing {spec_path}: {e}")
            print(f"{spec_path.name:<30} {'ERROR':<10} {str(e)[:50]:<50}")
            exit_code = 1

    print("-" * 90)
    print(f"Processed {len(results)} spec files")

    return exit_code


def main() -> None:
    """Entry point for eval runner."""
    sys.exit(run_eval())


if __name__ == "__main__":
    main()

