import pydantic
import models.utils as utils


class StopWithoutCoordinates(pydantic.BaseModel):
    stop_name: str
    stop_code: int
    stop_id: int
    direction: str

    @staticmethod
    def from_raw(stop: dict):
        attrs = {}
        attrs["stop_name"] = utils.clean_str(stop["DURAK_ADI"])
        attrs["stop_code"] = stop["DURAK_DURAK_KODU"]
        attrs["stop_id"] = stop["DURAK_ID"]
        attrs["direction"] = utils.clean_str(stop["DURAK_YON_BILGISI"])

        return StopWithoutCoordinates(**attrs)
