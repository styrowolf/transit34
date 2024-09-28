import pydantic
import models.utils as utils
from models.coordinates import Coordinates
from models.direction import Direction


class LineStop(pydantic.BaseModel):
    stop_name: str
    stop_code: int
    coordinates: Coordinates
    direction: str

    line_code: str
    line_id: int

    route_code: str
    route_order: int
    route_direction: Direction

    @staticmethod
    def alphabetic_import(row):
        fields = [
            "coordinates_x",
            "coordinates_y",
            "direction",
            "line_code",
            "line_id",
            "route_code",
            "route_direction",
            "route_order",
            "stop_code",
            "stop_name",
        ]

        attrs = {}
        for i in range(len(fields)):
            if fields[i] == "coordinates_x":
                attrs["coordinates"] = {"x": row[i]}
            elif fields[i] == "coordinates_y":
                attrs["coordinates"]["y"] = row[i]
            else:
                attrs[fields[i]] = row[i]

        return LineStop(**attrs)

    @staticmethod
    def from_raw(stop: dict):
        attrs = {}
        attrs["stop_name"] = utils.clean_str(stop["DURAK_ADI"])
        attrs["stop_code"] = stop["DURAK_DURAK_KODU"]
        attrs["coordinates"] = Coordinates(**stop["DURAK_GEOLOC"])
        attrs["direction"] = utils.clean_str(stop["DURAK_YON_BILGISI"])

        attrs["line_code"] = stop["HAT_HAT_KODU"]
        attrs["line_id"] = stop["HAT_ID"]

        attrs["route_code"] = stop["GUZERGAH_GUZERGAH_KODU"]
        attrs["route_order"] = stop["GUZERGAH_SEGMENT_SIRA"]
        attrs["route_direction"] = Direction.from_int(stop["GUZERGAH_YON"])

        return LineStop(**attrs)
