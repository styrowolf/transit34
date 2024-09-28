import pydantic
from models.route_info import RouteInfo


class LineInfo(pydantic.BaseModel):
    line_code: str
    line_id: int
    line_name: str
    routes: list[RouteInfo]
