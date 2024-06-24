from abc import abstractmethod
from collections.abc import Iterable

from pydantic import BaseModel
from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app.api.models import LocationPayload
from app.models import Category, Location


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
        create_data = self.get_create_data_from_payload(payload)
        item = self.model(**create_data)

        self._session.add(item)
        self._session.commit()
        self._session.refresh(item)
        return item

    def update(self, payload: BaseModel, item):
        update_data = self.get_update_data_from_payload(payload)

        stmt = update(self.model).where(self.model.id == item.id).values(**update_data)

        self._session.execute(stmt)
        self._session.commit()
        self._session.refresh(item)
        return item

    def delete(self, item):
        self._session.delete(item)
        self._session.commit()

    def get_create_data_from_payload(self, payload: BaseModel) -> dict:
        return payload.model_dump()

    def get_update_data_from_payload(self, payload: BaseModel) -> dict:
        return payload.model_dump(exclude_unset=True)


class CategoryCrud(Crud):
    @property
    def model(self):
        return Category


class LocationCrud(Crud):
    @property
    def model(self):
        return Location

    def get_create_data_from_payload(self, payload: LocationPayload) -> dict:
        data = payload.model_dump()
        return data | {"coordinate": payload.point_coordinate}

    def get_update_data_from_payload(self, payload: LocationPayload) -> dict:
        data = payload.model_dump()
        return data | {"coordinate": payload.point_coordinate}
