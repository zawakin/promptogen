from __future__ import annotations

import typing
from typing import Any, Dict

from pydantic import BaseModel

Model = typing.TypeVar("Model", bound="BaseModel")

# NOTE: Define BaseModel alias for BaseModel to reduce dependency on pydantic


class DataClass(BaseModel):
    """Base class for dataclasses.

    This class is a wrapper around pydantic's BaseModel class. It provides a few convenience methods for converting
    between dictionaries and dataclasses.
    """

    def to_dict(self) -> dict[str, Any]:
        """Convert the dataclass to a dictionary.

        Returns:
            A dictionary representation of the dataclass.
        """
        return super().model_dump()

    def copy(self: Model) -> Model:
        """Create a copy of the dataclass.

        Returns:
            A copy of the dataclass."""
        return self.model_copy(deep=True)

    def update(self: Model, **kwargs: Any) -> Model:
        """Create a copy of the dataclass with updated values.

        Args:
            **kwargs: The values to update.

        Returns:
            A copy of the dataclass with updated values.
        """
        if not all((key in self.model_fields.keys() for key in kwargs.keys())):
            raise ValueError(f"Invalid keys: {kwargs.keys()}")
        return self.model_copy(deep=True, update=kwargs)

    @classmethod
    def from_dict(cls: type[Model], d: Dict[str, Any]) -> Model:
        """Create a dataclass from a dictionary.

        Args:
            d: The dictionary to create the dataclass from.

        Returns:
            The created dataclass.
        """
        if not isinstance(d, dict):
            raise TypeError(f"Expected dict, got {type(d)}")
        return cls.model_validate(d)

    @classmethod
    def from_json_string(cls: type[Model], json_string: str) -> Model:
        """Create a dataclass from a JSON string.

        Args:
            json_string: The JSON string to create the dataclass from.

        Returns:
            The created dataclass.
        """
        return cls.model_validate_json(json_string)

    @classmethod
    def from_json_file(cls: type[Model], filename: str) -> Model:
        """Create a dataclass from a JSON file.

        Args:
            filename: The name of the file to create the dataclass from.

        Returns:
            The created dataclass.
        """
        with open(filename, "r") as f:
            return cls.model_validate_json(f.read())

    def to_json_file(self, filename: str, indent=4) -> None:
        """Save the dataclass to a JSON file.

        Args:
            filename: The name of the file to save the dataclass to.
            indent: The indentation level to use when saving the dataclass. Defaults to 4.
        """
        with open(filename, "w") as f:
            f.write(self.model_dump_json(indent=indent))
