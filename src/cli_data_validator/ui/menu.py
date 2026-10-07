"""Interactive CLI Menu module.

Provides a terminal REPL user interface using Rich and Questionary
for dataset validation and dynamic YAML schema editing.
"""

from pathlib import Path
from typing import Any

import questionary
import yaml
from questionary import Choice
from rich.console import Console
from rich.panel import Panel

from cli_data_validator.core.engine import ValidationEngine
from cli_data_validator.core.factory import DynamicModelFactory
from cli_data_validator.core.loader import Schema
from cli_data_validator.io.readers import CSVReader
from cli_data_validator.io.writers import JSONWriter
from cli_data_validator.ui.reporter import CLIReporter

console = Console()
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SQUEMA_PATH = BASE_DIR / "core" / "test.yaml"


def display_header() -> None:
    """Clears the console screen and renders the application main banner."""
    console.clear()

    banner = Panel.fit(
        "[bold cyan]CLI Data Sanitizer & Validator Engine[/bold cyan]\n"
        "[dim]Validação e higienização de dados via Pydantic V2[/dim]",
        border_style="bright_blue",
        padding=(1, 4),
    )

    console.print(banner)
    console.print()


def interactive_loop() -> None:
    """Main interactive REPL loop managing menu navigation and user execution choices."""
    while True:
        # Show header
        display_header()

        choice = questionary.select(
            message="Choose an option:",
            choices=[
                Choice("🚀 Process and Validate Dataset (CSV)", value=1),
                Choice("✏️  Edit Existing YAML Schema", value=2),
                Choice("❌ Exit", value=3),
            ],
            style=questionary.Style(
                [
                    ("pointer", "fg:cyan bold"),
                    ("selected", "fg:cyan bold"),
                    ("highlighted", "fg:cyan"),
                ]
            ),
        ).ask()

        # Exit
        if choice == 3:
            console.print("\n[bold green]Closing the app... Goodbye![/bold green]\n")
            break

        # Process
        if choice == 1:
            data_file = questionary.text(
                message="Data file path (CSV):", default=BASE_DIR / "samples" / "MOCK_DATA.csv"
            ).ask()

            data_path = Path(data_file)
            squema_path = Path(DEFAULT_SQUEMA_PATH)

            if not data_path.exists():
                console.print("\n[bold red]Error: Data file not found![bold red]\n")
                return

            with console.status(
                "[bold green]Loading configs and analyzing dataset...[bold green]"
            ):
                squema_data = Schema.load_file(squema_path)
                model = DynamicModelFactory.create_model_from_schema(squema_data)
                records_stream = CSVReader.read(data_path)
                result = ValidationEngine.validate(
                    data=records_stream, validation_model=model
                )

                JSONWriter.write_output(
                    valid_records=result["valid_records"],
                    errors=result["errors"],
                )

                CLIReporter.print_summary(result)
                CLIReporter.print_errors(result["errors"])

            console.print("[bold green]Validation completed successfully![/bold green]")
            console.print(
                f"[bold green]Results exported to the 'output/' directory.[/bold green]"
            )
            questionary.press_any_key_to_continue(
                "Press any key to return to the main menu..."
            ).ask()
        # Edit congfigs
        elif choice == 2:
            _handle_edit_schema()


def _cast_numeric_value(val_str: str | None, field_type: str) -> Any:
    """Casts string inputs from CLI prompts to float, int, or None.

    Args:
        val_str: The string input entered by the user in the prompt.
        field_type: Target field type ('int', 'float', 'str', etc.).

    Returns:
        Converted numeric value (int or float) or None if string is blank.
    """
    if not val_str or val_str.strip() == "":
        return None

    if field_type == "float":
        return float(val_str)
    elif field_type == "int":
        return int(val_str)

    return val_str


