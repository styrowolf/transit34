import pydantic
from models.coordinates import Coordinates


class NearbyStop(pydantic.BaseModel):
    stop_name: str
    stop_code: int
    stop_id: int
    coordinates: Coordinates
    direction: str
    distance: float
