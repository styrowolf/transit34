import json
from typing import Optional
from typing_extensions import Annotated
from fastapi import FastAPI, Header, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from transit34_fastapi.env import Env
import transit34_fastapi.geoindexing as geoindexing
import transit34_models as models
from transit34_fastapi.providers.database import (
    ProcessedDataDB,
    get_line_info,
    get_stop_info,
)
from transit34_fastapi.providers.on_api import OtobusumNeredeAPI
from transit34_fastapi.dirs import get_templates_dir, get_translations_dir
import transit34_fastapi.utils as utils
from transit34_fastapi.utils import is_depar_route

app = FastAPI()
templates = Jinja2Templates(directory=get_templates_dir())


def bus_icon() -> str:
    return templates.get_template("icons/bus.html").render({})


def switch_direction_icon() -> str:
    return templates.get_template("icons/switch_direction.html").render({})


def get_language(accept_language: Optional[str]) -> str:
    if accept_language is None:
        return "en"
    else:
        if accept_language.startswith("tr"):
            return "tr"
        elif accept_language.startswith("en"):
            return "en"
        elif accept_language.find("tr") != -1:
            return "tr"
        else:
            return "en"


def get_translations(accept_language: Optional[str]) -> dict[str, str]:
    lang = get_language(accept_language)
    with open(get_translations_dir() / f"{lang}.json", "r") as json_file:
        return json.load(json_file)


def render_map(line_info: models.LineInfo, route_code: str) -> str:
    route = list(filter(lambda e: e.route_code == route_code, line_info.routes))[0]

    min_x, min_y, max_x, max_y = 0, 0, 0, 0
    for stop in route.stops:
        y, x = stop.coordinates.y, stop.coordinates.x
        if min_x == 0:
            min_x = x
        if min_y == 0:
            min_y = y
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    bounds = {}
    bounds["min_x"] = min_x
    bounds["min_y"] = min_y
    bounds["max_x"] = max_x
    bounds["max_y"] = max_y

    markers = []
    for stop in route.stops:
        lat, lon = stop.coordinates.y, stop.coordinates.x

        marker = {"x": lon, "y": lat, "text": stop.stop_name, "type": "stop"}
        markers.append(marker)

    url = Env.TILES_URL
    is_pmtiles = False
    if url.startswith("pmtiles://"):
        is_pmtiles = True
        url = url.removeprefix("pmtiles://")

    markers_url = f"/live_bus_markers/{route.route_code}"

    map_wo_iframe = templates.get_template("maplibre.html").render(
        {
            "markers_url": markers_url,
            "zoom_start": 12,
            "bounds": bounds,
            "is_pmtiles": is_pmtiles,
            "url": url,
            "markers": markers,
        }
    )
    return map_wo_iframe


@app.get("/")
def index(request: Request, accept_language: Annotated[Optional[str], Header()] = None):
    translations = get_translations(accept_language)
    return templates.TemplateResponse(
        "index.html", {"request": request, "translations": translations}
    )


@app.get("/search/lines")
def search_routes(request: Request):
    query = request.query_params.get("query")
    if query is not None and query != "":
        lines = ProcessedDataDB.search_line(query)
        return templates.TemplateResponse(
            "partials/search_lines.html", {"request": request, "lines": lines}
        )
    return HTMLResponse(status_code=200)


@app.get("/search/stops")
def search_stops(request: Request):
    query = request.query_params.get("query")
    if query is not None and query != "":
        stops = ProcessedDataDB.search_stop(query)
        return templates.TemplateResponse(
            "partials/search_stops.html", {"request": request, "stops": stops}
        )
    return HTMLResponse(status_code=200)


@app.get("/partials/arrivals/{stop_code}")
def arrivals_partial(
    stop_code: str,
    request: Request,
    accept_language: Annotated[Optional[str], Header()] = None,
):
    translations = get_translations(accept_language)
    try:
        arrivals: list[models.Arrival] = OtobusumNeredeAPI.stop_arrivals(stop_code)
    except Exception as _e:
        arrivals = []

    return templates.TemplateResponse(
        "partials/stop_arrivals.html",
        {
            "request": request,
            "translations": translations,
            "arrivals": arrivals,
            "bus_icon": bus_icon(),
        },
    )


def render_stops_partial(
    line_info: models.LineInfo, live_buses: list[models.LiveBus], route_code: str
) -> str:
    route: models.RouteInfo = list(
        filter(lambda e: e.route_code == route_code, line_info.routes)
    )[0]
    buses = list(filter(lambda bus: bus.route_code == route_code, live_buses))
    stops: list[dict] = list(map(lambda e: e.model_dump(), route.stops))

    for bus in buses:
        stops[bus.stop_order]["live_bus"] = bus

    return templates.get_template("partials/line_stops.html").render(
        {"stops": stops, "bus_icon": bus_icon()}
    )


