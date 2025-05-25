from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.base import BaseModel, TimestampMixin


class Naukri(BaseModel, TimestampMixin):
    __tablename__ = "naukri"

    keyword: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    original_job_id: Mapped[int] = mapped_column(nullable=False)
    company_id: Mapped[int] = mapped_column(nullable=True)
    company_name: Mapped[str] = mapped_column(nullable=True)
    skills: Mapped[str] = mapped_column(nullable=True)
    jd_url: Mapped[str] = mapped_column(nullable=True)
    static_url: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    posted_on: Mapped[str] = mapped_column(nullable=True)
    mode: Mapped[str] = mapped_column(nullable=True)
    experience: Mapped[str] = mapped_column(nullable=True)
    vacancy: Mapped[int] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        """Return the string based representation of naukri fields for devs."""
        return (
            f"Naukri(id={self.id}, title={self.title}, posted_on={self.posted_on}, "
            f"experience={self.experience}, vacancy={self.vacancy})"
        )
