import pydantic
from transit34_models.route import Route
import transit34_models.utils as utils


class LineOnStop(pydantic.BaseModel):
    line_code: str
    line_id: int
    route_code: str
    route_id: int
    route_name: str

    @staticmethod
    def from_raw(d: dict):
        attrs = {}
        attrs["line_code"] = d["GUZERGAH_HAT_KODU"]
        attrs["line_id"] = d["GUZERGAH_HAT_ID"]
        attrs["route_code"] = d["GUZERGAH_GUZERGAH_KODU"]
        attrs["route_id"] = d["GUZERGAH_ID"]
        attrs["route_name"] = utils.clean_str(d["GUZERGAH_GUZERGAH_ADI"])
        return LineOnStop(**attrs)

    @staticmethod
    def from_route(rp: Route):
        return LineOnStop(**rp.model_dump())
