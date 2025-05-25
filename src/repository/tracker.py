from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.tracker import Tracker


async def create_tracker(db: AsyncSession, keyword: str, offset: int, total_jobs_collected: int) -> Tracker:
    tracker = Tracker(keyword=keyword, offset=offset, total_jobs_collected=total_jobs_collected)
    db.add(tracker)
    await db.commit()
    await db.refresh(tracker)
    return tracker


async def get_tracker_by_keyword(db: AsyncSession, keyword: str) -> Tracker | None:
    tracker = await db.execute(select(Tracker).where(Tracker.keyword == keyword))
    return tracker.scalars().all()