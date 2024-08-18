import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import sqlite3

import duckdb

import transit34_models as models
import transit34_cli.utils as utils
from transit34_cli.api_calls import (
    all_line_stops,
    all_lines,
    all_routes,
    all_stops,
    all_timetables,
)


@dataclass
class IETTDownloadArgs:
    out_path: Path
    skip_download: bool = False
    skip_process: bool = False
    skip_duckdb_raw: bool = False
    skip_duckdb: bool = False
    skip_sqlite: bool = False

    @staticmethod
    def from_args(args):
        return IETTDownloadArgs(
            Path(args.path),
            args.skip_download,
            args.skip_process,
            args.skip_duckdb_raw,
            args.skip_duckdb,
            args.skip_sqlite,
        )

    def configure_parser(parser: argparse.ArgumentParser):
        parser.add_argument(
            "path",
            type=str,
            default=".",
            nargs="?",
            help="output directory for downloaded files (default: current directory)",
        )

        parser.add_argument(
            "--skip-download",
            action="store_true",
            help="skip downloading data",
        )

        parser.add_argument(
            "--skip-process",
            action="store_true",
            help="skip processing raw data",
        )

        parser.add_argument(
            "--skip-duckdb-raw",
            action="store_true",
            help="skip loading raw data into duckdb",
        )

        parser.add_argument(
            "--skip-duckdb",
            action="store_true",
            help="skip loading processed data into duckdb",
        )

        parser.add_argument(
            "--skip-sqlite",
            action="store_true",
            help="skip loading data into sqlite3",
        )

        parser.set_defaults(func=main)


def download(out_path: Path) -> list:
    stops_raw = all_stops()
    print("fetched stops!")
    utils.json_file_dump(stops_raw, out_path / "stops-raw.json")

    routes_raw = all_routes()
    print("fetched routes!")
    utils.json_file_dump(routes_raw, out_path / "routes-raw.json")

    timetables_raw = all_timetables()
    print("fetched timetables!")
    utils.json_file_dump(timetables_raw, out_path / "timetables-raw.json")

    line_stops_raw = all_line_stops()
    print("fetched line stops!")
    utils.json_file_dump(line_stops_raw, out_path / "line_stops-raw.json")

    lines_raw = all_lines()
    print("fetched lines!")
    utils.json_file_dump(lines_raw, out_path / "lines-raw.json")

    return [stops_raw, routes_raw, timetables_raw, line_stops_raw, lines_raw]


def load_raw_data(out_path: Path) -> list:
    stops_raw = utils.json_file_load(out_path / "stops-raw.json")
    routes_raw = utils.json_file_load(out_path / "routes-raw.json")
    timetables_raw = utils.json_file_load(out_path / "timetables-raw.json")
    line_stops_raw = utils.json_file_load(out_path / "line_stops-raw.json")
    lines_raw = utils.json_file_load(out_path / "lines-raw.json")

    return [stops_raw, routes_raw, timetables_raw, line_stops_raw, lines_raw]


def process_raw(raw_data: list, out_path: Path, errors: list = None):
    [stops_raw, routes_raw, timetables_raw, line_stops_raw, lines_raw] = raw_data

    stops = list(map(lambda stop: models.Stop.from_raw(stop), stops_raw))
    print("processed stops!")
    utils.pydantic_model_list_dump(stops, out_path / "stops.json")

    routes = list(map(lambda pattern: models.Route.from_raw(pattern), routes_raw))
    print("processed routes!")
    utils.pydantic_model_list_dump(routes, out_path / "routes.json")

    timetables = list(
        filter(
            lambda e: e is not None,
            map(
                lambda timetable: models.TimetableTrip.from_raw(
                    timetable, errors=errors
                ),
                timetables_raw,
            ),
        )
    )
    print("processed timetables!")
    utils.pydantic_model_list_dump(timetables, out_path / "timetables.json")

    line_stops = list(
        map(lambda route: models.LineStop.from_raw(route), line_stops_raw)
    )
    print("processed line stops!")
    utils.pydantic_model_list_dump(line_stops, out_path / "line_stops.json")

    lines = list(map(lambda route: models.Line.from_raw(route), lines_raw))
    print("processed lines!")
    utils.pydantic_model_list_dump(lines, out_path / "lines.json")


def load_into_duckdb(duckdb_path: Path, json_path: Path):
    con = duckdb.connect(str(duckdb_path))
    cur = con.cursor()

    def exec_stmt(table_name):
        cur.execute(
            f"CREATE TABLE {table_name} AS SELECT * FROM read_json('{json_path / f'{table_name}.json'}', format = 'array');"
        )

    for table_name in ["stops", "routes", "timetables", "line_stops", "lines"]:
        exec_stmt(table_name)
    con.close()


def load_into_duckdb_raw(duckdb_path: Path, json_path: Path):
    con = duckdb.connect(str(duckdb_path))
    cur = con.cursor()

    def exec_stmt(table_name):
        cur.execute(
            f"CREATE TABLE {table_name} AS SELECT * FROM read_json('{json_path / f'{table_name}-raw.json'}', format = 'array');"
        )

    for table_name in ["stops", "routes", "timetables", "line_stops", "lines"]:
        exec_stmt(table_name)
    con.close()


def load_into_sqlite_from_duckdb(duckdb_path: Path, sqlite_path: Path, strict: bool):
    sql_dir = utils.get_sql_dir()

    con = sqlite3.connect(str(sqlite_path))
    create_script = "create_tables.sql" if strict else "create_tables_nostrict.sql"
    create_script = utils.read(sql_dir / create_script)
    con.cursor().executescript(create_script)
    con.commit()
    print("created tables!")
    con.close()

    duckcon = duckdb.connect()
    duckcon.execute(f"ATTACH DATABASE '{duckdb_path}' AS ptd;")
    duckcon.execute(f"ATTACH DATABASE '{sqlite_path}' AS pts (TYPE SQLITE);")
    print("attached both databases to duckdb!")

    import_script = utils.read(sql_dir / "import_from_duckdb.sql")
    duckcon.execute(import_script)
    duckcon.close()
    print("imported data to sqlite3 database!")

    con = sqlite3.connect(str(sqlite_path))
    create_indexes_script = utils.read(sql_dir / "create_indexes.sql")
    con.executescript(create_indexes_script)
    con.commit()
    con.close()

    print("created indexes in sqlite3!")


def main(args):
    args = IETTDownloadArgs.from_args(args)
    errors = []
    os.makedirs(args.out_path, exist_ok=True)

    if not args.skip_download:
        raw_data = download(args.out_path)
    else:
        raw_data = load_raw_data(args.out_path)

    if not args.skip_process:
        process_raw(raw_data, args.out_path, errors=errors)

    if not args.skip_duckdb:
        load_into_duckdb(args.out_path / "iett.duckdb", args.out_path)

    if not args.skip_duckdb_raw:
        load_into_duckdb_raw(args.out_path / "iett-raw.duckdb", args.out_path)

    if not args.skip_sqlite:
        load_into_sqlite_from_duckdb(
            args.out_path / "iett.duckdb", args.out_path / "iett.sqlite3", strict=False
        )

    utils.json_file_dump(errors, args.out_path / "errors.json")
    print("done!")