def _handle_edit_schema() -> None:
    """Sub-menu handler for interactive schema modification and YAML serialization."""
    schema_path = Path(DEFAULT_SQUEMA_PATH)

    if not schema_path.exists():
        console.print("\n[bold red]Error: Schema file not found![/bold red]\n")
        questionary.press_any_key_to_continue(
            "Press any key to return to the main menu..."
        ).ask()
        return

    current_config = Schema.load_file(schema_path)

    while True:
        display_header()

        console.print_json(data=current_config)

        choice = questionary.select(
            message="Choose an option:",
            choices=[
                Choice("➕ Add/Edit Schema Field", value=1),
                Choice("🗑️ Remove Existing Field", value=2),
                Choice("💾 Save and Return to Main Menu", value=3),
            ],
            style=questionary.Style(
                [
                    ("pointer", "fg:cyan bold"),
                    ("selected", "fg:cyan bold"),
                    ("highlighted", "fg:cyan"),
                ]
            ),
        ).ask()

        if choice == 3:
            with open(schema_path, "w") as config_file:
                yaml.dump(
                    current_config,
                    config_file,
                    sort_keys=False,
                    allow_unicode=True,
                    indent=2,
                )
            console.print("\n[bold green]Schema saved successfully![/bold green]\n")
            break

        if choice == 1:
            _add_edit_field(current_config)
        elif choice == 2:
            _remove_field(current_config)


def _add_edit_field(config: dict) -> None:
    """Interactively prompts user for field definitions and updates schema config.

    Args:
        config: Dictionary representing the in-memory YAML schema configuration.
    """
    if "config" not in config or not isinstance(config["config"], dict):
        config["config"] = {}

    field_name = questionary.text(
        message="Name of the new field (or existing field to edit):",
    ).ask()

    if not field_name:
        return

    field_type = questionary.select(
        message="Type of the field:",
        choices=[
            "str",
            "int",
            "float",
            "bool",
            "date",
            "datetime",
            "email",
        ],
        style=questionary.Style(
            [
                ("pointer", "fg:cyan bold"),
                ("selected", "fg:cyan bold"),
                ("highlighted", "fg:cyan"),
            ]
        ),
    ).ask()

    is_required = questionary.confirm(
        message="Is it a required field?",
    ).ask()

    def is_valid_number(text: str):
        """Validates whether the user input can be parsed into a number."""
        # Permite deixar em branco caso o limite seja opcional
        if text.strip() == "":
            return True

        try:
            float(text)
            return True
        except ValueError:
            return "Please enter a valid number (e.g., 10 or 2.5)."

    if field_type in ["int", "float", "str"]:
        min_value = questionary.text(
            message="Minimum value/length (leave blank for none):", default="1", validate=is_valid_number
        ).ask()
        max_value = questionary.text(
            message="Maximum value/length (leave blank for none):", default="10", validate=is_valid_number
        ).ask()

        # Converte as strings para int/float nativos do Python
        parsed_min = _cast_numeric_value(min_value, field_type)
        parsed_max = _cast_numeric_value(max_value, field_type)

        config["config"][field_name] = {
            "type": field_type,
            "required": is_required,
            "min": parsed_min,
            "max": parsed_max,
        }
    else:
        config["config"][field_name] = {"type": field_type, "required": is_required}

    console.print(f"\n[bold green]Field {field_name} configured successfully![/bold green]\n")


def _remove_field(config: dict) -> None:
    """Interactively prompts user to remove a field from the schema.

    Args:
        config: Dictionary representing the in-memory YAML schema configuration.
    """
    if "config" not in config or not config["config"]:
            console.print("\n[bold yellow]No fields available to remove.[/bold yellow]\n")
            questionary.press_any_key_to_continue(
                "Press any key to return to the schema menu..."
            ).ask()
            return
    
    field_name = questionary.text(
        message="Name of the field to remove:",
    ).ask()

    if field_name in config["config"]:
        del config["config"][field_name]
        console.print(f"\n[bold green]Field {field_name} removed![/bold green]\n")
    else:
        console.print(f"\n[bold red]Field {field_name} not found in squema![/bold red]\n")

    questionary.press_any_key_to_continue(
        "Press any key to return to the schema menu..."
    ).ask()
