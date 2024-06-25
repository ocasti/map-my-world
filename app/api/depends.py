from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.db import engine
from app.crud import CategoryCrud, LocationCrud, ReviewCrud


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


def get_category_crud(session: SessionDep) -> CategoryCrud:
    return CategoryCrud(session=session)


def get_location_crud(session: SessionDep) -> LocationCrud:
    return LocationCrud(session=session)


def get_review_crud(session: SessionDep) -> ReviewCrud:
    return ReviewCrud(session=session)


CategoryCrudDep = Annotated[CategoryCrud, Depends(get_category_crud)]
LocationCrudDep = Annotated[LocationCrud, Depends(get_location_crud)]
ReviewCrudDep = Annotated[ReviewCrud, Depends(get_review_crud)]
