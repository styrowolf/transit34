from datetime import datetime, time
from typing import Optional

import pydantic
from models.coordinates import Coordinates


class LiveBus(pydantic.BaseModel):
    line_id: int
    route_code: str
    vehicle_door_no: str
    last_location_time: time
    last_location: Coordinates
    stop_order: int
    stop_id: int
    stop_enter_time: Optional[time]
    stop_exit_time: Optional[time]

    @staticmethod
    def from_raw(bus: dict):
        attrs = {}
        attrs["line_id"] = bus["H_GOREV_HATID"]
        attrs["route_code"] = bus["K_GUZERGAH_GUZERGAHKODU"]
        attrs["vehicle_door_no"] = bus["K_ARAC_KAPINUMARASI"]
        format = "%Y-%m-%dT%H:%M:%S"
        time = bus["SISTEMSAATI"].split(".")[0]
        attrs["last_location_time"] = datetime.strptime(time, format).time()
        attrs["last_location"] = {
            "x": bus["BOYLAM"],
            "y": bus["ENLEM"],
        }
        # passed stop order (-1 fixes overguessing)
        attrs["stop_order"] = bus["H_GOREV_DURAK_GECIS_SIRANO"] - 1
        attrs["stop_id"] = bus["H_GOREV_DURAK_GECIS_DURAKID"]

        if bus["H_GOREV_D_G_GIRISZAMANI"] is not None:
            time = bus["H_GOREV_D_G_GIRISZAMANI"].split(".")[0]
            attrs["stop_enter_time"] = datetime.strptime(time, format).time()
        else:
            attrs["stop_enter_time"] = None

        if bus["H_GOREV_D_G_GECISZAMANI"] is not None:
            time = bus["H_GOREV_D_G_GECISZAMANI"].split(".")[0]
            attrs["stop_exit_time"] = datetime.strptime(time, format).time()
        else:
            attrs["stop_exit_time"] = None

        return LiveBus(**attrs)
