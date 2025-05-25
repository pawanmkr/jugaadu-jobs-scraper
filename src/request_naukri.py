# ruff: noqa: E501
from urllib.parse import quote

import httpx

from src.utils import retry_with_backoff


async def make_naukri_request(keyword: str, offset: int) -> httpx.Response:
    base_url = "https://www.naukri.com/jobapi/v3/search"
    limit = 20
    encoded_keyword = quote(keyword)
    seo_key = f"{keyword.replace(' ', '-')}-jobs"
    url = (
        f"{base_url}?noOfResults={limit}&urlType=search_by_keyword&searchType=adv"
        f"&keyword={encoded_keyword}&pageNo={offset}&k={encoded_keyword}&seoKey={seo_key}&src=jobsearchDesk"
    )

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
        "cookie": "test=naukri.com; _t_us=6830B140; _t_s=direct; _t_r=1030%2F%2F; persona=default; _t_ds=de6c1e51748021568-23de6c1e5-0de6c1e5; J=0; bm_mi=AA132C7F102724473BDF9A3290DF689D~YAAQf5xMF1bdUMeWAQAACDg1/hsEN1O/LaeT8AnNToMnnQKaDIpGyStkGcspy3VK8HdlBLa7a8qq7uo2UcAfVukanjwQB4dihZxz5fycsekRZqA+jwG+LABd1ngd+pPFNTZXleRKx1yjHZs3v07/stiX8ylLm70cokVfefEwK8IhEEiQSIJs20KGpmHIw9FXZ4cbixHx+qW98umL05fiylXywWw8EIPsLVQzEo/bU34fSJhFYDWYAQtHjGCBxG/SHeNx4E+PMPpg6ymGWgk5fTSNI5VlCXJNhiuf8/0eKj3VnWEv+/9ncXsHsm/CEiSQbf4B+XirOfJ2vOFGQgqLLNh25A==~1; bm_sv=D52FF7412E8AB15B063F6302DC0FD28E~YAAQf5xMF6zdUMeWAQAAED41/hv48JykMFxtotNwn6z1ft22EwkWHGti+ecHsUaaWtSf12i+pup6IIaRMCyT8LT410UKUkf2GJJK1Rbl1jKKjAOIvnd1ceSK0aAoGVUPxF28DrO+a93PcfzpyETlha7/zMKd3GCAbxUiS+7nqCkE5rLBvORrKPGTYwVt6c99KJgyg4diuaAzQ1vhJSXIXp+90iXiu87vPnnnN1ikz/9cyM0j30ihU6b+vS6Ei4fBrQ==~1; ak_bmsc=E8823672970E4D12D1301A1FAE4B345B~000000000000000000000000000000~YAAQf5xMF6DmUMeWAQAAvLQ1/hspqKKuEOsJoY43jOw67GKX7Mui5rIHsIbPrzut7Hun2wL5ld0QsdDdvsAVX113QWDeIjDda/okEj68DgqUYPfJoHwljEiPQEgrfLN0d9JlYyy2wDnDoYoUruVjDqeFVI4RRwS2rRro+sMAMSw9+KPUbKi5xhlp/rQ3XWwuZzYoC5jPlNAT9sxUQUgXBavRGvA1c7GAYVbQ2mfxjZQvtjViF7A4+h6ZEgEJW/5LrrxL0KhOMO+v5Iy9mCcn9Ew1xK/TGpmQIxLzlbJrsvRgHpEG5AYEl/jNFdj/r3LD649HpQUZZDLTTNNjIoODX4bVkdnqliKOFFxuUncfPwOnLx86JJJH94Y9cvF6NlRy64MVoWKo9SQ9/qJrDEU5pwvlPyDXNfYhGTx6QxuQU/RHola0kY+l9QktWRhXgTXtuNcIwMPgUsx945Ce/dMWJLnD8tZmKfUuN8lU",
        "Referer": f"https://www.naukri.com/{seo_key}?k={encoded_keyword}",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response


async def safe_naukri_request(keyword: str, offset: int) -> httpx.Response:
    return await retry_with_backoff(lambda: make_naukri_request(keyword, offset))
