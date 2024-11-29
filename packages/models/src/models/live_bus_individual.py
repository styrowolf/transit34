from datetime import datetime, time
from models import utils
import pydantic
from models.coordinates import Coordinates
from models.amenities import Amenities
from models.vehicle_info import VehicleInfo
from on_api import raw_models

# otobüsüm nerede API
class LiveBusIndividualOld(pydantic.BaseModel):
    vehicle_door_no: str
    last_location_time: time
    last_location: Coordinates
    vehicle_plate: str
    speed: float

    @staticmethod
    def from_raw(resp: list):
        resp = resp[0]
        attrs = {}
        attrs["vehicle_door_no"] = resp["K_ARAC_KAPINUMARASI"]
        format = "%Y-%m-%dT%H:%M:%S"
        time_str = resp["H_OTOBUSKONUM_KAYITZAMANI"].split(".")[0]
        time = datetime.strptime(time_str, format).time()
        attrs["last_location_time"] = time
        attrs["last_location"] = {
            "x": resp["H_OTOBUSKONUM_BOYLAM"],
            "y": resp["H_OTOBUSKONUM_ENLEM"],
        }
        attrs["vehicle_plate"] = resp["K_ARAC_PLAKA"]
        attrs["speed"] = resp["H_OTOBUSKONUM_HIZ"]
        return LiveBusIndividual(**attrs)

# arac.iett.gov.tr API
class LiveBusIndividual(pydantic.BaseModel):
    vehicle_door_no: str
    last_location_time: time
    last_location: Coordinates
    vehicle_plate: str
    speed: float
    amenities: Amenities
    vehicle_info: VehicleInfo

    def from_raw(r: raw_models.BusInfo):
        format = "%H:%M:%S"
        last_location_time = datetime.strptime(r.lastLocationTime, format).time()
        last_location = {
            "x": r.longitude,
            "y": r.latitude,
        }
        amenities = Amenities(
            wheelchair_accessible=r.accessibility,
            air_conditioning=utils.false_if_none(r.isAirConditioned),
            bicycle=r.hasBicycleRack,
            usb=r.hasUsbCharger,
            wifi=r.hasWifi,
        )

        vehicle_info = VehicleInfo(
            operator=r.operatorType,
            brand_name=r.brandName,
            year=r.modelYear,
            vehicle_type=r.vehicleType,
            seating_capacity=r.seatingCapacity,
            full_capacity=r.fullCapacity,
        )

        return LiveBusIndividual(vehicle_door_no=r.vehicleDoorCode, vehicle_plate=r.numberPlate, last_location_time=last_location_time, last_location=last_location, speed=r.speed, amenities=amenities, vehicle_info=vehicle_info)