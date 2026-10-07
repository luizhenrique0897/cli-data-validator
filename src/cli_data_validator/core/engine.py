"""Validation Engine module.

Processes streamed dataset rows against a dynamic Pydantic model,
segregating valid records from validation errors.
"""

import time
from typing import Any
from collections.abc import Generator

from pydantic import BaseModel, ValidationError


class ValidationEngine:
    """Core engine responsible for validating row-by-row data against a Pydantic model."""

    @staticmethod
    def validate(data: Generator[dict[str, str], Any, Any], validation_model: type[BaseModel]) -> dict[str, Any]:
        """Validates streaming dataset rows against the provided Pydantic model.

        Args:
            data: Generator yielding row dictionaries (typically string key-value pairs from CSV).
            validation_model: The dynamic Pydantic model class used to parse and validate each row.

        Returns:
            A dictionary containing processing statistics, valid records, and detailed error logs.
        """
        valid_records: list[dict[str, Any]] = []
        errors: list[dict[str, Any]] = []

        start_time = time.perf_counter()

        # CSV row indexing starts at 2 (accounting for 1-based index + header row)
        for row_index, line in enumerate(data, start=2):
            try:
                validated_record = validation_model(**line)
                valid_records.append(validated_record.model_dump())
            except ValidationError as e:
                for error in e.errors():
                    field_name = str(error["loc"][0]) if error["loc"] else "unknown"
                    errors.append(
                        {
                            "row": row_index,
                            "field": field_name,
                            "invalid_value": line.get(field_name),
                            "message": error["msg"],
                        }
                    )

        elapsed_time = round((time.perf_counter() - start_time), 4)

        return {
            "total_processed": len(valid_records) + len(errors),
            "valid_count": len(valid_records),
            "error_count": len(errors),
            "elapsed_seconds": elapsed_time,
            "valid_records": valid_records,
            "errors": errors,
        }
