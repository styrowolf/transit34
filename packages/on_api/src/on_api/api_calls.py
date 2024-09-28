from typing import Optional
import httpx
from on_api.headers import headers
from on_api.env import Env
from on_api.cache import cache
from on_api.constants import HALF_HOUR, HALF_MINUTE


@cache.cache(ttl=HALF_HOUR)
def stop(stop_code: int):
    h = headers()
    payload = {
        "alias": "mainGetBusStop_basic_search",
        "data": {
            "HATYONETIM.DURAK.DURAK_KODU": stop_code,
        },
    }

    resp = httpx.post(Env.SERVICE_URL, headers=h, json=payload)
    return resp.json()


# model done
@cache.cache(ttl=HALF_HOUR)
def timetable(route_code: str):
    h = headers()
    payload = {
        "alias": "akyolbilGetTimeTable",
        "data": {
            "HATYONETIM.GUZERGAH.HAT_KODU": route_code,
        },
    }

    resp = httpx.post(Env.SERVICE_URL, headers=h, json=payload)
    return resp.json()


# model done
@cache.cache(ttl=HALF_HOUR)
def route(route_code: str, route_pattern: Optional[str] = None):
    h = headers()
    payload = {
        "alias": "mainGetRoute",
        "data": {
            "HATYONETIM.HAT.HAT_KODU": route_code,
        },
    }

    if route_pattern is not None:
        payload["data"]["HATYONETIM.GUZERGAH.GUZERGAH_KODU"] = route_pattern

    resp = httpx.post(Env.SERVICE_URL, headers=h, json=payload)
    return resp.json()


# model done
@cache.cache(ttl=HALF_HOUR)
def route_patterns(route_code: str):
    h = headers()
    payload = {
        "alias": "mainGetLine",
        "data": {
            "HATYONETIM.HAT.HAT_KODU": route_code,
        },
    }

    resp = httpx.post(Env.SERVICE_URL, headers=h, json=payload)
    return resp.json()


@cache.cache(ttl=HALF_MINUTE)
def live_buses(route_id: int, state_id: str = "23"):
    h = headers()
    payload = {
        "data": {
            "AKYOLBILYENI.H_GOREV.HATID": route_id,
            "AKYOLBILYENI.H_GOREV.GOREVDURUMID": state_id,
        },
        "alias": "mainGetBusRunBusStopPass",
    }

    resp = httpx.post(Env.SERVICE_URL, headers=h, json=payload)
    return resp.json()


@cache.cache(ttl=HALF_MINUTE)
def live_buses_on_route_old(route_id: Optional[str], door_number=Optional[str]):
    h = headers()
    payload = {"alias": "mainGetLiveBus_basic", "data": {}}

    if door_number is not None:
        payload["data"]["AKYOLBILYENI.K_ARAC.KAPINUMARASI"] = door_number

    if route_id is not None:
        payload["data"]["AKYOLBILYENI.K_GUZERGAH.HATID"] = route_id

    resp = httpx.post(Env.SERVICE_URL, headers=h, json=payload)
    return resp.json()


# model done
@cache.cache(ttl=HALF_MINUTE)
def bus_point_passing(route_id: int):
    h = headers()
    payload = {
        "alias": "ybs",
        "data": {
            "method": "POST",
            "path": ["real-time-information", "point-passing", route_id],
            "data": {"username": "netuce", "password": "n1!t8c7M1"},
        },
    }

    resp = httpx.post(Env.SERVICE_URL, headers=h, json=payload)
    return resp.json()


# model done
@cache.cache(ttl=HALF_HOUR)
def routes_on_stop(stop_code: int):
    h = headers()
    payload = {
        "alias": "mainGetBusStopLine",
        "data": {
            "HATYONETIM.DURAK.DURAK_KODU": stop_code,
        },
    }

    resp = httpx.post(Env.SERVICE_URL, headers=h, json=payload)
    return resp.json()


# model done
@cache.cache(ttl=HALF_MINUTE)
def stop_arrivals(stop_code: int):
    h = headers()
    payload = {
        "alias": "ybs",
        "data": {
            "method": "POST",
            "data": {"username": "netuce", "password": "n1!t8c7M1"},
            "path": ["real-time-information", "stop-arrivals", stop_code],
        },
    }

    resp = httpx.post(Env.SERVICE_URL, headers=h, json=payload)
    return resp.json()


@cache.cache(ttl=HALF_MINUTE)
def stop_announcements(stop_code: int):
    h = headers()
    payload = {
        "alias": "ybs",
        "data": {
            "data": {"password": "n1!t8c7M1", "username": "netuce"},
            "method": "POST",
            "path": ["real-time-information", "stop-status", stop_code],
        },
    }

    resp = httpx.post(Env.SERVICE_URL, headers=h, json=payload)
    return resp.json()


@cache.cache(ttl=HALF_MINUTE)
def route_announcements(route_code: str):
    h = headers()
    payload = {
        "data": {
            "method": "POST",
            "data": {"username": "netuce", "password": "n1!t8c7M1"},
            "path": ["real-time-information", "line-status", route_code, "*"],
        },
        "alias": "ybs",
    }

    resp = httpx.post(Env.SERVICE_URL, headers=h, json=payload)
    return resp.json()


@cache.cache(ttl=HALF_MINUTE)
def bus_location_by_door_no(vehicle_door_no: str):
    h = headers()
    payload = {
        "alias": "mainGetBusLocation_basic",
        "data": {"AKYOLBILYENI.K_ARAC.KAPINUMARASI": vehicle_door_no},
    }

    resp = httpx.post(Env.SERVICE_URL, headers=h, json=payload)
    return resp.json()


# model done
@cache.cache(ttl=HALF_HOUR)
def nearby_stops(lat: float, lon: float, radius: float = 1):
    h = headers()
    payload = {
        "data": {
            "HATYONETIM.DURAK.GEOLOC": {
                "r": radius,
                "lat": lat,
                "long": lon,
            }
        },
        "alias": "mainGetBusStopNearby",
    }

    resp = httpx.post(Env.SERVICE_URL, headers=h, json=payload)
    return resp.json()
