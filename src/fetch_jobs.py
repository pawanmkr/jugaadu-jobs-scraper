import logging

from src.db.setup import AsyncSessionLocal
from src.request_naukri import safe_naukri_request
from src.repository.naukri import create_naukri
from src.repository.tracker import create_tracker
from src.utils import take_a_break

logger = logging.getLogger(__name__)

async def fetch_jobs(keyword: str, start_page: int = 1, end_page: int = 100):
    total_jobs_collected = 0
    exception_occured = False
    
    async with AsyncSessionLocal() as session:
        for offset in range(start_page, end_page):
            try:
                response = await safe_naukri_request(keyword, offset)
                
                if response.status_code == 200:
                    logger.info("Jobs fetched successfully, page: %s", offset)
                    
                    job_list = response.json().get('jobDetails', [])

                    if not isinstance(job_list, list):
                        raise ValueError("jobDetails is missing or not a list")

                    for job in job_list:
                        try:
                            await create_naukri(session, job, keyword=keyword)
                        except Exception as e:
                            raise Exception(f"[DATABASE ERROR] {e}")

                    total_jobs_collected += len(job_list)
                    logger.debug("Collected %d jobs", total_jobs_collected)
                    
                    take_a_break(offset)
                else:
                    raise Exception(f"[NAUKRI] Error fetching jobs, Got: {response.status_code} with Reason - {response.text}")
                
            except Exception as e:
                logger.error("Error fetching jobs: %s", e)
                exception_occured = True

            finally:                
                # ✅ After total_jobs_collected and reached end_page
                if offset == end_page - 1:
                    await create_tracker(session, keyword, offset + 1, total_jobs_collected)
                    
                # when error/exception occurred 
                elif exception_occured:
                    await create_tracker(session, keyword, offset, total_jobs_collected)
                    break
