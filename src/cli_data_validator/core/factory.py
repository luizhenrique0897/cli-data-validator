from pydantic import BaseModel, EmailStr, create_model, Field
from datetime import datetime, date
from typing import Any

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
        pass
        #return create_model(model_name, ) ###