def is_opposite_direction(p1: models.RouteInfo, p2: models.RouteInfo) -> bool:
    if p1.route_code == p2.route_code:
        return False

    splits1 = p1.route_code.split("_")
    splits2 = p2.route_code.split("_")

    oppositeByCode = (
        splits1[0] == splits2[0]
        and splits1[1] != splits2[1]
        and splits1[2] == splits2[2]
    )

    if oppositeByCode:
        return True

    is_depar1 = is_depar_route(p1.route_code)
    is_depar2 = is_depar_route(p2.route_code)

    if is_depar1 != is_depar2:
        return False

    name_splits1 = list(map(lambda e: e.strip(), p1.route_name.split("-")))
    name_splits2 = list(map(lambda e: e.strip(), p2.route_name.split("-")))
    same_name = p1.route_name == p2.route_name

    if len(name_splits1) < 2 or len(name_splits2) < 2:
        return False

    oppositeByName = (
        name_splits1[0] == name_splits2[1]
        and name_splits1[1] == name_splits2[0]
        and not same_name
    )

    return oppositeByName


def render_route_partial(
    line_info: models.LineInfo,
    live_buses: list[models.LiveBus],
    route_code: str,
    translations,
) -> str:
    route: models.RouteInfo = list(
        filter(lambda e: e.route_code == route_code, line_info.routes)
    )[0]

    weekdays = list(
        filter(lambda trip: trip.day_type == models.DayType.WorkingDay, route.trips)
    )
    saturdays = list(
        filter(lambda trip: trip.day_type == models.DayType.Saturday, route.trips)
    )
    sundays = list(
        filter(lambda trip: trip.day_type == models.DayType.Sunday, route.trips)
    )

    schedule_sections = []

    for trips, title in [
        (weekdays, translations["weekdays"]),
        (saturdays, translations["saturday"]),
        (sundays, translations["sunday"]),
    ]:
        section = {"title": title, "rows": []}

        times: dict[int, list[int]] = {}

        for trip in trips:
            time = trip.time
            minutes_list = times.get(time.hour, [])
            minutes_list.append(time.minute)
            times[time.hour] = minutes_list

        def int_to_str(i: int) -> str:
            if i < 10:
                return f"0{i}"
            return str(i)

        for hour, minutes in dict(sorted(times.items())).items():
            m2 = list(utils.batch(minutes, 5))
            minutes = "<br>".join(map(lambda e: " | ".join(map(int_to_str, e)), m2))
            section["rows"].append({"hour": hour, "minutes": minutes})

        schedule_sections.append(section)

    opposite_route = None
    opposite_candidates = list(
        filter(lambda e: is_opposite_direction(e, route), line_info.routes)
    )
    if len(line_info.routes) > 0 and len(opposite_candidates) > 0:
        opposite_route = opposite_candidates[0]

    stops_partial = render_stops_partial(line_info, live_buses, route_code)

    schedule = templates.get_template("partials/line_schedule.html").render(
        {"translations": translations, "schedule_sections": schedule_sections}
    )

    return templates.get_template("partials/line_route.html").render(
        {
            "translations": translations,
            "schedule": schedule,
            "stops": stops_partial,
            "route": route,
            "opposite_route": opposite_route,
            "switch_direction_icon": switch_direction_icon(),
        }
    )


@app.get("/partials/stops/{route_code}")
def stops_partial(route_code: str):
    line_code = route_code.split("_")[0]
    line_info: models.LineInfo = get_line_info(line_code)
    try:
        live_buses: list[models.LiveBus] = OtobusumNeredeAPI.live_buses(
            line_info.line_id
        )
    except Exception as _e:
        live_buses = []

    rendered = render_stops_partial(line_info, live_buses, route_code)
    return HTMLResponse(rendered)


@app.get("/partials/route")
def route_partial(
    route_code: str, accept_language: Annotated[Optional[str], Header()] = None
):
    line_code = route_code.split("_")[0]
    translations = get_translations(accept_language)
    line_info: models.LineInfo = get_line_info(line_code)

    # gets live buses via lazy loading later on
    rendered = render_route_partial(line_info, [], route_code, translations)
    return HTMLResponse(rendered)


@app.get("/stops/{stop_code}")
def stop(
    stop_code: int,
    request: Request,
    accept_language: Annotated[Optional[str], Header()] = None,
):
    translations = get_translations(accept_language)
    stop_info = get_stop_info(stop_code)

    arrivals = templates.get_template("partials/stop_arrivals.html").render(
        {"translations": translations}
    )
    return templates.TemplateResponse(
        "stop.html",
        {
            "translations": translations,
            "stop_info": stop_info,
            "arrivals": arrivals,
            "request": request,
        },
    )


