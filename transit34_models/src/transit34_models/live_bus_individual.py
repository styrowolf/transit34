from datetime import datetime, time
import pydantic
from transit34_models.coordinates import Coordinates


class LiveBusIndividual(pydantic.BaseModel):
    vehicle_door_no: str
    last_location_time: time
    last_location: Coordinates
    vehicle_plate: str
    speed: float

    @staticmethod
    def from_raw(resp: list):
        resp = resp[0]
        attrs = {}
        attrs["vehicle_door_no"] = resp["K_ARAC_KAPINUMARASI"]
        format = "%Y-%m-%dT%H:%M:%S"
        time_str = resp["H_OTOBUSKONUM_KAYITZAMANI"].split(".")[0]
        time = datetime.strptime(time_str, format).time()
        attrs["last_location_time"] = time
        attrs["last_location"] = {
            "x": resp["H_OTOBUSKONUM_BOYLAM"],
            "y": resp["H_OTOBUSKONUM_ENLEM"],
        }
        attrs["vehicle_plate"] = resp["K_ARAC_PLAKA"]
        attrs["speed"] = resp["H_OTOBUSKONUM_HIZ"]
        return LiveBusIndividual(**attrs)
