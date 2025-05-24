from urllib.parse import quote

import requests
from src.utils import retry_with_backoff


def make_naukri_request(keyword: str, offset: int):
    base_url = 'https://www.naukri.com/jobapi/v3/search'
    limit = 20 # max is 20
    encoded_keyword = quote(keyword)
    seo_key = f"{keyword.replace(' ', '-')}-jobs"
    url = f"{base_url}?noOfResults={limit}&urlType=search_by_keyword&searchType=adv&keyword={encoded_keyword}&pageNo={offset}&k={encoded_keyword}&seoKey={seo_key}&src=jobsearchDesk"

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
    
    return requests.get(url, headers=headers)


async def safe_naukri_request(keyword, offset):
    return await retry_with_backoff(lambda: make_naukri_request(keyword, offset))