@app.get("/lines/{line_code}")
def line(
    line_code: str,
    request: Request,
    route_code: Optional[str] = None,
    accept_language: Annotated[Optional[str], Header()] = None,
):
    translations = get_translations(accept_language)
    line_info: models.LineInfo = get_line_info(line_code)

    # mark depar routes with star
    for p in line_info.routes:
        if is_depar_route(p.route_code):
            p.route_name = f"{p.route_name}*"

    if len(line_info.routes) == 0:
        return templates.TemplateResponse(
            "line.html",
            {
                "request": request,
                "translations": translations,
                "line_info": line_info,
                "route_code": None,
            },
        )

    # skip live buses for first render, let htmx lazily load it
    live_buses = []

    if route_code is not None:
        matches = list(filter(lambda e: e.route_code == route_code, line_info.routes))

        if len(matches) == 0:
            route_code = line_info.routes[0].route_code
    else:
        route_code = line_info.routes[0].route_code

    route_partial = render_route_partial(
        line_info, live_buses, route_code, translations
    )

    return templates.TemplateResponse(
        "line.html",
        {
            "request": request,
            "translations": translations,
            "line_info": line_info,
            "route_code": route_code,
            "route_partial": route_partial,
        },
    )


@app.get("/map/{route_code}")
def map_endpoint(route_code: str):
    line_code = route_code.split("_")[0]
    line_info: models.LineInfo = get_line_info(line_code)

    map_wo_iframe = render_map(line_info, route_code)
    return HTMLResponse(map_wo_iframe)


@app.get("/live_bus_markers/{route_code}")
def map_markers(route_code: str):
    line_code = route_code.split("_")[0]
    line_info: models.LineInfo = get_line_info(line_code)
    try:
        live_buses: list[models.LiveBus] = OtobusumNeredeAPI.live_buses(
            line_info.line_id
        )
    except Exception as _e:
        live_buses = []
        return {"success": False}

    route = list(filter(lambda e: e.route_code == route_code, line_info.routes))[0]
    markers = []

    buses = list(filter(lambda e: e.route_code == route.route_code, live_buses))
    for bus in buses:
        lat, lon = bus.last_location.y, bus.last_location.x
        door = bus.vehicle_door_no

        marker = {"x": lon, "y": lat, "text": door, "type": "bus"}
        markers.append(marker)

    return {"success": True, "markers": markers}


@app.get("/partials/announcements/line/{line_code}")
def route_announcements(
    line_code: str,
    request: Request,
    accept_language: Annotated[Optional[str], Header()] = None,
):
    translations = get_translations(accept_language)
    try:
        announcements: list[models.LineAnnouncement] = (
            OtobusumNeredeAPI.line_announcements(line_code)
        )
    except Exception as _e:
        announcements = None

    return templates.TemplateResponse(
        "partials/line_announcements.html",
        {
            "request": request,
            "translations": translations,
            "announcements": announcements,
        },
    )


@app.get("/partials/announcements/stop/{stop_code}")
def stop_announcements(
    stop_code: int,
    request: Request,
    accept_language: Annotated[Optional[str], Header()] = None,
):
    translations = get_translations(accept_language)
    try:
        announcements: list[models.StopAnnouncement] = (
            OtobusumNeredeAPI.stop_announcements(stop_code)
        )
    except Exception as _e:
        announcements = None

    return templates.TemplateResponse(
        "partials/stop_announcements.html",
        {
            "request": request,
            "translations": translations,
            "announcements": announcements,
        },
    )


@app.get("/live/bus/{vehicle_door_no}/marker")
def bus_marker(vehicle_door_no: str):
    try:
        bus: models.LiveBusIndividual = OtobusumNeredeAPI.bus_location_by_door_no(
            vehicle_door_no
        )
    except Exception as _e:
        bus = None
        return {"success": False}

    lat, lon = bus.last_location.y, bus.last_location.x
    door = bus.vehicle_door_no
    marker = {
        "x": lon,
        "y": lat,
        "text": f"{door} ({bus.last_location_time})",
        "type": "bus",
    }

    return {"success": True, "markers": [marker]}


