import httpx
from transit34_cli.env import Env

HEADERS = None


def get_headers():
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


def headers():
    global HEADERS
    if HEADERS is None:
        HEADERS = get_headers()
    return HEADERS


def all_stops():
    h = headers()
    payload = {"data": {}, "alias": "mainGetBusStopNearby"}

    resp = httpx.post(Env.SERVICE_URL, headers=h, json=payload, timeout=60)
    return resp.json()


def all_routes():
    h = headers()
    payload = {
        "alias": "mainGetLine",
        "data": {},
    }

    resp = httpx.post(Env.SERVICE_URL, headers=h, json=payload, timeout=60)
    return resp.json()


def all_timetables():
    h = headers()
    payload = {"alias": "akyolbilGetTimeTable", "data": {}}

    resp = httpx.post(Env.SERVICE_URL, headers=h, json=payload, timeout=60)
    return resp.json()


def all_line_stops():
    h = headers()
    payload = {"alias": "mainGetRoute", "data": {}}

    resp = httpx.post(Env.SERVICE_URL, headers=h, json=payload, timeout=60)
    return resp.json()


def all_lines():
    h = headers()
    payload = {"alias": "mainGetLine_basic_search", "data": {}}

    resp = httpx.post(Env.SERVICE_URL, headers=h, json=payload, timeout=60)
    return resp.json()
