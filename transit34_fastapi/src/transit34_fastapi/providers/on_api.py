from typing import Optional
from transit34_models import (
    Arrival,
    LiveBus,
    LineOnStop,
    Route,
    Stop,
    LineStop,
    StopWithoutCoordinates,
    TimetableTrip,
)
import transit34_models as models
from transit34_on_api.api_calls import (
    timetable,
    route,
    route_patterns,
    nearby_stops,
    routes_on_stop,
    stop,
    stop_arrivals,
    bus_point_passing,
    stop_announcements,
    route_announcements,
    bus_location_by_door_no,
)


class OtobusumNeredeAPI:
    @staticmethod
    def timetable(line_code: str) -> list[TimetableTrip]:
        return list(map(lambda e: TimetableTrip.from_raw(e), timetable(line_code)))

    @staticmethod
    def line_stops(line_code: str, route_code: Optional[str] = None) -> list[LineStop]:
        return list(map(lambda e: LineStop.from_raw(e), route(line_code, route_code)))

    @staticmethod
    def routes(line_code: str) -> list[Route]:
        return list(map(lambda e: Route.from_raw(e), route_patterns(line_code)))

    @staticmethod
    def nearby_stops(lat: float, lon: float, radius: float = 1) -> list[Stop]:
        return list(map(lambda e: Stop.from_raw(e), nearby_stops(lat, lon, radius)))

    @staticmethod
    def lines_on_stop(stop_code: int) -> list[LineOnStop]:
        return list(map(lambda e: LineOnStop.from_raw(e), routes_on_stop(stop_code)))

    @staticmethod
    def stop(stop_code: int) -> Stop:
        return list(map(lambda e: StopWithoutCoordinates.from_raw(e), stop(stop_code)))

    @staticmethod
    def stop_arrivals(stop_code: int) -> list[Arrival]:
        return list(map(lambda e: Arrival.from_raw(e), stop_arrivals(stop_code)))

    @staticmethod
    def live_buses(line_id: int) -> list[LiveBus]:
        return list(map(lambda e: LiveBus.from_raw(e), bus_point_passing(line_id)))

    @staticmethod
    def stop_announcements(stop_code: int) -> list[models.StopAnnouncement]:
        return models.StopAnnouncement.from_raw(stop_announcements(stop_code))

    @staticmethod
    def line_announcements(line_code: str) -> list[models.LineAnnouncement]:
        return models.LineAnnouncement.from_raw(route_announcements(line_code))

    @staticmethod
    def bus_location_by_door_no(vehicle_door_no: str) -> models.LiveBusIndividual:
        return models.LiveBusIndividual.from_raw(
            bus_location_by_door_no(vehicle_door_no)
        )
