from sqlalchemy.orm import Mapped, mapped_column
from src.db.models.base import BaseModel, TimestampMixin


class Naukri(BaseModel, TimestampMixin):
    __tablename__ = "naukri"
    
    keyword: Mapped[str] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    original_job_id: Mapped[int] = mapped_column(nullable=False)
    company_id: Mapped[int] = mapped_column()
    company_name: Mapped[str] = mapped_column()
    skills: Mapped[str] = mapped_column()
    jd_url: Mapped[str] = mapped_column()
    static_url: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    posted_on: Mapped[str] = mapped_column()
    mode: Mapped[str] = mapped_column()
    experience: Mapped[str] = mapped_column()
    vacancy: Mapped[int] = mapped_column()
    
    def __repr__(self):
        return f"Naukri(id={self.id}, title={self.title}, posted_on={self.posted_on}, experience={self.experience}, vacancy={self.vacancy})"