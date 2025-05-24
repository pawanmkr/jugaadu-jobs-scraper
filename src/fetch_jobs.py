import logging

from src.db.setup import AsyncSessionLocal
from src.request_naukri import safe_naukri_request
from src.repository.naukri import create_naukri
from src.repository.tracker import create_tracker
from src.utils import take_a_break

logger = logging.getLogger(__name__)

async def fetch_jobs(keyword: str, start_page: int = 1, end_page: int = 100):
    total_jobs_collected = 0
    
    async with AsyncSessionLocal as session:
        for offset in range(start_page, end_page):
            try:
                response = await safe_naukri_request(keyword, offset)
                
                if response.status_code == 200:
                    logger.info("Jobs fetched successfully, page: %s", offset)
                    
                    job_list = response.json().get('jobDetails', [])

                    if not isinstance(job_list, list):
                        raise ValueError("jobDetails is missing or not a list")

                    for job in job_list:
                        await create_naukri(session, job, keyword=keyword)

                    total_jobs_collected += len(job_list)
                    logger.debug("Collected %d jobs", total_jobs_collected)
                    
                    take_a_break(offset)
                else:
                    raise Exception(f"[NAUKRI] Error fetching jobs, Got: {response.status_code} with Reason - {response.text}")
                
            except Exception as e:
                logger.error("Error fetching jobs: %s", e)
                
            finally:
                # ✅ After total_jobs_collected
                await create_tracker(session, keyword, offset, total_jobs_collected)
