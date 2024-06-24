from collections.abc import Iterable

from fastapi import APIRouter, HTTPException

from app.api.depends import LocationCrudDep
from app.api.models import LocationPayload, LocationPublic, LocationsPublic, Message
from app.models import Location

router = APIRouter()


@router.get("/", response_model=LocationsPublic)
def read_locations(
    crud: LocationCrudDep, skip: int = 0, limit: int = 25
) -> LocationsPublic:
    """Retrieve locations."""
    count = crud.get_count()
    locations: Iterable[Location] = crud.get_list(skip=skip, limit=limit)

    return LocationsPublic(
        data=locations,
        count=count,
    )


@router.get("/{id}", response_model=LocationPublic)
def read_location(crud: LocationCrudDep, id: int):
    """Get location by ID"""
    location: Location = crud.get_detail(id=id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.post("/", response_model=LocationPublic)
def create_location(crud: LocationCrudDep, payload: LocationPayload):
    """Create new location."""
    location = crud.create(payload=payload)
    return location


@router.put("/{id}", response_model=LocationPublic)
def update_location(crud: LocationCrudDep, id: int, payload: LocationPayload):
    """Update a location."""
    location: Location = crud.get_detail(id=id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    location = crud.update(payload=payload, item=location)
    return location


@router.delete("/{id}")
def delete_location(crud: LocationCrudDep, id: int) -> Message:
    """Delete a location."""
    location: Location = crud.get_detail(id=id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    crud.delete(item=location)
    return Message(message="Location deleted")
