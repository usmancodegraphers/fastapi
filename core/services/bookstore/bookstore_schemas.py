from pydantic import BaseModel
from typing import List


class AuthorSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class BookSchema(BaseModel):
    id: int
    title: str
    authors: List[AuthorSchema]

    class Config:
        from_attributes = True
