import pydantic
from models.coordinates import Coordinates
from models.line_on_stop import LineOnStop


class StopInfo(pydantic.BaseModel):
    stop_name: str
    stop_code: int
    stop_id: int
    coordinates: Coordinates
    direction: str
    lines: list[LineOnStop]
