from pathlib import Path
import typer

from cli_data_validator.core.factory import DynamicModelFactory
from cli_data_validator.core.loader import Schema
from cli_data_validator.core.engine import ValidationEngine
from cli_data_validator.io.readers import CSVReader
from cli_data_validator.io.writers import JSONWriter
from cli_data_validator.ui.reporter import CLIReporter

app = typer.Typer(help="CLI Data Sanitizer & Validator Engine")


@app.command()
def process(
    data_path: Path = typer.Argument(..., help="Caminho do arquivo CSV de entrada"),
    schema_path: Path = typer.Option(..., "--schema", "-s", help="Caminho do arquivo YAML/JSON de regras"),
    output_dir: Path = typer.Option(Path("output"), "--output", "-o", help="Diretório de saída dos JSONs"),
) -> None:
    """Valida um dataset com base em um esquema e exporta os resultados."""
    # 1. Carrega esquema e modelo
    schema_data = Schema.load_file(schema_path)
    model = DynamicModelFactory.create_model_from_schema(schema_data)

    # 2. Lê os dados e executa a validação
    records_stream = CSVReader.read(data_path)
    result = ValidationEngine.validate(data=records_stream, validation_model=model)

    # 3. Salva os resultados em arquivo
    JSONWriter.write_output(
        valid_records=result["valid_records"],
        errors=result["errors"],
        valid_path=output_dir / "valid_data.json",
        error_path=output_dir / "errors.json",
    )

    # 4. Imprime o relatório visual no terminal
    CLIReporter.print_summary(result)
    CLIReporter.print_errors(result["errors"])


if __name__ == "__main__":
    app()