from pydantic import BaseModel, Field
from pydantic_mongo import PydanticObjectId
from typing import List


class Movie(BaseModel):
    # TODO: Add fields
    id: PydanticObjectId = Field(alias="_id")
    title: str = Field(...)
    cast: List[str] = Field(...)
