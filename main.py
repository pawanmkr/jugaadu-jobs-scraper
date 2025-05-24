import asyncio

from src.db.setup import init_models
from src.fetch_jobs import fetch_jobs
from src.logging_config import setup_logging


async def main():
    setup_logging()
    await init_models()
    await fetch_jobs(keyword="node js developer", start_page=1, end_page=2)


if __name__ == "__main__":
    asyncio.run(main())
    