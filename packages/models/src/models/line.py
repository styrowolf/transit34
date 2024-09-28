import pydantic
import models.utils as utils


class Line(pydantic.BaseModel):
    line_name: str
    line_id: int
    line_code: str

    @staticmethod
    def alphabetic_import(row):
        fields = ["line_code", "line_id", "line_name"]
        attrs = {}
        for i in range(len(fields)):
            attrs[fields[i]] = row[i]
        return Line(**attrs)

    @staticmethod
    def from_raw(r: dict):
        attrs = {}
        attrs["line_name"] = utils.clean_str(r["HAT_HAT_ADI"])
        attrs["line_id"] = r["HAT_ID"]
        attrs["line_code"] = r["HAT_HAT_KODU"]
        return Line(**attrs)
