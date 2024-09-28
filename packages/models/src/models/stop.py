import pydantic
import models.utils as utils
from models.coordinates import Coordinates


class Stop(pydantic.BaseModel):
    stop_name: str
    stop_code: int
    stop_id: int
    coordinates: Coordinates
    direction: str

    @staticmethod
    def alphabetic_import(row):
        fields = [
            "coordinates_x",
            "coordinates_y",
            "direction",
            "stop_code",
            "stop_id",
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
        return Stop(**attrs)

    @staticmethod
    def from_raw(stop: dict):
        attrs = {}
        attrs["stop_name"] = utils.clean_str(stop["DURAK_ADI"])
        attrs["stop_code"] = stop["DURAK_DURAK_KODU"]
        attrs["stop_id"] = stop["DURAK_ID"]
        attrs["coordinates"] = stop["DURAK_GEOLOC"]
        attrs["direction"] = utils.clean_str(stop["DURAK_YON_BILGISI"])
        return Stop(**attrs)
