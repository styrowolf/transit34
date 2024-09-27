import argparse
from dataclasses import dataclass

import duckdb
from transit34_cli.subcommands.gtfs_to_dataset import gtfs_types


@dataclass
class GTFSToDatasetArgs:
    def configure_parser(parser: argparse.ArgumentParser):
        parser.set_defaults(func=main)


@dataclass
class StopSetCandidate:
    stops: list[int]
    stops_code: str
    trips: list[gtfs_types.Trip]
    direction: int


def construct(l: list[int]) -> str:
    return "_".join(map(str, l))


def main(args):
    duckcon = duckdb.connect(
        "~/programming/pt/data/2024-06-07T14-22-17/public-transport-gtfs-data-utf8/istanbul-gtfs.db",
        read_only=True,
    )

    def lm(t, query) -> list:
        res = duckcon.execute(query).fetchall()
        return list(map(lambda e: t.from_tuple(e), res))

    routes: list[gtfs_types.Route] = lm(
        gtfs_types.Route, "SELECT * FROM routes;"
    )  # WHERE route_short_name LIKE 'T3';

    """
    routes 
    -> trips0, trips1

    seperate trips0 into stopsets (stopsets0)
    seperate trips1 into stopsets (stopsets1)

    stopsets = []

    for stopset0 in stopsets0:
        for stopset1 in stopsets1:
            if stopset0->stops == reverse(stopset1->stops)
                merge stopset0 and stopset1 as outbound and inbound pair, append to stopsets
                remove stopset1 from iteration
                break
            else:
                append stopset0 to stopsets

    add remaining unadded stopsets in stopsets1 to stopsets
    """
    for route in routes:
        trips0: list[gtfs_types.Trip] = lm(
            gtfs_types.Trip,
            f"SELECT * FROM trips WHERE route_id = '{route.route_id}' AND direction_id = 0;",
        )
        trips1: list[gtfs_types.Trip] = lm(
            gtfs_types.Trip,
            f"SELECT * FROM trips WHERE route_id = '{route.route_id}' AND direction_id = 1;",
        )

        def process_trips(trips: list[gtfs_types.Trip]) -> dict[str, StopSetCandidate]:
            stopsets: dict[str, StopSetCandidate] = {}
            s: list[list[int]] = []
            for trip in trips:
                stop_ids = duckcon.execute(
                    f"SELECT stop_id FROM stop_times WHERE trip_id = '{trip.trip_id}' ORDER BY stop_sequence;"
                ).fetchall()
                s.append(list(map(lambda e: e[0], stop_ids)))

            for ids, trip in zip(s, trips):
                ids_str = construct(ids)
                ssc = stopsets.get(ids_str)
                if ssc is None:
                    stopsets[ids_str] = StopSetCandidate(
                        stops=ids, stops_code=ids_str, trips=[trip], direction=0
                    )
                else:
                    ssc.trips.append(trip)

            return stopsets

        stopsets0: dict[str, StopSetCandidate] = process_trips(trips0)
        stopsets1: dict[str, StopSetCandidate] = process_trips(trips1)

        def make_pairs() -> list[list[StopSetCandidate | None]]:
            added_stopsets1 = set()
            stopset_pairs: list[list[StopSetCandidate | None]] = []

            if len(stopsets0) > 0 and len(stopsets1) == 0:
                return [[stopset, None] for stopset in stopsets0]
            elif len(stopsets1) > 0 and len(stopsets0) == 0:
                return [[None, stopset] for stopset in stopsets1]
            else:
                for k0, stopset0 in stopsets0.items():
                    for k1, stopset1 in stopsets1.items():
                        k1_reversed = construct(list(reversed(stopset1.stops)))
                        if k0 == k1_reversed:
                            stopset_pairs.append([stopset0, stopset1])
                            added_stopsets1.add(k1)
                        else:
                            stopset_pairs.append([stopset0, None])

                for k1, stopset1 in stopsets1.items():
                    if k1 not in added_stopsets1:
                        stopset_pairs.append([None, stopset1])
                return stopset_pairs

        stopset_pairs = make_pairs()
        
