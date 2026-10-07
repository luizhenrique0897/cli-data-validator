"""Main entry point for the CLI Data Sanitizer & Validator application.

Launches the interactive menu (REPL) when executed directly.
"""

from cli_data_validator.ui.menu import interactive_loop


def main() -> None:
    """Start the interactive command-line interface."""
    interactive_loop()


if __name__ == "__main__":
    main()
