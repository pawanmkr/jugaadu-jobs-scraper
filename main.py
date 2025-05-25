# ruff: noqa: T201
"""Main entry point for the job scraping application.

This module initializes the job scraping process, setting up database connections,
logging configuration, and command-line argument parsing. It orchestrates the
fetching and saving of job listings from naukri.com based on user-provided
search keywords.

Usage:
    python main.py -k "search_keyword"

Modules:
    - src.db.setup: Database setup and session management
    - src.logging_config: Logging configuration
    - src.process_jobs: Job scraping and saving functionality
    - src.repository.tracker: Job tracking functionality
"""

import argparse
import asyncio
import logging

from src.db.setup import AsyncSessionLocal, init_models
from src.logging_config import setup_logging
from src.process_jobs import fetch_and_save_jobs
from src.repository.tracker import get_last_tracker_by_keyword

logger = logging.getLogger(__name__)
DEFAULT_START_PAGE = 1


async def main() -> None:
    setup_logging()

    # Argument parsing
    parser = argparse.ArgumentParser(
        description="Job scraper configuration - Only naukri.com is supported yet",
    )
    parser.add_argument("-k", type=str, required=True, help="Search keyword for jobs")
    parser.add_argument(
        "-s",
        type=int,
        default=1,
        help="""Start page for scraping (default: 1). If not specified,
                it will use the last fetched page from DB if available.""",
    )
    parser.add_argument(
        "-max",
        type=int,
        default=1000,
        help="""Maximum number of jobs to fetch (default: 1000).
                20 jobs per page, so 1000/20 = 50 pages.""",
    )
    args = parser.parse_args()

    await init_models()

    keyword = args.k
    start_page = args.s
    max_jobs_to_fetch = args.max

    if not start_page > DEFAULT_START_PAGE:
        async with AsyncSessionLocal() as session:
            tracker = await get_last_tracker_by_keyword(session, keyword)
            if tracker:
                start_page = tracker.offset
                logger.info(
                    "🔍 Found previously fetched page number %s for %s\n",
                    start_page,
                    keyword,
                )
            else:
                start_page = 1

    end_page: int = start_page + round(max_jobs_to_fetch / 20)

    while True:
        print(
            f"Your input: "
            f"keyword='{keyword} "
            f"start_page={start_page} "
            f"max_jobs_to_fetch={max_jobs_to_fetch}",
        )
        print(
            f"It will collect {(end_page - start_page) * 20} '{keyword}' jobs from page"
            f" {start_page} - {end_page}",
        )
        print()

        consent = input("Do you want to proceed? (y/n) 🤔: ").strip().lower()

        if consent == "y":
            print("🏃🏻‍➡️ Proceeding", end="", flush=True)
            for _ in range(3):
                await asyncio.sleep(1)
                print(".", end="", flush=True)

            print()  # move to nxt line after proceeding...
            await fetch_and_save_jobs(
                keyword=keyword,
                start_page=start_page,
                end_page=end_page,
            )
            break
        if consent == "n":
            print("❌ Operation cancelled.")
            break
        print("⚠️ Please enter 'y' for yes or 'n' for no.")


if __name__ == "__main__":
    asyncio.run(main())
