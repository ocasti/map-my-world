from fastapi import APIRouter

from app.api.routes.categories import router as categories_router
from app.api.routes.locations import router as locations_router
from app.api.routes.reviews import router as reviews_router

api_router = APIRouter()
api_router.include_router(categories_router, prefix="/categories", tags=["categories"])
api_router.include_router(locations_router, prefix="/locations", tags=["locations"])
api_router.include_router(reviews_router, prefix="/reviews", tags=["reviews"])
