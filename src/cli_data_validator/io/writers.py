"""Data Output Writer module.

Handles exporting validated data records and error logs to JSON files.
"""

import json
from pathlib import Path
from typing import Any


class JSONWriter:
    """Writer class responsible for serializing dataset output records into JSON files."""

    @staticmethod
    def write_json(data: list[dict[str, Any]], file_path: Path) -> None:
        """Writes a list of dictionaries to a formatted JSON file.

        Args:
            data: List of dictionaries to be serialized.
            file_path: Target path where the JSON file will be saved.
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
        """Exports valid records and error reports to their respective JSON destination files.

        Args:
            valid_records: List of successfully validated data rows.
            errors: List of detected validation error details.
            valid_path: Target output path for valid records. Defaults to 'output/valid_data.json'.
            error_path: Target output path for error logs. Defaults to 'output/errors.json'.
        """
        cls.write_json(data=valid_records, file_path=valid_path)

        if errors:
            cls.write_json(data=errors, file_path=error_path)
