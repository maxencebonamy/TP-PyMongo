from models.pagination import PaginationResponse, PaginationMeta
from typing import Union, Any
from models.movie import Movie


def paginate(collection: Any, query: Any, page: Union[str, None], limit: Union[str, None]) -> PaginationResponse[Movie]:
    # default page and limit values
    page = int(page) if page else 1
    limit = int(limit) if limit else 10
    # convert page to skip value, which is easier to use with MongoDB
    skip = (page - 1) * limit

    # get the data and total count of documents
    data = collection.find(query).skip(skip).limit(limit)
    total = collection.count_documents(query)

    # calculate the last page, previous page and next page for pagination metadata
    last_page = (total + limit - 1) // limit
    previous_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < last_page else None

    # create the PaginationMeta and PaginationResponse objects
    meta = PaginationMeta(
        page=page,
        limit=limit,
        total=total,
        first_page=1,
        last_page=last_page,
        previous_page=previous_page,
        next_page=next_page
    )
    return PaginationResponse(data=data, meta=meta)
