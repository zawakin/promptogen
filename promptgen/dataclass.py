from __future__ import annotations

from typing import Any, Dict

from pydantic import BaseModel
from typing_extensions import TypeAlias

# NOTE: Define BaseModel alias for BaseModel to reduce dependency on pydantic
DataClass: TypeAlias = BaseModel


class DictLike(DataClass):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.__dict__.update(kwargs)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DictLike":
        return cls(**data)

    @classmethod
    def from_dataclass(cls, data: BaseModel) -> "DictLike":
        return cls(**data.dict())

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def pop(self, key: str) -> Any:
        return self.__dict__.pop(key)

    def keys(self):
        return self.__dict__.keys()