@app.get("/partial/map/bus/{vehicle_door_no}")
def vehicle_map(
    vehicle_door_no: str, request: Request, route_code: Optional[str] = None
):
    try:
        bus: models.LiveBusIndividual = OtobusumNeredeAPI.bus_location_by_door_no(
            vehicle_door_no
        )
    except Exception as _e:
        bus = None

    markers = []

    zoom = None
    bounds = None
    center = None

    if route_code is not None:
        line_code = route_code.split("_")[0]
        line_info = get_line_info(line_code)
        pattern = list(filter(lambda e: e.route_code == route_code, line_info.routes))[
            0
        ]

        min_x, min_y, max_x, max_y = 0, 0, 0, 0
        for stop in pattern.stops:
            y, x = stop.coordinates.y, stop.coordinates.x
            if min_x == 0:
                min_x = x
            if min_y == 0:
                min_y = y
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

        bounds = {}
        bounds["min_x"] = min_x
        bounds["min_y"] = min_y
        bounds["max_x"] = max_x
        bounds["max_y"] = max_y

        for stop in pattern.stops:
            lat, lon = stop.coordinates.y, stop.coordinates.x

            marker = {"x": lon, "y": lat, "text": stop.stop_name, "type": "stop"}
            markers.append(marker)
    else:
        zoom = 12

    if bus:
        center = {"x": bus.last_location.x, "y": bus.last_location.y}
        zoom = 14
        bounds = None

    url = Env.TILES_URL
    is_pmtiles = False
    if url.startswith("pmtiles://"):
        is_pmtiles = True
        url = url.removeprefix("pmtiles://")

    markers_url = f"/live/bus/{vehicle_door_no}/marker"

    map_wo_iframe = templates.get_template("maplibre.html").render(
        {
            "markers_url": markers_url,
            "center": center,
            "zoom": zoom,
            "bounds": bounds,
            "is_pmtiles": is_pmtiles,
            "url": url,
            "markers": markers,
        }
    )
    return HTMLResponse(map_wo_iframe)


@app.get("/bus/{vehicle_door_no}")
def vehicle(
    vehicle_door_no: str,
    request: Request,
    route_code: Optional[str] = None,
    accept_language: Annotated[Optional[str], Header()] = None,
):
    translations = get_translations(accept_language)
    translations["busNotFoundExplanation"] = translations[
        "busNotFoundExplanation"
    ].format(vehicle_door_no=vehicle_door_no)
    try:
        bus: models.LiveBusIndividual = OtobusumNeredeAPI.bus_location_by_door_no(
            vehicle_door_no
        )
    except Exception as _e:
        bus = None

    return templates.TemplateResponse(
        "bus.html",
        {
            "bus": bus,
            "vehicle_door_no": vehicle_door_no,
            "route_code": route_code,
            "translations": translations,
            "request": request,
        },
    )


@app.get("/nearby_stops/{lat}/{lon}")
def nearby_stops(lat: float, lon: float, request: Request):
    stops: list[dict] = []
    for e in geoindexing.nearby_stops({"x": lon, "y": lat}, 500):
        stop_code = int(e[0])
        distance = e[1]
        stop = ProcessedDataDB.stop(stop_code).model_dump()
        stop["distance"] = distance
        stops.append(stop)

    stops.sort(key=lambda e: e["distance"])

    return templates.TemplateResponse(
        "partials/nearby_stops.html",
        {"request": request, "stops": stops, "lat": lat, "lon": lon},
    )


@app.get("/map/nearby_stops/{lat}/{lon}")
def nearby_stops_map(
    lat: float,
    lon: float,
    request: Request,
    accept_language: Annotated[Optional[str], Header()] = None,
):
    translations = get_translations(accept_language)
    stops: list[dict] = []
    for e in geoindexing.nearby_stops({"x": lon, "y": lat}, 500):
        stop_code = int(e[0])
        distance = e[1]
        stop = ProcessedDataDB.stop(stop_code).model_dump()
        stop["distance"] = distance
        stops.append(stop)

    stops.sort(key=lambda e: e["distance"])

    min_x, min_y, max_x, max_y = 0, 0, 0, 0
    markers = []
    for stop in stops:
        y, x = stop["coordinates"]["y"], stop["coordinates"]["x"]
        if min_x == 0:
            min_x = x
        if min_y == 0:
            min_y = y
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

        marker = {
            "x": x,
            "y": y,
            "text": f"{stop['stop_name']} ({(stop['direction'])})",
            "type": "stop",
        }
        markers.append(marker)

    bounds = {}
    bounds["min_x"] = min_x
    bounds["min_y"] = min_y
    bounds["max_x"] = max_x
    bounds["max_y"] = max_y

    url = Env.TILES_URL
    is_pmtiles = False
    if url.startswith("pmtiles://"):
        is_pmtiles = True
        url = url.removeprefix("pmtiles://")

    markers.append(
        {"x": lon, "y": lat, "text": translations["youAreHere"], "type": "user"}
    )

    map_wo_iframe = templates.get_template("maplibre.html").render(
        {
            "markers_url": None,
            "center": None,
            "zoom": None,
            "bounds": bounds,
            "is_pmtiles": is_pmtiles,
            "url": url,
            "markers": markers,
        }
    )
    return HTMLResponse(map_wo_iframe)
