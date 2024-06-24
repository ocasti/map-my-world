from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.db import engine
from app.crud import CategoryCrud


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


def get_category_crud(session: SessionDep) -> CategoryCrud:
    return CategoryCrud(session=session)


CategoryCrudDep = Annotated[CategoryCrud, Depends(get_category_crud)]
