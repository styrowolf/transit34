import json
from redis import Redis

from t34.env import Env
from t34 import utils
from on_api.api_calls import bus_fleet
from on_api import raw_models
from timeloop import Timeloop
from datetime import timedelta

client = Redis(host=Env.REDIS_HOSTNAME, port=Env.REDIS_PORT)

tl = Timeloop()

@tl.job(interval=timedelta(minutes=30))
def update_fleet():
    fleet: list[raw_models.BusInfo] = [raw_models.BusInfo.model_validate(bus) for bus in bus_fleet()]
    pipe = client.pipeline()
    pipe.delete("fleet")
    buses = utils.sort_vehicle_door_codes([bus.vehicleDoorCode for bus in fleet])
    pipe.set("fleet", json.dumps(buses))
    pipe.execute()

def get_fleet() -> list[str]:
    return json.loads(client.get("fleet"))

def init():
    if not client.exists("fleet"):
        update_fleet()
    tl.start(block=False)