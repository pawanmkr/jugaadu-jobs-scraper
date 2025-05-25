import asyncio
import logging
import secrets
import time
from typing import Callable  # noqa: UP035

logger = logging.getLogger(__name__)


# avoid ip-block by naukri.com using breaks
def take_a_break(i: int) -> None:
    if i % 3 == 0:
        # delay = random.uniform(5, 10)
        delay = secrets.randbelow(2)
        msg = f"⏱️ Longer pause: {delay:.2f} seconds"
        logger.info(msg)
        time.sleep(delay)
    else:
        # delay = random.uniform(2, 5)
        delay = secrets.randbelow(1)
        msg = f"⏱️ Sleeping for {delay:.2f} seconds..."
        logger.info(msg)
        time.sleep(delay)


async def retry_with_backoff(fn: Callable, retries: int = 5) -> None:
    for attempt in range(retries):
        try:
            return await fn()

        except Exception as e:
            wait = 2**attempt + secrets.randbelow(1)

            msg = f"🔄 Attempt {attempt}/{retries} failed: {e}. Retrying in {wait:.2f}s"
            logger.exception(msg)

            await asyncio.sleep(wait)

    msg = f"❌ All {retries} retry attempts failed."
    raise RuntimeError(msg)
