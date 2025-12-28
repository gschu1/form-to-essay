"""Static checks for evaluation."""

from pathlib import Path

from json_to_essay.schemas.spec import EssaySpec
from json_to_essay.util.files import read_json


def validate_spec_file(spec_path: Path) -> tuple[bool, str]:
    """
    Validate a spec file can be loaded and parsed.

    Args:
        spec_path: Path to spec file

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        if not spec_path.exists():
            return False, "File not found"

        spec_data = read_json(spec_path)
        EssaySpec(**spec_data)
        return True, ""
    except Exception as e:
        return False, str(e)

