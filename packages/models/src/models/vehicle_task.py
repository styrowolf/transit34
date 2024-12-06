from datetime import datetime, time, timedelta, timezone
from typing import Optional
from models import utils
import pydantic
from on_api import raw_models

# TODO: interpret actual from the other tasks of the vehicle
# TODO: get starting station from line_name.split(" - ")[0]
class VehicleTask(pydantic.BaseModel):
    line_code: str
    route_code: Optional[str]
    line_name: str
    task_start_time: str

    @staticmethod
    def from_raw(r: raw_models.BusTask):
        dt = datetime.fromtimestamp(int(r.approximateStartTime / 1000), tz=timezone(timedelta(hours=3)))
        task_start_time = dt.time().strftime("%H:%M")
        extracted_line_code = utils.extract_line_code_from_route_code(r.routeCode)
        
        line_code = r.lineCode
        route_code = r.routeCode

        # if two values do not agree remove route_code
        if extracted_line_code != line_code:
            route_code = None

        return VehicleTask(
            route_code=route_code,
            task_start_time=task_start_time,
            line_name=r.lineName,
            line_code=line_code,
        )