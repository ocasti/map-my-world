from abc import abstractmethod
from collections.abc import Iterable

from pydantic import BaseModel
from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app.models import Category


class Crud:
    def __init__(self, session: Session) -> None:
        self._session = session

    @property
    @abstractmethod
    def model(self): ...

    def get_count(self) -> int:
        count_stmt = func.count(self.model.id)
        count = self._session.scalars(count_stmt).first()
        return count

    def get_list(self, skip: int = 0, limit: int = 25) -> Iterable:
        stmt = select(self.model).offset(skip).limit(limit)
        data = self._session.scalars(stmt)
        return data

    def get_detail(self, id: int):
        stmt = select(self.model).where(self.model.id == id)
        item = self._session.scalars(stmt).first()
        return item

    def create(self, payload: BaseModel):
        item = self.model(**payload.model_dump())

        self._session.add(item)
        self._session.commit()
        self._session.refresh(item)
        return item

    def update(self, payload: BaseModel, item):
        update_data = payload.model_dump(exclude_unset=True)

        stmt = update(self.model).where(self.model.id == item.id).values(**update_data)

        self._session.execute(stmt)
        self._session.commit()
        self._session.refresh(item)
        return item

    def delete(self, item):
        self._session.delete(item)
        self._session.commit()


class CategoryCrud(Crud):
    @property
    def model(self):
        return Category
