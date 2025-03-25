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
    parser = argparse.ArgumentParser(description='Templify - A template rendering tool')
    parser.add_argument('command', choices=['render', 'validate'], help='Command to execute')
    parser.add_argument('template', help='Template file or string to process')
    parser.add_argument('--context', '-c', help='JSON file containing context data')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--format', '-f', choices=['text', 'json', 'yaml', 'pdf'], help='Output format')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    # Parse arguments
    args = parser.parse_args(args)

    # Handle --help flag
    if args.command == 'help' or '-h' in sys.argv or '--help' in sys.argv:
        parser.print_help()
        return 0

    # Handle unimplemented commands
    if args.command not in ['render', 'validate']:
        print(f"Error: Command '{args.command}' not implemented")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
