from datetime import datetime

from sqlalchemy import Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    # Auto-generate __tablename__ if not defined
    @declared_attr
    def __tablename__(self, cls) -> str:
        return cls.__name__.lower()


class BaseModel(Base):
    __abstract__ = True  # Prevents this from becoming a real table

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())
