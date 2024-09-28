from dataclasses import dataclass
from typing import Optional


@dataclass
class Agency:
    agency_id: int
    agency_name: str
    agency_url: str
    agency_timezone: str
    agency_lang: Optional[str]
    agency_fare_url: Optional[str]
    agency_phone: Optional[str]

    @staticmethod
    def from_tuple(t):
        return Agency(*t)


@dataclass
class Calendar:
    service_id: int
    monday: int
    tuesday: int
    wednesday: int
    thursday: int
    friday: int
    saturday: int
    sunday: int
    start_date: int
    end_date: int

    @staticmethod
    def from_tuple(t):
        return Calendar(*t)


@dataclass
class Frequency:
    trip_id: int
    start_time: str
    end_time: str
    headway_secs: int
    exact_times: int  # optional

    @staticmethod
    def from_tuple(t):
        return Frequency(*t)


@dataclass
class Route:
    route_id: int
    agency_id: int
    route_short_name: str
    route_long_name: str
    route_desc: Optional[str]
    route_type: int
    route_url: Optional[str]
    route_color: Optional[str]
    route_text_color: Optional[str]

    @staticmethod
    def from_tuple(t):
        return Route(*t)


@dataclass
class Shape:
    shape_id: int
    shape_pt_lat: float
    shape_pt_lon: float
    shape_pt_sequence: int
    shape_dist_traveled: Optional[float]

    @staticmethod
    def from_tuple(t):
        return Shape(*t)


@dataclass
class StopTime:
    trip_id: int
    arrival_time: str
    departure_time: str
    stop_id: int
    stop_sequence: int
    stop_headsign: Optional[str]
    pickup_type: int
    drop_off_type: int
    shape_dist_traveled: Optional[float]
    timepoint: int

    @staticmethod
    def from_tuple(t):
        return StopTime(*t)


@dataclass
class Stop:
    stop_id: int
    stop_code: str  # optional
    stop_name: str
    stop_desc: Optional[str]
    stop_lat: float
    stop_lon: float
    zone_id: Optional[int]
    stop_url: Optional[str]
    location_type: Optional[int]
    parent_station: Optional[int]
    stop_timezone: Optional[str]
    wheelchair_boarding: int  # optional

    @staticmethod
    def from_tuple(t):
        return Stop(*t)


@dataclass
class Trip:
    route_id: int
    service_id: int
    trip_id: int
    trip_headsign: Optional[str]
    trip_short_name: str  # optional
    direction_id: int
    block_id: Optional[int]
    shape_id: Optional[int]
    wheelchair_accessible: int  # opt
    bikes_allowed: int  # opt

    @staticmethod
    def from_tuple(t):
        return Trip(*t)
