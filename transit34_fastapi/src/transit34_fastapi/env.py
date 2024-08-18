import os


def if_not_none(value, default):
    return value if value is not None else default


class Env:
    REDIS_HOSTNAME = "127.0.0.1"
    REDIS_PORT = 6379
    TILES_URL = "https://tiles.kurt.town/tiles/istanbul/{z}/{x}/{y}.mvt"
    DATABASE = "databases/otobus.sqlite3"


Env.REDIS_HOSTNAME = if_not_none(os.getenv("REDIS_HOSTNAME"), Env.REDIS_HOSTNAME)
Env.REDIS_PORT = if_not_none(os.getenv("REDIS_PORT"), Env.REDIS_PORT)
Env.TILES_URL = if_not_none(os.getenv("TILES_URL"), Env.TILES_URL)
Env.DATABASE = if_not_none(os.getenv("DATABASE"), Env.DATABASE)
