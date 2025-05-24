from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String

class Base(DeclarativeBase):
    pass

class Naukri(Base):
    __tablename__ = 'naukri'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    original_job_id: Mapped[int] = mapped_column(unique=True)
    company_id: Mapped[int] = mapped_column()
    company_name: Mapped[str] = mapped_column()
    skills: Mapped[str] = mapped_column()
    jd_url: Mapped[str] = mapped_column()
    static_url: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    created_date: Mapped[str] = mapped_column()
    mode: Mapped[str] = mapped_column()
    experience: Mapped[str] = mapped_column()
    vacancy: Mapped[int] = mapped_column()
