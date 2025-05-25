"""Module for processing and saving jobs from Naukri API.

This module provides functionality to:
- Fetch job listings from Naukri API
- Process and validate job data
- Save jobs to the database
- Track scraping progress
"""

import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.setup import AsyncSessionLocal
from src.exceptions.database import DatabaseWriteError
from src.exceptions.http import NotOkError
from src.repository.naukri import create_naukri
from src.repository.tracker import create_tracker
from src.request_naukri import safe_naukri_request
from src.utils import take_a_break

logger = logging.getLogger(__name__)
OK = 200
DATABASE_ERROR_PREFIX = "[DATABASE ERROR]"


async def process_page_jobs(session: AsyncSession, keyword: str, offset: int) -> int:
    response = await safe_naukri_request(keyword, offset)

    if response.status_code != OK:
        raise NotOkError(response.status_code, response.text)

    # Try parsing the response JSON
    try:
        data = response.json()
    except ValueError as e:
        msg = f"Invalid JSON response on page {offset}: {e}"
        raise ValueError(msg) from e

    # Extract job list and validate its type
    job_list = data.get("jobDetails", [])
    if not isinstance(job_list, list):
        msg = "jobDetails is missing or not a list"
        raise TypeError(msg)

    # Save each job in the database
    for job in job_list:
        try:
            await create_naukri(session, job, keyword=keyword)
        except SQLAlchemyError as e:
            msg = DATABASE_ERROR_PREFIX + " Failed to create naukri"
            raise DatabaseWriteError(msg, e) from e

    return len(job_list)


async def save_tracker(
    session: AsyncSession, keyword: str, offset: int, total: int
) -> None:
    try:
        await create_tracker(session, keyword, offset, total)
        logger.info(
            "Tracker saved: keyword='%s', offset=%d, total_jobs_collected=%d",
            keyword,
            offset,
            total,
        )
    except SQLAlchemyError as e:
        msg = DATABASE_ERROR_PREFIX + " Failed to create tracker"
        raise DatabaseWriteError(msg, e) from e


async def fetch_and_save_jobs(
    keyword: str, start_page: int = 1, end_page: int = 100
) -> None:
    total_jobs_collected = 0  # Tracks total jobs added during this run
    offset = start_page - 1  # Initialized before the loop
    completed_normally = True  # Flag to determine if loop ran successfully

    async with AsyncSessionLocal() as session:
        try:
            for offset in range(start_page, end_page):
                try:
                    # Process jobs from the current page
                    jobs_this_page = await process_page_jobs(session, keyword, offset)
                    total_jobs_collected += jobs_this_page

                    logger.debug(
                        "\nFound %d jobs on page %d and total is %d",
                        jobs_this_page,
                        offset,
                        total_jobs_collected,
                    )

                    take_a_break(
                        offset
                    )  # Respectful pause to avoid rate limiting / being blocked

                except Exception:
                    # On any per-page error (bad response, DB error, etc.),
                    # stop processing further
                    logger.exception("🚨 Error fetching jobs at page %s", offset)
                    completed_normally = False
                    break

        except BaseException:
            # Handles manual interrupts (KeyboardInterrupt) or fatal crashes
            logger.exception("🚫 Interrupted or fatal error")
            completed_normally = False
            raise  # Important: propagate for higher-level shutdown handling

        finally:
            # Decide where the tracker should resume from
            # If loop completed, resume from the next page;
            # otherwise, retry current offset later
            tracker_offset = offset + 1 if completed_normally else offset

            # Save progress in tracker
            if total_jobs_collected != 0:
                await save_tracker(
                    session, keyword, tracker_offset, total_jobs_collected
                )
                logger.info("🗣️ Done and dusted! Time for a break.")
