from typing import Any, Optional, Sequence, Union

from pydantic import BaseModel, ConfigDict
from pydantic.functional_validators import field_validator
from sqlalchemy import Column
from sqlalchemy import inspect as sa_inspect
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.util import AliasedClass


class JoinArgs(BaseModel):
    model: Any
    join_type: str = "left"
    join_on: Any
    filters: Optional[dict] = None
    join_prefix: Optional[str] = None
    select_columns: Optional[type[BaseModel]] = None
    relationship_type: Optional[str] = "one-to-one"

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("relationship_type")
    def check_valid_relationship_type(cls, value):
        valid_relationship_types = {"one-to-one", "one-to-many"}
        if value is not None and value not in valid_relationship_types:
            raise ValueError(f"Invalid relationship type: {value}")  # pragma: no cover
        return value

    @field_validator("join_type")
    def check_valid_join_type(cls, value):
        valid_join_types = {"left", "inner"}
        if value not in valid_join_types:
            raise ValueError(f"Unsupported join type: {value}")
        return value


def get_primary_key(model: type[DeclarativeBase]) -> Union[str, None]:  # pragma: no cover
    """Get the first primary key of a SQLAlchemy model."""
    key: Optional[str] = get_primary_keys(model)[0].name
    return key


def get_primary_keys(model: type[DeclarativeBase]) -> Sequence[Column]:
    """Get all the primary key of a SQLAlchemy model."""
    inspector = sa_inspect(model).mapper
    primary_key_columns: Sequence[Column] = inspector.primary_key

    return primary_key_columns


def extract_columns(
    model: Union[type[DeclarativeBase], AliasedClass],
    schema: Optional[type[BaseModel]],
    prefix: Optional[str] = None,
) -> list[Any]:
    """
    Retrieves a list of ORM column objects from a SQLAlchemy model that match the field names
    in a given Pydantic schema, or all columns from the model if no schema is provided.
    When an alias is provided, columns are referenced through this alias,
    and a prefix can be applied to column names if specified.

    Args:
        model: The SQLAlchemy ORM model containing columns to be matched with the schema fields.
        schema: Optional; a Pydantic schema containing field names to be matched
            with the model's columns. If None, all columns from the model are used.
        prefix: Optional; a prefix to be added to all column names. If None, no prefix is added.

    Returns:
        A list of ORM column objects (potentially labeled with a prefix) that correspond to
        the field names defined in the schema or all columns from the model if no schema is specified.
        These columns are correctly referenced through the provided alias if one is given.
    """
    columns = []
    if schema:
        for field in schema.model_fields: # field is column.key
            if hasattr(model, field):
                column = getattr(model, field)
                if prefix is not None:
                    column_label = f"{prefix}{field}" if prefix else f"{field}"
                    column = column.label(column_label)
                columns.append(column)
    else:
        for column in model.__table__.c:
            column = getattr(model, column.key)
            if prefix is not None:
                column_label = f"{prefix}{column.key}" if prefix else f"{column.key}"
                column = column.label(column_label)
            columns.append(column)

    return columns

