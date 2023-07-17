from __future__ import annotations

from typing import Any

from pydantic import BaseModel

# NOTE: Define BaseModel alias for BaseModel to reduce dependency on pydantic


class DataClass(BaseModel):
    def dict(self) -> dict[str, Any]:
        return super().model_dump()

    # TODO(zawakin): Replace `model_copy` with the following methods.
    # def copy(self) -> DataClass:
    #     return super().model_copy(deep=True)
    # def update(self: Model, **kwargs: Any) -> Model:
    #     return super().model_copy(deep=True, update=kwargs)
    pass
