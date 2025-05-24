import time
import random
import requests
from datatypes.job import Job
from typing import List
from urllib.parse import quote

jobs: List[Job] = []

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

for i in range(2):
    base_url = 'https://www.naukri.com/jobapi/v3/search'
    limit = 20 # max is 20
    offset = i + 1
    keyword = 'node js developer'
    encoded_keyword = quote(keyword)
    seo_key = f"{keyword.replace(' ', '-')}-jobs"
    url = f"{base_url}?noOfResults={limit}&urlType=search_by_keyword&searchType=adv&keyword={keyword}&pageNo={offset}&k={keyword}&seoKey={seo_key}&src=jobsearchDesk"

    headers = {
        "accept": "application/json",
        "accept-language": "en-GB",
        "appid": "109",
        "clientid": "d3skt0p",
        "content-type": "application/json",
        "gid": "LOCATION,INDUSTRY,EDUCATION,FAREA_ROLE",
        "nkparam": "bFSngPweFuTcgMtIrloaZlT3doFW5owslzaYYRvpToNeVshGOteA5ZQRjl7yY1vQkJaXT8XJzC56jM5adaun7A==",
        "sec-ch-ua": '"Not(A:Brand";v="24", "Chromium";v="122"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "systemid": "Naukri",
        "cookie": "YOUR_FULL_COOKIE_STRING_HERE",
        "Referer": "https://www.naukri.com/node-js-developer-jobs?k=node%20js%20developer",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }   

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("[NAUKRI] Jobs found sucessfully")
        
    data = response.json()
        
    if isinstance(data, dict):
        jobs.extend(data.get('jobDetails', []))
        
    take_a_break(i)
        
print(f"[NAUKRI] Found {len(jobs)} jobs")





# TODO: save the data first in sqlite





    #     print("\nJOB INFO")
    #     for job in jobs:
    #         print(
    #             f"""--------------------------------------------------------------------------------------------------
    #               Title       : {job.get('title')}
    #               Job ID      : {job.get('jobId')}
    #               Company ID  : {job.get('companyId')}
    #               Company     : {job.get('companyName')}
    #               Skills      : {job.get('tagsAndSkills')}
    #               JD URL      : {job.get('jdURL')[:25]}...
    #               Static URL  : {job.get('staticUrl')}
    #               Description : {job.get('jobDescription', '')[:50]}...
    #               Posted On   : {job.get('createdDate')}
    #               Mode        : {job.get('mode')}
    #               Experience  : {job.get('experienceText')}
    #               Vacancy     : {job.get('vacancy', 'N/A')}"""
    #         )