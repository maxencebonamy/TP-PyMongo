from pydantic import BaseModel
from typing import List, TypeVar, Generic, Union


class PaginationMeta(BaseModel):
    page: int
    limit: int
    total: int
    first_page: int
    last_page: int
    previous_page: Union[int, None]
    next_page: Union[int, None]


T = TypeVar('T')


class PaginationResponse(BaseModel, Generic[T]):
    meta: PaginationMeta
    data: List[T]
