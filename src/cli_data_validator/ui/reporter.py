"""CLI Reporter module.

Renders formatted statistical summaries and error tables in the terminal using Rich.
"""

from typing import Any

from rich.console import Console
from rich.table import Table

console = Console()


class CLIReporter:
    """Reporter class responsible for displaying execution reports in the terminal."""

    @staticmethod
    def print_summary(result: dict[str, Any]) -> None:
        """Prints a styled table summarizing dataset processing statistics.

        Args:
            result: Dictionary containing total_processed, valid_count, error_count,
                    and elapsed_seconds metrics.
        """
        total = result.get("total_processed", 0)
        valid = result.get("valid_count", 0)
        errors = result.get("error_count", 0)
        elapsed = result.get("elapsed_seconds", 0.0)

        success_rate = round((valid / total * 100), 2) if total > 0 else 0.0

        table = Table(
            title="📊 Processing Summary",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="bold white", justify="right")

        table.add_row("Total Processed Rows", str(total))
        table.add_row("Valid Records", f"[green]{valid}[/green]")
        table.add_row("Failed Records", f"[red]{errors}[/red]")
        table.add_row(
            "Success Rate", f"[bold yellow]{success_rate}%[/bold yellow]"
        )
        table.add_row("Elapsed Time", f"{elapsed}s")

        console.print("\n")
        console.print(table)

    @staticmethod
    def print_errors(errors: list[dict[str, Any]], max_display: int = 5) -> None:
        """Prints a detailed breakdown table of validation errors found.

        Args:
            errors: List of error dictionaries logged during validation.
            max_display: Maximum number of error rows to show in the CLI preview table.
        """
        if not errors:
            console.print(
                "\n[bold green]✨ No validation errors found in the dataset![/bold green]\n"
            )
            return

        table = Table(
            title=f"\n⚠️ Error Details (Showing up to {max_display} failures)",
            show_header=True,
            header_style="bold red",
        )
        table.add_column("Row", style="dim", justify="right")
        table.add_column("Invalid Field", style="bold yellow")
        table.add_column("Original Value", style="white")
        table.add_column("Rejection Reason", style="red")

        for err in errors[:max_display]:
            table.add_row(
                str(err.get("row", "-")),
                str(err.get("field", "-")),
                str(err.get("invalid_value", "-")),
                str(err.get("message", "-")),
            )

        console.print(table)

        if len(errors) > max_display:
            console.print(
                f"... and {len(errors) - max_display} more hidden errors. "
                f"Check 'output/errors.json' for the complete log.[/dim]\n"
            )
