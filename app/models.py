"""DB models"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(45))

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name={self.name})"
