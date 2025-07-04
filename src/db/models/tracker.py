from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.base import BaseModel, TimestampMixin


class Tracker(BaseModel, TimestampMixin):
    __tablename__ = "tracker"

    keyword: Mapped[str] = mapped_column(nullable=False)
    offset: Mapped[int] = mapped_column(nullable=False)
    total_jobs_collected: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        """Return the string representation of the tracker record for devs."""
        return (
            f"Tracker(id={self.id}, keyword={self.keyword}, offset={self.offset}, "
            f"total_jobs_collected={self.total_jobs_collected})"
        )
