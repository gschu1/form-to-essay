"""File utility functions."""

import json
import shutil
from pathlib import Path
from typing import Any

import yaml


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists, create if needed."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, data: Any) -> None:
    """Write data as JSON to file."""
    ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def read_json(path: Path) -> Any:
    """Read JSON from file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_text(path: Path, content: str) -> None:
    """Write text content to file."""
    ensure_dir(path.parent)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def read_text(path: Path) -> str:
    """Read text content from file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def copy_file(src: Path, dst: Path) -> None:
    """Copy a file from src to dst."""
    ensure_dir(dst.parent)
    shutil.copy2(src, dst)


def load_yaml(path: Path) -> dict:
    """Load YAML file."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

