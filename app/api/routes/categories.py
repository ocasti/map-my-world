from collections.abc import Iterable

from fastapi import APIRouter, HTTPException

from app.api.depends import CategoryCrudDep
from app.api.models import CategoriesPublic, CategoryPayload, CategoryPublic, Message
from app.models import Category

router = APIRouter()


@router.get("/", response_model=CategoriesPublic)
def read_categories(
    crud: CategoryCrudDep, skip: int = 0, limit: int = 25
) -> CategoriesPublic:
    """Retrieve categories."""
    count = crud.get_count()
    categories: Iterable[Category] = crud.get_list(skip=skip, limit=limit)

    return CategoriesPublic(
        data=categories,
        count=count,
    )


@router.get("/{id}", response_model=CategoryPublic)
def read_category(crud: CategoryCrudDep, id: int):
    """Get category by ID"""
    category: Category = crud.get_detail(id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryPublic)
def create_category(crud: CategoryCrudDep, payload: CategoryPayload):
    """Create new category."""
    category = crud.create(payload=payload)
    return category


@router.put("/{id}", response_model=CategoryPublic)
def update_category(crud: CategoryCrudDep, id: int, payload: CategoryPayload):
    """Update a category."""
    category: Category = crud.get_detail(id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = crud.update(payload=payload, item=category)
    return category


@router.delete("/{id}")
def delete_category(crud: CategoryCrudDep, id: int) -> Message:
    """Delete a category."""
    category: Category = crud.get_detail(id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    crud.delete(item=category)
    return Message(message="Category deleted")
