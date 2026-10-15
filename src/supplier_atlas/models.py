"""Strict transport contracts; category-specific vocabulary comes from the catalog."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class Predicate(StrictModel):
    field: str = Field(min_length=1, max_length=100)
    op: Literal["eq", "lt", "lte", "gt", "gte"] = "eq"
    value: float | str | bool
    unit: str | None = Field(default=None, max_length=30)


class TableQuery(StrictModel):
    schema_id: str
    filters: list[Predicate] = Field(default_factory=list, max_length=12)


class SearchRequest(StrictModel):
    category: str
    text: str = Field(default="", max_length=200)
    properties: list[Predicate] = Field(default_factory=list, max_length=12)
    table: TableQuery | None = None
    fields: list[str] = Field(default_factory=list, max_length=16)
    limit: int = Field(default=10, ge=1, le=50)
    cursor: str | None = Field(default=None, max_length=4000)


class TableRequest(StrictModel):
    table_id: str
    columns: list[str] | None = Field(default=None, min_length=1, max_length=24)
    filters: list[Predicate] = Field(default_factory=list, max_length=12)
    limit: int = Field(default=20, ge=1, le=100)
    cursor: str | None = Field(default=None, max_length=4000)


class GetRequest(StrictModel):
    ids: list[str] = Field(min_length=1, max_length=5)
    fields: list[str] | None = Field(default=None, max_length=24)
    tables: list[TableRequest] = Field(default_factory=list, max_length=3)
    include_sources: bool = False


class DiscoverRequest(StrictModel):
    category: str | None = None
    schema_id: str | None = None
    limit: int = Field(default=20, ge=1, le=50)
    cursor: str | None = Field(default=None, max_length=4000)

