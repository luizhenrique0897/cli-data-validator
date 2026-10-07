"""Dynamic Model Factory module.

Generates Pydantic V2 model classes dynamically from schema configuration dictionaries.
"""

from datetime import date, datetime
from typing import Any

from pydantic import EmailStr, Field, create_model

# Mapping from string representations in schema to Python/Pydantic types
TYPE_MAPPING: dict[str, Any] = {
    "str": str,
    "string": str,
    "int": int,
    "integer": int,
    "float": float,
    "number": float,
    "bool": bool,
    "boolean": bool,
    "date": date,
    "datetime": datetime,
    "email": EmailStr,
}


class DynamicModelFactory:
    """Factory class to construct dynamic Pydantic V2 models at runtime."""

    @staticmethod
    def create_model_from_schema(
        schema: dict[str, Any], model_name: str = "DynamicDataModel"
    ):
        """Creates a dynamic Pydantic model from a schema dictionary.

        Args:
            schema: Dictionary containing field rules under the "config" key.
            model_name: Name of the dynamically generated model class.

        Returns:
            A dynamically generated Pydantic BaseModel class.

        Raises:
            TypeError: If a field configuration rule is not a dictionary.
            ValueError: If an unsupported field type is specified.
        """

        fields = schema.get("config", {})
        field_definition = {}

        for field_name, rules in fields.items():
            if not isinstance(rules, dict):
                raise TypeError(
                    f"The field configuration of '{field_name}' should be a dictionary."
                )

            field_type = rules.get("type", "str")
            if field_type not in TYPE_MAPPING:
                raise ValueError(
                    f"The type of the field '{field_name} is not recognize ({field_type}).'"
                    f"Supported types: {list(TYPE_MAPPING.keys())}"
                )

            python_type = TYPE_MAPPING[field_type]
            is_required = rules.get("required", True)

            # Arguments for pydantic.Field
            field_kwargs = {}

            # Process minimum constraints (ge for numeric, min_length for strings)
            if "min" in rules:
                if python_type in (int, float):
                    field_kwargs["ge"] = rules["min"]
                elif python_type == str:
                    field_kwargs["min_length"] = int(rules["min"])

            # Process maximum constraints (le for numeric, max_length for strings)
            if "max" in rules:
                if python_type in (int, float):
                    field_kwargs["le"] = rules["max"]
                elif python_type == str:
                    field_kwargs["max_length"] = int(rules["max"])

            # Define field requirement status and default value
            if not is_required:
                target_type = python_type | None
                default_value = rules.get("default", None)
            else:
                target_type = python_type
                default_value = ...

            field_definition[field_name] = (
                target_type,
                Field(default=default_value, **field_kwargs),
            )

        return create_model(model_name, **field_definition)
