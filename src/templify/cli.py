"""
Command-line interface for Templify
"""
import argparse
import sys

from . import __version__


def main(args: list[str] | None = None) -> int:
    """
    Main entry point for the CLI.

    Args:
        args: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = argparse.ArgumentParser(
        description="Templify - Advanced templating features for Python"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    # Add subcommands here as the project grows
    parser.add_argument(
        "command",
        choices=["render-text", "render-data", "render-pdf"],
        help="Command to execute",
    )

    args = parser.parse_args(args)

    # Placeholder for command handling
    print(f"Command '{args.command}' not implemented yet")
    return 1


if __name__ == "__main__":
    sys.exit(main())
