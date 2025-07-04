from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.tracker import Tracker


async def create_tracker(
    db: AsyncSession,
    keyword: str,
    offset: int,
    total_jobs_collected: int,
) -> Tracker:
    tracker = Tracker(
        keyword=keyword, offset=offset, total_jobs_collected=total_jobs_collected
    )
    db.add(tracker)
    await db.commit()
    await db.refresh(tracker)
    return tracker


async def get_last_tracker_by_keyword(db: AsyncSession, keyword: str) -> Tracker | None:
    subq = (
        select(func.max(Tracker.offset))
        .where(Tracker.keyword == keyword)
        .scalar_subquery()
    )
    stmt = select(Tracker).where(Tracker.keyword == keyword, Tracker.offset == subq)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_all_trackers_by_keyword(db: AsyncSession, keyword: str) -> Tracker | None:
    tracker = await db.execute(select(Tracker).where(Tracker.keyword == keyword))
    return tracker.scalars().all()
