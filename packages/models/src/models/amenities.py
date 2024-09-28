import pydantic


class Amenities(pydantic.BaseModel):
    wheelchair_accessible: bool
    wifi: bool
    air_conditioning: bool
    usb: bool
    bicycle: bool
