import asyncio
import logging
import random
import time
from typing import Callable  # noqa: UP035

logger = logging.getLogger(__name__)

# avoid ip-block by naukri.com using breaks
def take_a_break(i: int):
    if i % 3 == 0:
        delay = random.uniform(5, 10)
        print(f"[WAIT] Longer pause: {delay:.2f} seconds")
        time.sleep(delay)
    else:
        delay = random.uniform(2, 5)
        print(f"[WAIT] Sleeping for {delay:.2f} seconds...")
        time.sleep(delay)


async def retry_with_backoff(fn: Callable, retries: int = 5):
    for attempt in range(retries):
        try:
            return await fn()
        except Exception as e:
            wait = 2 ** attempt + random.uniform(0.5, 1.5)
            logger.warning(f"[RETRY] Attempt {attempt+1}/{retries} failed: {e}. Retrying in {wait:.2f}s")
            await asyncio.sleep(wait)
    raise Exception(f"[FAILURE] All {retries} retry attempts failed.")
