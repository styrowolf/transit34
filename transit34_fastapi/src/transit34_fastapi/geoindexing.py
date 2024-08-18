import transit34_models as models
from transit34_fastapi.providers.database import get_all_stops_without_useless_ones

from redis import Redis

from transit34_fastapi.env import Env

client = Redis(host=Env.REDIS_HOSTNAME, port=Env.REDIS_PORT)


def init():
    client.delete("geoindexed:stops")
    stops = get_all_stops_without_useless_ones()

    pipe = client.pipeline()
    for stop in stops:
        pipe.geoadd(
            "geoindexed:stops",
            [stop.coordinates.x, stop.coordinates.y, stop.stop_code],
        )

    pipe.execute()


def nearby_stops(c: models.Coordinates, radius: float) -> list[list[str, float]]:
    return client.geosearch(
        "geoindexed:stops",
        latitude=c["y"],
        longitude=c["x"],
        radius=radius,
        unit="m",
        withdist=True,
        withcoord=False,
    )
