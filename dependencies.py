from typing import Annotated

from fastapi import Depends, Query
from pydantic import BaseModel



class PaginationParams(BaseModel):

    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None,Query(3, ge=1, lt=20)]


PaginationDep = Annotated[PaginationParams, Depends()]

# можно реализовать иначе, без использования депендс
# вот пример из доки
# class FilterParams(BaseModel):
#     model_config = {"extra": "forbid"}
#
#     limit: int = Field(100, gt=0, le=100)
#     offset: int = Field(0, ge=0)
#     order_by: Literal["created_at", "updated_at"] = "created_at"
#     tags: list[str] = []
#
#
# @app.get("/items/")
# async def read_items(filter_query: Annotated[FilterParams, Query()]):
#     return filter_query