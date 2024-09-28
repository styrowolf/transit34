import pydantic
from models import utils


class StopAnnouncement(pydantic.BaseModel):
    line_code: str
    information: str

    @staticmethod
    def from_raw(announcement: dict) -> list:
        announcements = []
        for stop in announcement.values():
            for a in stop["duyuru"]:
                attrs = {}
                attrs["line_code"] = a["HAT"]
                attrs["information"] = utils.clean_str(a["BILGI"])
                announcements.append(attrs)

        return announcements
