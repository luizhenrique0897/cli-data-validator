from pydantic import BaseModel, EmailStr, create_model, Field
from datetime import datetime, date
from typing import Any

from loader import Schema
from pathlib import Path

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
    """Transform a dictionary into a dynamic Pydantic V2 model"""

    @staticmethod
    def create_model_from_schema(schema: dict[str, Any], model_name: str = "DynamicDataModel"):

        fields = schema.get("config", {})
        field_definition = {}

        for field_name, rules in fields.items():
            if not isinstance(rules, dict):
                raise ValueError(
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

            # Min and Max Fields
            if "min" in rules:
                if python_type in (int, float):
                    field_kwargs["ge"] = rules["min"]
                elif python_type == str:
                    field_kwargs["min_length"] = int(rules["min"])

            if "max" in rules:
                if python_type in (int, float):
                    field_kwargs["le"] = rules["max"]
                elif python_type == str:
                    field_kwargs["max_length"] = int(rules["max"])

            # Required fields
            if not is_required:
                target_type = python_type | None
                default_value = rules.get("default", None)
            else:
                target_type = python_type
                default_value = ...

            field_definition[field_name] = (
                target_type,
                Field(default=default_value, **field_kwargs)
            )
        
        return create_model(model_name, **field_definition)

file_path = Path("core/test.yaml")
my_schema = Schema.load_file(file_path)

my_model = DynamicModelFactory.create_model_from_schema(schema=my_schema)

print(my_model)
for nome_campo, info in my_model.model_fields.items():
    print(f"Atributo: {nome_campo} | Tipo: {info.annotation} | Requerido: {info.is_required()}")
    # Exibe as restrições (gt, lt, min_length, etc.) presentes no metadata
    print("  Restrições (Field):")
    for meta in info.metadata:
        print(f"    - {meta}")

invalid_data = {
    "device_id": "teste",
    "temperature": 100
}

# VALIDAÇÃO
try:
    my_model(**invalid_data)
except Exception as e:
    print("Capturou o erro com sucesso!\n", e)