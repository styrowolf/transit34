from datetime import datetime, time
import pydantic
from models import utils
from models.amenities import Amenities
from models.coordinates import Coordinates


class Arrival(pydantic.BaseModel):
    line_code: str
    route_code: str
    line_name: str
    vehicle_door_no: str
    last_location_time: time
    last_speed: float
    last_location: Coordinates
    stop_order: int
    minutes_until_arrival: int
    amenities: Amenities

    @staticmethod
    def from_raw(arrival: dict):
        attrs = {}
        attrs["line_code"] = arrival["hatkodu"]
        attrs["route_code"] = arrival["guzergah"]
        attrs["line_name"] = utils.clean_str(arrival["hatadi"])
        attrs["vehicle_door_no"] = arrival["kapino"]
        format = "%H:%M:%S"
        attrs["last_location_time"] = datetime.strptime(
            arrival["son_konum_saati"], format
        ).time()
        attrs["last_speed"] = arrival["son_hiz"]
        coords = arrival["son_konum"].split(",")
        attrs["last_location"] = {
            "x": coords[0],
            "y": coords[1],
        }
        attrs["stop_order"] = arrival["stopOrder"]
        attrs["minutes_until_arrival"] = arrival["dakika"]
        attrs["amenities"] = {}
        attrs["amenities"]["wheelchair_accessible"] = bool(arrival["engelli"])
        attrs["amenities"]["wifi"] = bool(arrival["wifi"])
        attrs["amenities"]["air_conditioning"] = bool(arrival["klima"])
        attrs["amenities"]["usb"] = bool(arrival["usb"])
        attrs["amenities"]["bicycle"] = bool(arrival["bisiklet"])

        return Arrival(**attrs)
