"""API models"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from .category import CategoryPublic
from .locations import LocationPublic


class DetailReviewPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    score: int
    reviewed_date: datetime
    location: LocationPublic
    category: CategoryPublic


class ReviewPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None
    score: int | None
    reviewed_date: datetime | None
    location_id: int
    category_id: int


class ReviewsPublic(BaseModel):
    data: list[ReviewPublic]
    count: int


class Payload(BaseModel):
    score: int = Field(min=0, max=5)


class CreateReviewPayload(Payload):
    location_id: int = Field(min=1)
    category_id: int = Field(min=1)


class UpdateReviewPayload(Payload): ...
