import functools
from typing import Any

from pydantic import BaseModel

# NOTE: Define DataClass alias for BaseModel to reduce dependency on pydantic
DataClass = BaseModel


class DictLike(DataClass):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.__dict__.update(kwargs)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DictLike":
        return cls(**data)

    @classmethod
    def from_dataclass(cls, data: DataClass) -> "DictLike":
        return cls(**data.dict())

    def __getitem__(self, key: str) -> Any:
        return self.__dict__[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def pop(self, key: str) -> Any:
        return self.__dict__.pop(key)

    def keys(self):
        return self.__dict__.keys()
