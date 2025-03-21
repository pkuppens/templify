"""
Tests for the CLI module
"""
import pytest
from templify.cli import main


def test_cli_version():
    """Test the --version flag"""
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])
    assert exc_info.value.code == 0


def test_cli_invalid_command():
    """Test invalid command handling"""
    with pytest.raises(SystemExit) as exc_info:
        main(["invalid-command"])
    assert exc_info.value.code == 2  # argparse error code


def test_cli_unimplemented_command():
    """Test unimplemented command handling"""
    with pytest.raises(SystemExit) as exc_info:
        main(["render-text"])
    assert exc_info.value.code == 1  # our error code
