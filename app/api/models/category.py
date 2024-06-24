"""API models"""

from pydantic import BaseModel, ConfigDict, Field


class CategoryPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class CategoriesPublic(BaseModel):
    data: list[CategoryPublic]
    count: int


class CategoryPayload(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=3, max_length=45)
