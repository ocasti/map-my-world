"""DB models"""

from datetime import UTC, datetime

from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()


def utcnow() -> datetime:
    return datetime.now(UTC)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(45))

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name={self.name})"


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(45))
    latitude: Mapped[float] = mapped_column()
    longitude: Mapped[float] = mapped_column()
    coordinate = mapped_column(Geometry("POINT"))

    def __repr__(self) -> str:
        return f"Location(id={self.id}, name={self.name})"


class Review(Base):
    __tablename__ = "location_category_reviewed"

    id: Mapped[int] = mapped_column(primary_key=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    reviewed_date: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
    score: Mapped[int] = mapped_column()

    location: Mapped[Location] = relationship()
    category: Mapped[Category] = relationship()

    def __repr__(self) -> str:
        return (
            f"Review(id={self.id}, "
            f"location_id={self.location_id}, category_id={self.category_id})"
        )
