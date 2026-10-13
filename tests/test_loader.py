"""Unit tests for the loader module."""

import json
from pathlib import Path

import pytest
import yaml

from cli_data_validator.core.loader import Schema


def test_load_valid_yaml(tmp_path: Path) -> None:
    """Tests loading a valid YAML schema file."""
    # 1. Arrange: cria um arquivo YAML temporário
    yaml_content = {
        "config": {
            "age": {"type": "int", "required": True}
        }
    }
    file_path = tmp_path / "schema.yaml"
    file_path.write_text(yaml.dump(yaml_content), encoding="utf-8")

    # 2. Act: chama a função do módulo
    loaded_schema = Schema.load_file(file_path)

    # 3. Assert: verifica se o resultado é o esperado
    assert loaded_schema == yaml_content
    assert "config" in loaded_schema
    assert loaded_schema["config"]["age"]["type"] == "int"


def test_load_valid_json(tmp_path: Path) -> None:
    """Tests loading a valid JSON schema file."""
    json_content = {"config": {"email": {"type": "email", "required": True}}}
    file_path = tmp_path / "schema.json"
    file_path.write_text(json.dumps(json_content), encoding="utf-8")

    loaded_schema = Schema.load_file(file_path)

    assert loaded_schema == json_content
    assert loaded_schema["config"]["email"]["type"] == "email"

def test_load_file_not_found() -> None:
    """Tests if FileNotFoundError is raised when the file does not exist."""
    non_existent_path = Path("invalid/path/config.yaml")
    with pytest.raises(FileNotFoundError) as exc_info:
        Schema.load_file(non_existent_path)

    assert "File not found:" in str(exc_info.value)

def test_unsupported_file_extension(tmp_path: Path) -> None:
    """Tests if ValueError is raised when an unsupported extension is passed."""
    file_path = tmp_path / "schema.txt"
    file_path.write_text("dummy content", encoding="utf-8")

    with pytest.raises(ValueError) as exc_info:
        Schema.load_file(file_path)

    assert "Format not supported:" in str(exc_info.value)