import json
from pathlib import Path
from typing import Any
import yaml


class Schema:
    @staticmethod
    def load_file(file_path: Path) -> dict[str, Any]:

        # Verify if file exists
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        suffix = file_path.suffix.lower()

        with open(file=file_path, mode="r") as file:
            if suffix in [".yaml", ".yml"]:
                schema_data = yaml.safe_load(file)
            elif suffix == ".json":
                schema_data = json.load(file)
            else:
                raise ValueError(
                    f"Format not supported: {suffix}. Use .yaml, .yml or .json"
                )

        return schema_data

'''
file = "core/test.yaml"
file_path = Path(file)

new_schema = Schema()
schema = new_schema.load_file(file_path)

print(schema)
'''
