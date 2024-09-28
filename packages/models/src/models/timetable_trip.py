from datetime import datetime, time
from enum import Enum
from typing import Optional
import pydantic

from models.direction import Direction


class DayType(str, Enum):
    WorkingDay = "working_day"
    Saturday = "saturday"
    Sunday = "sunday"

    @staticmethod
    def from_str(day: str):
        if day == "I":
            return DayType.WorkingDay
        elif day == "C":
            return DayType.Saturday
        elif day == "P":
            return DayType.Sunday
        else:
            return None


class TimetableTrip(pydantic.BaseModel):
    line_code: str
    route_code: str
    time: time
    day_type: DayType
    direction: Direction

    @staticmethod
    def alphabetic_import(row):
        fields = ["day_type", "direction", "line_code", "route_code", "time"]
        attrs = {}
        for i in range(len(fields)):
            attrs[fields[i]] = row[i]

        # convert TEXT from database to time
        attrs["time"] = datetime.strptime(attrs["time"], "%H:%M:%S").time()
        return TimetableTrip(**attrs)

    @staticmethod
    def from_raw(t: dict, errors: Optional[list] = None):
        try:
            attrs = {}
            attrs["line_code"] = t["GUZERGAH_HAT_KODU"]
            attrs["route_code"] = t["K_ORER_SGUZERGAH"]
            dformat = "%Y-%m-%d %H:%M:%S"
            attrs["time"] = datetime.strptime(t["K_ORER_DTSAATGIDIS"], dformat).time()
            attrs["day_type"] = DayType.from_str(t["K_ORER_SGUNTIPI"])
            attrs["direction"] = Direction.from_str(t["K_ORER_SYON"])
            return TimetableTrip(**attrs)
        except pydantic.ValidationError as e:
            if errors is not None:
                errors.append(
                    {
                        "error": str(e),
                        "raw_data": t,
                    }
                )
            return None
