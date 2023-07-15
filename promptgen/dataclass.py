from __future__ import annotations

from typing import Any, Dict

from pydantic import BaseModel
from typing_extensions import TypeAlias

# NOTE: Define BaseModel alias for BaseModel to reduce dependency on pydantic
DataClass: TypeAlias = BaseModel
