from redis_cache import RedisCache
from redis import Redis

from transit34_on_api.env import Env

client = Redis(
    host=Env.REDIS_HOSTNAME,
    port=Env.REDIS_PORT,
    decode_responses=True,
)

cache = RedisCache(
    redis_client=client,
)
