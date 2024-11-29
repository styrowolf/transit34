from pydantic import BaseModel
from typing import Optional

# simple chatgpt generated basemodels with all fields optional, to extract data and have ide support
class BusInfo(BaseModel):
    vehicleDoorCode: Optional[str] = None
    numberPlate: Optional[str] = None
    garageCode: Optional[str] = None
    garageName: Optional[str] = None
    operatorId: Optional[int] = None
    operatorType: Optional[str] = None
    accessibility: Optional[bool] = None
    brandName: Optional[str] = None
    modelYear: Optional[int] = None
    vehicleType: Optional[str] = None
    seatingCapacity: Optional[int] = None
    fullCapacity: Optional[int] = None
    isAirConditioned: Optional[bool] = None
    hasUsbCharger: Optional[bool] = None
    hasWifi: Optional[bool] = None
    hasBicycleRack: Optional[bool] = None
    vehicleSoftwareVersion: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    speed: Optional[int] = None
    ## YYYY-MM-DD
    lastLocationDate: Optional[str] = None
    # HH:MM:SS
    lastLocationTime: Optional[str] = None

class BusTask(BaseModel):
    taskId: Optional[int] = None
    taskStartTime: Optional[int] = None
    taskEndTime: Optional[int] = None
    taskComingTime: Optional[int] = None
    approximateEndTime: Optional[int] = None
    approximateStartTime: Optional[int] = None
    serviceNo: Optional[int] = None
    driverRegisterNo: Optional[str] = None
    lineCode: Optional[str] = None
    lineName: Optional[str] = None
    routeDirection: Optional[int] = None
    routeCode: Optional[str] = None
    unreadMessage: Optional[bool] = None
    taskStatus: Optional[int] = None
    oldLineName: Optional[str] = None
    superiorName: Optional[str] = None
    busDoorNumber: Optional[str] = None
    driverId: Optional[int] = None
    vehicleId: Optional[int] = None
    routeId: Optional[int] = None
    updatedStartTime: Optional[int] = None
    lineId: Optional[int] = None
    taskStatusCode: Optional[str] = None # A = active, B = next
    justificationId: Optional[int] = None
    lastLocationTime: Optional[int] = None
    updatedBy: Optional[str] = None
    interventionCode: Optional[str] = None
    note: Optional[str] = None
    updatedTime: Optional[int] = None
    isActive: Optional[bool] = None
    lastPointOrderNumber: Optional[int] = None
    taskTypeId: Optional[int] = None
    createdBy: Optional[int] = None
    lastStopPassedCode: Optional[str] = None
    lastStopPassedName: Optional[str] = None
    stopId: Optional[int] = None
    stopCode: Optional[str] = None
    stopName: Optional[str] = None
    sendingTime: Optional[int] = None
    sendingTimeOld: Optional[int] = None
    hasPlanSent: Optional[bool] = None
    deliveryReportTime: Optional[int] = None
    gprsActive: Optional[bool] = None
