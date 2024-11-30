from pydantic import BaseModel
from typing import List, TypeVar, Generic, Union

# PaginationMeta contains all information about current page when a response is paginated
class PaginationMeta(BaseModel):
    page: int
    limit: int
    total: int
    first_page: int
    last_page: int
    previous_page: Union[int, None]
    next_page: Union[int, None]


T = TypeVar('T')

# PaginationResponse contains both the metadata and the data that consists of an array of objects
class PaginationResponse(BaseModel, Generic[T]):
    meta: PaginationMeta
    data: List[T]
