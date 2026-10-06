from pydantic import BaseModel, ValidationError
from pathlib import Path
from typing import Any
import time
import sys

from cli_data_validator.core.loader import Schema
from cli_data_validator.core.factory import DynamicModelFactory
from cli_data_validator.io.readers import CSVReader
from cli_data_validator.io.writers import JSONWriter

class ValidationEngine:
    """Validate each line of the dataset based on the pydantic validator"""

    @staticmethod
    def validate(data: list, validation_model: type[BaseModel]) -> dict[str, Any]:
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
                    field_name = (
                        str(error["loc"][0]) if error["loc"] else "unknown"
                    )
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
            "errors": errors
        }

config_file_path = Path("./src/cli_data_validator/core/test.yaml")
my_schema = Schema.load_file(file_path=config_file_path)
csv_file_path = Path("./samples/MOCK_DATA.csv")
input_data = CSVReader.read(file_path=csv_file_path)
custom_model = DynamicModelFactory.create_model_from_schema(schema=my_schema)

test = ValidationEngine.validate(data=input_data, validation_model=custom_model)

JSONWriter.write_output(test["valid_records"], test["errors"], Path("./src/cli_data_validator/core/result.json"), Path("./src/cli_data_validator/core/errors.json"))
