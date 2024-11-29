import pydantic

class VehicleInfo(pydantic.BaseModel):
    operator: str
    brand_name: str
    seating_capacity: int
    full_capacity: int
    year: int
    vehicle_type: str