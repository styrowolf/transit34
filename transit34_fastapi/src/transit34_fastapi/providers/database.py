import sqlite3
from typing import Optional
from transit34_models import Line, Route, LineOnStop, Stop, LineStop, TimetableTrip

from transit34_fastapi.env import Env
import transit34_models as models
from transit34_fastapi.utils import is_depar_route
from transit34_fastapi import utils

con = sqlite3.connect(Env.DATABASE, check_same_thread=False)


def cursor():
    return con.cursor()


def number_of_timetable_trips(line_code: str, route_code: Optional[str] = None) -> int:
    if route_code is not None:
        out = (
            cursor()
            .execute(
                "SELECT COUNT(*) FROM timetables WHERE line_code = ? AND route_code = ?",
                [line_code, route_code],
            )
            .fetchone()
        )
        return out[0]
    else:
        out = (
            cursor()
            .execute("SELECT COUNT(*) FROM timetables WHERE line_code = ?", [line_code])
            .fetchone()
        )
        return out[0]


def last_stop_order(line_code: str, route_code: str) -> int:
    return (
        cursor()
        .execute(
            "SELECT max(route_order) FROM line_stops WHERE line_code = ? AND route_code = ?;",
            [line_code, route_code],
        )
        .fetchone()
    )


class ProcessedDataDB:
    @staticmethod
    def timetable(
        line_code: str, route_code: Optional[str] = None
    ) -> list[TimetableTrip]:
        if route_code is not None:
            rows = (
                cursor()
                .execute(
                    "SELECT * FROM timetables WHERE line_code = ? AND route_code = ?",
                    [line_code, route_code],
                )
                .fetchall()
            )
            return list(map(lambda e: TimetableTrip.alphabetic_import(e), rows))
        else:
            rows = (
                cursor()
                .execute("SELECT * FROM timetables WHERE line_code = ?", [line_code])
                .fetchall()
            )
            return list(map(lambda e: TimetableTrip.alphabetic_import(e), rows))

    @staticmethod
    def line_stops(line_code: str, route_code: Optional[str] = None) -> list[LineStop]:
        if route_code is not None:
            rows = (
                cursor()
                .execute(
                    "SELECT * FROM line_stops WHERE line_code = ? AND route_code = ?",
                    [line_code, route_code],
                )
                .fetchall()
            )
            return list(map(lambda e: LineStop.alphabetic_import(e), rows))
        else:
            rows = (
                cursor()
                .execute("SELECT * FROM line_stops WHERE line_code = ?", [line_code])
                .fetchall()
            )
            return list(map(lambda e: LineStop.alphabetic_import(e), rows))

    @staticmethod
    def routes(line_code: str) -> list[Route]:
        rows = (
            cursor()
            .execute("SELECT * FROM routes WHERE line_code = ?", [line_code])
            .fetchall()
        )
        return list(map(lambda e: Route.alphabetic_import(e), rows))

    @staticmethod
    def route(line_code: str) -> Route:
        row = (
            cursor()
            .execute("SELECT * FROM routes WHERE route_code = ?", [line_code])
            .fetchone()
        )
        return Route.alphabetic_import(row)

    @staticmethod
    def stop(stop_code: int) -> Stop:
        row = (
            cursor()
            .execute("SELECT * FROM stops WHERE stop_code = ?", [stop_code])
            .fetchone()
        )
        return Stop.alphabetic_import(row)

    @staticmethod
    def line(line_code: str) -> Line:
        row = (
            cursor()
            .execute("SELECT * FROM lines WHERE line_code = ?", [line_code])
            .fetchone()
        )
        return Line.alphabetic_import(row)

    @staticmethod
    def search_line(query: str) -> list[Line]:
        query = utils.query_transform(query)
        rows = (
            cursor()
            .execute(
                "SELECT * FROM lines WHERE line_name LIKE ? OR line_code LIKE ? LIMIT 10",
                [query, query],
            )
            .fetchall()
        )
        return list(map(lambda e: Line.alphabetic_import(e), rows))

    @staticmethod
    def search_stop(query: str) -> list[Stop]:
        query = utils.query_transform(query)
        rows = (
            cursor()
            .execute(
                "SELECT * FROM stops WHERE stop_name LIKE ? AND stop_code > 0 AND (SELECT COUNT(*) FROM line_stops WHERE (SELECT COUNT(*) FROM timetables WHERE timetables.route_code = line_stops.route_code) > 0) > 0 LIMIT 10",
                [query],
            )
            .fetchall()
        )
        return list(map(lambda e: Stop.alphabetic_import(e), rows))

    @staticmethod
    def lines_on_stop(stop_code: int) -> list[LineOnStop]:
        rows = (
            cursor()
            .execute("SELECT * FROM line_stops WHERE stop_code = ?", [stop_code])
            .fetchall()
        )
        candidates: list[LineStop] = list(
            map(lambda e: LineStop.alphabetic_import(e), rows)
        )

        candidates = list(
            filter(
                lambda e: number_of_timetable_trips(e.line_code, e.route_code) > 0,
                candidates,
            )
        )

        candidates = list(
            filter(
                lambda e: last_stop_order(e.line_code, e.route_code) != e.route_order,
                candidates,
            )
        )

        routes = list(
            map(
                lambda e: Route.alphabetic_import(
                    cursor()
                    .execute(
                        "SELECT * FROM routes WHERE line_code = ? AND route_code = ?",
                        [e.line_code, e.route_code],
                    )
                    .fetchone()
                ),
                candidates,
            )
        )
        return list(map(lambda e: LineOnStop.from_route(e), routes))


