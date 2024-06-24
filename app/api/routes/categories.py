from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def read_categories():
    """Retrieve categories."""
    return "categories"
