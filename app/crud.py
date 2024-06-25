from abc import abstractmethod
from collections.abc import Iterable

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select, text, update
from sqlalchemy.orm import Session

from app.api.models import CreateReviewPayload, LocationPayload
from app.models import Category, Location, Review


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


class ReviewCrud(Crud):
    @property
    def model(self):
        return Review

    def get_list(self, skip: int = 0, limit: int = 25) -> Iterable:
        sql = text(
            "SELECT lcr.id, lcr.reviewed_date, lcr.score, "
            "c.id as category_id, l.id as location_id "
            "FROM categories c "
            "CROSS JOIN locations l "
            "LEFT JOIN location_category_reviewed lcr "
            "ON c.id = lcr.category_id AND l.id = lcr.location_id "
            # Sort To return first no reviewed, next old reviewed
            "ORDER BY lcr.reviewed_date ASC, "
            "c.id ASC, l.id ASC "
            f"LIMIT {limit} "
            f"OFFSET {skip} "
        )
        data = self._session.execute(sql)
        return (
            Review(
                id=row[0],
                reviewed_date=row[1],
                score=row[2],
                category_id=row[3],
                location_id=row[4],
            )
            for row in data
        )

    def create(self, payload: CreateReviewPayload):
        self._valid_create(payload=payload)

        create_data = self.get_create_data_from_payload(payload)
        item = self.model(**create_data)

        self._session.add(item)
        self._session.commit()
        self._session.refresh(item)
        return item

    def _valid_create(self, payload: CreateReviewPayload) -> None:
        category = self._get_category(category_id=payload.category_id)
        if not category:
            raise HTTPException(status_code=400, detail="Category not found")

        location = self._get_location(location_id=payload.location_id)
        if not location:
            raise HTTPException(status_code=400, detail="Location not found")

        exists = self._get_review_exists(
            category_id=category.id, location_id=location.id
        )
        if exists:
            raise HTTPException(status_code=400, detail="Review exists")

    def _get_category(self, category_id: int) -> Category | None:
        stmt = select(Category).where(Category.id == category_id)
        category = self._session.scalars(stmt).first()
        return category

    def _get_location(self, location_id: int) -> Location | None:
        stmt = select(Location).where(Location.id == location_id)
        location = self._session.scalars(stmt).first()
        return location

    def _get_review_exists(self, category_id: int, location_id: int) -> Review | None:
        stmt = (
            select(Review.id)
            .where(Review.category_id == category_id)
            .where(Review.location_id == location_id)
        )
        exists = self._session.scalars(stmt).first()
        return exists
