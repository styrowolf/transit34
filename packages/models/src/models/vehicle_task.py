from datetime import datetime, time, timedelta, timezone
from models import utils
import pydantic
from on_api import raw_models

class VehicleTask(pydantic.BaseModel):
    line_code: str
    route_code: str
    line_name: str
    task_start_time: str

    @staticmethod
    def from_raw(r: raw_models.BusTask):
        dt = datetime.fromtimestamp(int(r.approximateStartTime / 1000), tz=timezone(timedelta(hours=3)))
        task_start_time = dt.time().strftime("%H:%M")
        line_code = utils.extract_line_code_from_route_code(r.routeCode)
        return VehicleTask(
            route_code=r.routeCode,
            task_start_time=task_start_time,
            line_name=r.lineName,
            line_code=line_code,
        )