"""Test utilities for handling temporary files."""

import logging
import os
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_project_tmp_dir() -> Path:
    """Get the project's temporary directory for test files.

    Returns:
        Path to the project's temporary directory.
    """
    project_root = Path(__file__).parent.parent
    tmp_dir = project_root / "tmp"
    tmp_dir.mkdir(exist_ok=True)
    return tmp_dir


def create_test_file(
    content: str,
    prefix: str = "test",
    suffix: str = ".txt",
    tmp_dir: Optional[Path] = None,
) -> Path:
    """Create a test file with the given content.

    Args:
        content: The content to write to the file
        prefix: The prefix for the filename
        suffix: The suffix for the filename
        tmp_dir: Optional temporary directory to use

    Returns:
        Path to the created file
    """
    if tmp_dir is None:
        tmp_dir = get_project_tmp_dir()

    import tempfile

    fd, path = tempfile.mkstemp(prefix=prefix, suffix=suffix, dir=tmp_dir)

    try:
        with os.fdopen(fd, "w") as f:
            f.write(content)
    finally:
        logger.info(f"Created test file: {path}")

    return Path(path)
