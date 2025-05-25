from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.datatypes.job import Job
from src.db.models.naukri import Naukri


async def create_naukri(db: AsyncSession, job: Job, keyword: str) -> Naukri:
    naukri = Naukri(
        keyword=keyword,
        title=job.get("title"),
        original_job_id=job.get("jobId"),
        company_id=job.get("companyId"),
        company_name=job.get("companyName"),
        skills=job.get("tagsAndSkills"),
        jd_url=job.get("jdURL"),
        static_url=job.get("staticUrl"),
        description=job.get("jobDescription"),
        posted_on=job.get("createdDate"),
        mode=job.get("mode"),
        experience=job.get("experienceText"),
        vacancy=job.get("vacancy"),
    )

    db.add(naukri)
    await db.commit()
    await db.refresh(naukri)
    return naukri


async def get_naukri_by_id(db: AsyncSession, id: int) -> Naukri | None:
    result = await db.execute(select(Naukri).where(Naukri.id == id))
    return result.scalar_one_or_none()


async def get_naukri_by_keyword(db: AsyncSession, keyword: str) -> list[Naukri]:
    result = await db.execute(select(Naukri).where(Naukri.keyword == keyword))
    return result.scalars().all()
