import pydantic
from transit34_models.coordinates import Coordinates
from transit34_models.line_on_stop import LineOnStop


class StopInfo(pydantic.BaseModel):
    stop_name: str
    stop_code: int
    stop_id: int
    coordinates: Coordinates
    direction: str
    lines: list[LineOnStop]
