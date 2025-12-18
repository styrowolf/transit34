from typing import Optional
import base64
import httpx
from on_api import raw_models
from on_api.headers import headers
from on_api.env import Env
from on_api.cache import cache
from on_api.constants import HALF_HOUR, HALF_MINUTE
import base64
import json
import httpx
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
import os

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

# arac.iett.gov.tr

# utils to decode
def ab2b64(data):
    """Convert bytes to base64 string"""
    return base64.b64encode(data).decode('utf-8')


def b642ab(b64_string):
    """Convert base64 string to bytes"""
    return base64.b64decode(b64_string)

DER_BYTES = b642ab("MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAy9pSv5ktuiGNvUIof18Qi8AToh97U/h6FyWIATGhjiFvG/XQmzFLrRcm+eIAb/QG6GW5mN1XYSUttjbVvS9hJH/vHq+emO//NNr3WEjE5gB1qiK8wrxhq2UtNlyjjtHE5bGTXWG5IkmrfuSqiEXvOhl2tEAXHV9hD+6WhP3e6Qeqxp1yA8BoF1UfDAaqllw0rDNiHC34bC6zepj4KEQw/YkGdmYHqANtFFb0YYO0+bmG4kh8T/LRboX25nzK/jd+8AMefQtap7hI1DXOcOVQdPK3XzKQbGJmHsqyvC4HH3AuDI2G3LAeFTi74KWjNb4mka8RppbqB2sCMnq7GQbbMQIDAQAB")
PUBKEY = serialization.load_der_public_key(DER_BYTES, backend=default_backend())

def get_server_public_key():
    """Fetch and import the server's public RSA key"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
    }
    try:
        #response = httpx.get('https://arac.iett.gov.tr/api/task/crypto/pubkey', headers=headers)
        #response.raise_for_status()
        #j = response.json()

        # Decode the base64 DER-encoded public key
        #der_bytes = b642ab(j['key'])

        # Import the public key
        #public_key = serialization.load_der_public_key(
        #    DER_BYTES,
        #    backend=default_backend()
        #)

        return PUBKEY
    except Exception as e:
        print(f"Error getting server public key: {e}")
        raise


def prepare_session():
    """Prepare encrypted session with AES key"""
    try:
        # Get server's public key
        pub_key = get_server_public_key()

        # Generate AES-256 key
        aes_key = AESGCM.generate_key(bit_length=256)

        # Encrypt the AES key with RSA-OAEP
        encrypted_key = pub_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Generate random IV (12 bytes for GCM)
        iv = os.urandom(12)

        return {
            'aes': aes_key,
            'encKey': ab2b64(encrypted_key),
            'ivB64': ab2b64(iv)
        }
    except Exception as e:
        print(f"Error preparing session: {e}")
        raise


def decrypt_response_if_needed(aes_key, resp_json):
    """Decrypt response if it contains encrypted data"""
    try:
        if resp_json and 'data' in resp_json and 'iv' in resp_json:
            # Decode base64 encrypted data and IV
            ciphertext = b642ab(resp_json['data'])
            iv = b642ab(resp_json['iv'])

            # Decrypt using AES-GCM
            aesgcm = AESGCM(aes_key)
            plaintext = aesgcm.decrypt(iv, ciphertext, None)

            # Decode and parse JSON
            text = plaintext.decode('utf-8')
            return json.loads(text)

        return resp_json
    except Exception as e:
        print(f"Error decrypting response: {e}")
        return resp_json


def get_bus_fleet_hook():
    """Fetch bus fleet data"""
    try:
        session = prepare_session()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
            'Content-Type': 'application/json'
        }

        response = httpx.post(
            'https://arac.iett.gov.tr/api/task/bus-fleet/buses',
            headers=headers,
            json={'encKey': session['encKey']}
        )
        response.raise_for_status()
        j = response.json()

        return decrypt_response_if_needed(session['aes'], j)
    except Exception as e:
        print(f"Error getting bus fleet: {e}")
        return None


def get_car_attributes_hook(door_number):
    """Fetch car attributes by door number"""
    try:
        session = prepare_session()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
            'Content-Type': 'application/json'
        }

        response = httpx.post(
            f'https://arac.iett.gov.tr/api/task/bus-fleet/buses/{door_number}',
            headers=headers,
            json={'encKey': session['encKey']}
        )
        response.raise_for_status()
        j = response.json()

        return decrypt_response_if_needed(session['aes'], j)
    except Exception as e:
        print(f"Error getting car attributes: {e}")
        return None


def get_car_tasks_hook(door_number):
    """Fetch car tasks by door number"""
    try:
        session = prepare_session()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
            'Content-Type': 'application/json'
        }

        response = httpx.post(
            f'https://arac.iett.gov.tr/api/task/getCarTasks/{door_number}',
            headers=headers,
            json={'encKey': session['encKey']}
        )
        response.raise_for_status()
        j = response.json()

        return decrypt_response_if_needed(session['aes'], j)
    except Exception as e:
        print(f"Error getting car tasks: {e}")
        return None



@cache.cache(ttl=HALF_MINUTE)
def bus_fleet():
    return get_bus_fleet_hook()

@cache.cache(ttl=HALF_MINUTE)
def bus_tasks(vehicle_door_no: str):
    return get_car_tasks_hook(vehicle_door_no)

@cache.cache(ttl=HALF_MINUTE)
def bus_info(vehicle_door_no: str):
    return get_car_attributes_hook(vehicle_door_no)
