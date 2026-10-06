import json
from typing import Any
from pathlib import Path

class JSONWriter:
    """Export results to JSON files"""

    @staticmethod
    def write_json(data: list[dict[str, Any]], file_path: Path) -> None:
        """
        Create json file
        """
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, mode="w", encoding="utf-8") as file:
            json.dump(
                data, 
                file, 
                indent=4,
                ensure_ascii=False,
                sort_keys=True,
                default=str,
            )

    @classmethod
    def write_output(
        cls,
        valid_records: list[dict[str, Any]],
        errors: list[dict[str, Any]],
        valid_path: Path = Path("output/valid_data.json"),
        error_path: Path = Path("output/errors.json"),
    ) -> None:
        """
        Write valid data and errors to json files
        """
        cls.write_json(data=valid_records, file_path=valid_path)

        if errors:
            cls.write_json(data=errors, file_path=error_path)