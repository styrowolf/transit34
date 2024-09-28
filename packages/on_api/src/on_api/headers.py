import httpx

from on_api.cache import cache
from on_api.constants import HALF_HOUR
from on_api.env import Env


@cache.cache(ttl=HALF_HOUR)
def headers():
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "ntcapi.iett.istanbul",
        "User-Agent": Env.USER_AGENT,
    }

    data = f"grant_type={Env.GRANT_TYPE}&scope={Env.SCOPE}&client_id={Env.CLIENT_ID}&client_secret={Env.CLIENT_SECRET}"

    resp = httpx.post(Env.OAUTH2_URL, headers=headers, data=data)
    access_token = resp.json()["access_token"]
    headers["Authorization"] = f"Bearer {access_token}"
    headers["Content-Type"] = "application/json"
    return headers
