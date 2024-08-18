import pydantic


class Coordinates(pydantic.BaseModel):
    x: float
    y: float
