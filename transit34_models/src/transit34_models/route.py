from typing import Optional

import pydantic
import transit34_models.utils as utils
from transit34_models.direction import Direction


class Route(pydantic.BaseModel):
    line_code: str
    line_id: int
    line_description: Optional[str]
    line_name: str

    route_code: str
    route_id: int
    route_description: Optional[str]
    route_name: str
    route_direction: Direction

    @staticmethod
    def alphabetic_import(row):
        fields = [
            "line_code",
            "line_description",
            "line_id",
            "line_name",
            "route_code",
            "route_description",
            "route_direction",
            "route_id",
            "route_name",
        ]
        attrs = {}
        for i in range(len(fields)):
            attrs[fields[i]] = row[i]
        return Route(**attrs)

    @staticmethod
    def from_raw(d: dict):
        attrs = {}
        attrs["line_code"] = d["HAT_HAT_KODU"]
        attrs["line_id"] = d["HAT_ID"]
        attrs["line_description"] = d["HAT_ACIKLAMA"]

        if attrs["line_description"] is not None:
            attrs["line_description"] = utils.clean_str(attrs["line_description"])

        attrs["line_name"] = utils.clean_str(d["HAT_HAT_ADI"])

        attrs["route_code"] = d["GUZERGAH_GUZERGAH_KODU"]
        attrs["route_id"] = d["GUZERGAH_ID"]
        attrs["route_description"] = d["GUZERGAH_ACIKLAMA"]

        if attrs["route_description"] is not None:
            attrs["route_description"] = utils.clean_str(attrs["route_description"])

        attrs["route_direction"] = Direction.from_int(d["GUZERGAH_YON"])
        attrs["route_name"] = utils.clean_str(d["GUZERGAH_GUZERGAH_ADI"])
        return Route(**attrs)
