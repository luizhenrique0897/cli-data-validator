import time
from typing import Any
from collections.abc import Generator

from pydantic import BaseModel, ValidationError


class ValidationEngine:
    """Validate each line of the dataset based on the pydantic validator"""

    @staticmethod
    def validate(data: Generator[dict[str, str], Any, Any], validation_model: type[BaseModel]) -> dict[str, Any]:
        """Run the validation logic

        Returns:
            dict with the filtered data
        """
        valid_records: list[dict[str, Any]] = []
        errors: list[dict[str, Any]] = []

        start_time = time.perf_counter()

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
