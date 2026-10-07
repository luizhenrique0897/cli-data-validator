"""Schema Loader module.

Handles loading and parsing configuration schema files in YAML or JSON format.
"""

import json
from pathlib import Path
from typing import Any

import yaml


class Schema:
    """Utility class for loading schema configurations from files."""

    @staticmethod
    def load_file(file_path: Path) -> dict[str, Any]:
        """Loads a configuration schema from a YAML or JSON file.

        Args:
            file_path: Path object pointing to the schema file (.yaml, .yml, or .json).

        Returns:
            A dictionary containing the parsed schema structure.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the file extension is not supported.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        suffix = file_path.suffix.lower()

        with open(file=file_path, mode="r", encoding="utf-8") as file:
            if suffix in [".yaml", ".yml"]:
                schema_data = yaml.safe_load(file)
            elif suffix == ".json":
                schema_data = json.load(file)
            else:
                raise ValueError(
                    f"Format not supported: {suffix}. Use .yaml, .yml or .json"
                )

        # Fallback to empty dict if the file is empty (yaml.safe_load returns None for empty files)
        return schema_data or {}
