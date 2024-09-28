import pydantic
from models import utils


class LineAnnouncement(pydantic.BaseModel):
    line_code: str
    information: str

    @staticmethod
    def from_raw(announcement: dict) -> list:
        announcements = []
        for route in announcement.values():
            for a in route.values():
                attrs = {}
                attrs["line_code"] = a["HAT"]
                attrs["information"] = utils.clean_str(a["BILGI"])
                message = a.get("MESAJ")
                if message is not None:
                    attrs["information"] = (
                        f"{utils.clean_str(message)} ({attrs['information']})"
                    )
                announcements.append(attrs)

        return announcements
