from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_locations():
    """Retrieve locations."""
    return "locations"
