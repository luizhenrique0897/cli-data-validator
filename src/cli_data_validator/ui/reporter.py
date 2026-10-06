from typing import Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class CLIReporter:
    """Show the results on CLI"""

    @staticmethod
    def print_summary(result: dict[str, Any]) -> None:
        """Exibe uma tabela com o resumo estatístico do processamento."""
        total = result.get("total_processed", 0)
        valid = result.get("valid_count", 0)
        errors = result.get("error_count", 0)
        elapsed = result.get("elapsed_seconds", 0.0)

        success_rate = round((valid / total * 100), 2) if total > 0 else 0.0

        table = Table(
            title="📊 Resumo da Processamento",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Métrica", style="cyan")
        table.add_column("Valor", style="bold white", justify="right")

        table.add_row("Total de Linhas Processadas", str(total))
        table.add_row("Registros Válidos", f"[green]{valid}[/green]")
        table.add_row("Registros com Falhas", f"[red]{errors}[/red]")
        table.add_row(
            "Taxa de Aprovação", f"[bold yellow]{success_rate}%[/bold yellow]"
        )
        table.add_row("Tempo Decorrido", f"{elapsed}s")

        console.print("\n")
        console.print(table)

    @staticmethod
    def print_errors(
        errors: list[dict[str, Any]], max_display: int = 5
    ) -> None:
        """Exibe uma tabela com o detalhamento das primeiras falhas encontradas."""
        if not errors:
            console.print(
                "\n[bold green]✨ Nenhum erro encontrado nos dados![/bold green]\n"
            )
            return

        table = Table(
            title=f"\n⚠️ Detalhes dos Erros (Exibindo até {max_display} falhas)",
            show_header=True,
            header_style="bold red",
        )
        table.add_column("Linha", style="dim", justify="right")
        table.add_column("Campo Defeituoso", style="bold yellow")
        table.add_column("Valor Original", style="white")
        table.add_column("Motivo do Rejeição", style="red")

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
                f"[dim]... e mais {len(errors) - max_display} erros ocultos. "
                f"Consulte o arquivo 'errors.json' para o log completo.[/dim]\n"
            )