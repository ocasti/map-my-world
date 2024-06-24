"""DB models"""

from geoalchemy2 import Geometry
from sqlalchemy import String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


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
