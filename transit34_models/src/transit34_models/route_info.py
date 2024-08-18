from typing import Optional

import pydantic
from transit34_models.direction import Direction
from transit34_models.line_stop import LineStop
from transit34_models.timetable_trip import TimetableTrip


class RouteInfo(pydantic.BaseModel):
    line_code: str
    line_id: int
    line_description: Optional[str]
    line_name: str

    route_code: str
    route_id: int
    route_description: Optional[str]
    route_name: str
    route_direction: Direction

    stops: list[LineStop]
    trips: list[TimetableTrip]
