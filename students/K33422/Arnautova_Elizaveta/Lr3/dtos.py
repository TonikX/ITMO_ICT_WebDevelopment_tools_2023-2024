from pydantic import BaseModel
from typing import List, Optional


class AuthorDTO(BaseModel):
    id: int
    name: str
    author_url: Optional[str]

    class Config:
        from_attributes = True


class UpdateAuthorDTO(BaseModel):
    name: Optional[str]
    author_url: Optional[str]

    class Config:
        from_attributes = True


class CategoryDTO(BaseModel):
    id: int
    name: str
    url: Optional[str]

    class Config:
        from_attributes = True


class UpdateCategoryDTO(BaseModel):
    name: Optional[str]
    url: Optional[str]

    class Config:
        from_attributes = True


class TitleDTO(BaseModel):
    id: int
    url: str
    title: str
    ingredients: int
    servings: int
    cook_time: Optional[str]
    author_id: int
    cur_url: Optional[str]
    author: Optional[AuthorDTO]  # Nested schema
    categories: List[CategoryDTO] = []  # Nested schema

    class Config:
        from_attributes = True


class UpdateTitleDTO(BaseModel):
    url: Optional[str]
    title: Optional[str]
    ingredients: Optional[int]
    servings: Optional[int]
    cook_time: Optional[str]
    author_id: Optional[int]
    cur_url: Optional[str]
    category_ids: Optional[List[int]]

    class Config:
        from_attributes = True


class TitleOutputDTO(BaseModel):
    id: int
    url: str
    title: str
    ingredients: int
    servings: int
    cook_time: Optional[str]
    cur_url: Optional[str]
    author: Optional[AuthorDTO]
    categories: List[CategoryDTO] = []

    class Config:
        from_attributes = True
