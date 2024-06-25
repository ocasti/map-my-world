from collections.abc import Iterable

from fastapi import APIRouter, HTTPException

from app.api.depends import ReviewCrudDep
from app.api.models import (
    CreateReviewPayload,
    DetailReviewPublic,
    Message,
    ReviewsPublic,
    UpdateReviewPayload,
)
from app.models import Review

router = APIRouter()


@router.get("/", response_model=ReviewsPublic)
def read_reviews(crud: ReviewCrudDep, skip: int = 0, limit: int = 25) -> ReviewsPublic:
    """Retrieve reviews."""
    count = crud.get_count()
    reviews: Iterable[Review] = crud.get_list(skip=skip, limit=limit)

    return ReviewsPublic(
        data=reviews,
        count=count,
    )


@router.get("/{id}", response_model=DetailReviewPublic)
def read_review(crud: ReviewCrudDep, id: int):
    """Get review by ID"""
    review: Review = crud.get_detail(id=id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.post("/", response_model=DetailReviewPublic)
def create_review(crud: ReviewCrudDep, payload: CreateReviewPayload):
    """Create new review."""
    review = crud.create(payload=payload)
    return review


@router.put("/{id}", response_model=DetailReviewPublic)
def update_review(crud: ReviewCrudDep, id: int, payload: UpdateReviewPayload):
    """Update a review."""
    review: Review = crud.get_detail(id=id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    review = crud.update(payload=payload, item=review)
    return review


@router.delete("/{id}")
def delete_review(crud: ReviewCrudDep, id: int) -> Message:
    """Delete a review."""
    review: Review = crud.get_detail(id=id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    crud.delete(item=review)
    return Message(message="Review deleted")
