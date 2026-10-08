"""Unit tests for the Dynamic Model Factory module."""

import pytest
from pydantic import ValidationError

from cli_data_validator.core.factory import DynamicModelFactory


def test_create_model_valid_schema() -> None:
    """Tests creating a dynamic model and instantiating it with valid data."""
    schema = {
        "config": {
            "name": {"type": "str", "required": True},
            "age": {"type": "int", "required": True},
            "email": {"type": "email", "required": False},
        }
    }

    # 1. Instancia a classe do modelo dinâmico
    ModelClass = DynamicModelFactory.create_model_from_schema(schema)

    # 2. Valida dados corretos
    instance = ModelClass(name="Alice", age=30, email="alice@example.com")

    assert instance.name == "Alice"
    assert instance.age == 30
    assert instance.email == "alice@example.com"


def test_required_field_validation_error() -> None:
    """Tests that missing a required field raises a ValidationError."""
    schema = {
        "config": {
            "username": {"type": "str", "required": True},
        }
    }

    ModelClass = DynamicModelFactory.create_model_from_schema(schema)

    # Tentar instanciar sem o campo obrigatório deve disparar ValidationError
    with pytest.raises(ValidationError) as exc_info:
        ModelClass()

    assert "Field required" in str(exc_info.value)


def test_optional_field_defaults_to_none() -> None:
    """Tests that optional fields default to None when omitted."""
    schema = {
        "config": {
            "bio": {"type": "str", "required": False},
        }
    }

    ModelClass = DynamicModelFactory.create_model_from_schema(schema)
    instance = ModelClass()

    assert instance.bio is None


def test_numeric_min_max_constraints() -> None:
    """Tests numeric minimum (ge) and maximum (le) bounds enforcement."""
    schema = {
        "config": {
            "score": {"type": "float", "required": True, "min": 0.0, "max": 10.0},
        }
    }

    ModelClass = DynamicModelFactory.create_model_from_schema(schema)

    # Valor válido no limite
    valid_instance = ModelClass(score=10.0)
    assert valid_instance.score == 10.0

    # Valor abaixo do mínimo
    with pytest.raises(ValidationError):
        ModelClass(score=-1.0)

    # Valor acima do máximo
    with pytest.raises(ValidationError):
        ModelClass(score=10.5)


def test_string_length_constraints() -> None:
    """Tests string minimum (min_length) and maximum (max_length) length constraints."""
    schema = {
        "config": {
            "code": {"type": "str", "required": True, "min": 3, "max": 5},
        }
    }

    ModelClass = DynamicModelFactory.create_model_from_schema(schema)

    # Válido (3 a 5 caracteres)
    assert ModelClass(code="ABC").code == "ABC"

    # String muito curta (< 3)
    with pytest.raises(ValidationError):
        ModelClass(code="AB")

    # String muito longa (> 5)
    with pytest.raises(ValidationError):
        ModelClass(code="ABCDEF")


def test_null_boundary_values_ignored() -> None:
    """Tests that min/max set to None are safely ignored without crashing."""
    schema = {
        "config": {
            "temperature": {"type": "float", "required": True, "min": None, "max": None},
        }
    }

    # Não deve lançar TypeError ao construir o modelo
    ModelClass = DynamicModelFactory.create_model_from_schema(schema)
    instance = ModelClass(temperature=-273.15)

    assert instance.temperature == -273.15


def test_unsupported_type_raises_value_error() -> None:
    """Tests that specifying an unsupported type raises a ValueError."""
    schema = {
        "config": {
            "invalid_field": {"type": "unsupported_type"},
        }
    }

    with pytest.raises(ValueError) as exc_info:
        DynamicModelFactory.create_model_from_schema(schema)

    assert "is not recognized" in str(exc_info.value) or "is not recognize" in str(exc_info.value)


def test_non_dict_rule_raises_type_error() -> None:
    """Tests that field rules that are not dictionaries raise a TypeError."""
    schema = {
        "config": {
            "bad_field": "not_a_dict",
        }
    }

    with pytest.raises(TypeError) as exc_info:
        DynamicModelFactory.create_model_from_schema(schema)

    assert "must be a dictionary" in str(exc_info.value) or "should be a dictionary" in str(exc_info.value)