def get_line_info(line_code: str) -> models.LineInfo:
    line = ProcessedDataDB.line(line_code)
    routes: list[models.Route] = ProcessedDataDB.routes(line_code)
    timetable: list[models.TimetableTrip] = ProcessedDataDB.timetable(line_code)
    route_infos: list[models.RouteInfo] = []

    for e in routes:
        stops: list[models.LineStop] = ProcessedDataDB.line_stops(
            e.line_code, e.route_code
        )
        trips = list(
            filter(
                lambda trip: trip.line_code == e.line_code
                and trip.route_code == e.route_code,
                timetable,
            )
        )
        info = models.RouteInfo(stops=stops, trips=trips, **e.model_dump())
        route_infos.append(info)

    route_infos_filtered = list(
        filter(lambda pattern: len(pattern.trips) > 0, route_infos)
    )
    return models.LineInfo(routes=route_infos_filtered, **line.model_dump())


def get_route_info(route_code: str) -> models.RouteInfo:
    e = ProcessedDataDB.route(route_code)
    timetable: list[models.TimetableTrip] = ProcessedDataDB.timetable(
        e.line_code, e.route_code
    )
    stops: list[models.LineStop] = ProcessedDataDB.line_stops(e.line_code, e.route_code)

    trips = list(
        filter(
            lambda trip: trip.line_code == e.line_code
            and trip.route_code == e.route_code,
            timetable,
        )
    )

    return models.RouteInfo(trips=trips, stops=stops, **e.model_dump())


def get_stop_info(stop_code: int) -> models.StopInfo:
    lines_on_stop: list[models.LineOnStop] = ProcessedDataDB.lines_on_stop(stop_code)
    filtered: list[LineOnStop] = []
    line_codes_to_routes: dict[str, list[str]] = {}

    for line in lines_on_stop:
        arr = line_codes_to_routes.get(line.line_code)
        if arr is not None:
            arr.append(line.route_code)
        else:
            line_codes_to_routes[line.line_code] = [line.route_code]

    for line in lines_on_stop:
        routes = line_codes_to_routes[line.line_code]
        if len(routes) == 1:
            filtered.append(line)
        else:
            if all(map(lambda e: is_depar_route(e), routes)):
                filtered.append(line)
            elif not is_depar_route(line.route_code):
                filtered.append(line)

    out = ProcessedDataDB.stop(stop_code)
    return models.StopInfo(lines=filtered, **out.model_dump())


def get_stop_id(stop_code: int) -> int:
    return (
        cursor()
        .execute("SELECT stop_id FROM stops WHERE stop_code = ?", [stop_code])
        .fetchone()[0]
    )


def get_all_line_infos():
    line_codes = list(
        map(lambda e: e[0], cursor().execute("SELECT line_code FROM lines"))
    )

    for line_code in line_codes:
        yield get_line_info(line_code)


def get_all_stops() -> list[models.Stop]:
    stops = cursor().execute("SELECT * FROM stops WHERE stop_code > 0").fetchall()
    return list(map(lambda e: Stop.alphabetic_import(e), stops))


def get_all_stops_without_useless_ones() -> list[models.Stop]:
    stops = (
        cursor()
        .execute(
            "SELECT * FROM stops WHERE stop_code > 0 AND (SELECT COUNT(*) FROM line_stops WHERE (SELECT COUNT(*) FROM timetables WHERE timetables.route_code = line_stops.route_code) > 0) > 0"
        )
        .fetchall()
    )
    return list(map(lambda e: Stop.alphabetic_import(e), stops))
