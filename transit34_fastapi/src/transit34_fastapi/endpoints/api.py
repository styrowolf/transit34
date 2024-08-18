from typing import Optional

from fastapi import FastAPI, HTTPException

import transit34_fastapi.geoindexing as geoindexing
import transit34_models as models
from transit34_fastapi.providers.database import (
    ProcessedDataDB,
    get_line_info,
    get_route_info,
    get_stop_info,
)
from transit34_fastapi.providers.on_api import OtobusumNeredeAPI

app = FastAPI()


@app.get("/")
def read_root():
    return "pt-otobus API v0.1.0"


@app.get("/line/{line_code}/stops")
def line_stops(
    line_code: str, route_code: Optional[str] = None
) -> list[models.LineStop]:
    return ProcessedDataDB.line_stops(line_code, route_code)


@app.get("/line/{line_code}/routes")
def routes(line_code: str) -> list[models.Route]:
    return ProcessedDataDB.routes(line_code)


@app.get("/line/{line_code}/timetable")
def timetable(line_code: str) -> list[models.TimetableTrip]:
    return ProcessedDataDB.timetable(line_code)


@app.get(
    "/line/{line_code}/info",
    name="Line info",
    openapi_extra={"x-fern-sdk-method-name": "lineInfo"},
)
def line_info(line_code: str) -> models.LineInfo:
    return get_line_info(line_code)


@app.get("/route/{route_code}/stops")
def route_stops(route_code: str) -> list[models.LineStop]:
    line_code = route_code.split("_")[0]
    return ProcessedDataDB.line_stops(line_code, route_code)


@app.get("/route/{route_code}/timetable")
def route_timetable(route_code: str) -> list[models.TimetableTrip]:
    line_code = route_code.split("_")[0]
    return ProcessedDataDB.timetable(line_code, route_code)


@app.get(
    "/route/{route_code}/info/",
    name="Line",
    openapi_extra={"x-fern-sdk-method-name": "routeInfo"},
)
def route_info(route_code: str) -> models.RouteInfo:
    return get_route_info(route_code)


@app.get("/stops")
def nearby_stops(
    lat: float, lon: float, radius: Optional[float] = 1000
) -> list[models.NearbyStop]:
    stops = []
    for e in geoindexing.nearby_stops({"x": lon, "y": lat}, radius):
        stop_code = int(e[0])
        distance = e[1]
        stop = ProcessedDataDB.stop(stop_code)
        stops.append(models.NearbyStop(distance=distance, **stop.model_dump()))

    return stops


@app.get("/stop/{stop_code}/lines")
def lines_on_stop(stop_code: str, api: bool = False) -> list[models.LineOnStop]:
    if api:
        return OtobusumNeredeAPI.lines_on_stop(
            stop_code
        )  # just returns non-DEPAR route patterns on stop
    else:
        return ProcessedDataDB.lines_on_stop(
            stop_code
        )  # returns DEPAR and non-DEPAR route patterns on stop


@app.get(
    "/stop/{stop_code}/info",
    name="Stop info",
    openapi_extra={"x-fern-sdk-method-name": "stopInfo"},
)
def stop_info(stop_code: int) -> models.StopInfo:
    return get_stop_info(stop_code)


@app.get(
    "/live/line/{line_code}/buses",
    name="Live buses on route",
    openapi_extra={"x-fern-sdk-method-name": "liveBusesOnRoute"},
)
def buses_on_route(line_code: str) -> list[models.LiveBus]:
    line = ProcessedDataDB.line(line_code)
    try:
        return OtobusumNeredeAPI.live_buses(line.line_id)
    except Exception as _e:
        print(_e)
        raise HTTPException(
            status_code=404, detail="Cannot access live buses for this route"
        )


@app.get("/live/line/{line_code}/announcements")
def line_announcements(line_code: str) -> list[models.LineAnnouncement]:
    return OtobusumNeredeAPI.line_announcements(line_code)


@app.get(
    "/live/stop/{stop_code}/arrivals",
    name="Live arrivals at stop",
    openapi_extra={"x-fern-sdk-method-name": "stopArrivals"},
)
def live_arrivals(stop_code: int) -> list[models.Arrival]:
    try:
        return OtobusumNeredeAPI.stop_arrivals(stop_code)
    except Exception as _e:
        raise HTTPException(
            status_code=404, detail="Cannot access stop arrivals for this stop"
        )


@app.get("/live/stop/{stop_code}/announcements")
def stop_announcements(stop_code: int) -> list[models.StopAnnouncement]:
    return OtobusumNeredeAPI.stop_announcements(stop_code)


@app.get("/live/bus/{vehicle_door_no}")
def bus_location(vehicle_door_no: str) -> models.LiveBusIndividual:
    return OtobusumNeredeAPI.bus_location_by_door_no(vehicle_door_no)


@app.get(
    "/search/line",
    name="Search route",
    openapi_extra={"x-fern-sdk-method-name": "searchRoute"},
)
def line_search(query: str) -> list[models.Line]:
    return ProcessedDataDB.search_line(query)


@app.get(
    "/search/stop",
    name="Search stop",
    openapi_extra={"x-fern-sdk-method-name": "searchStop"},
)
def stop_search(query: str) -> list[models.Stop]:
    return ProcessedDataDB.search_stop(query)
