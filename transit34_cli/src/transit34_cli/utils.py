import json
import os
from pathlib import Path

import pydantic


def json_file_dump(data, filename):
    with open(filename, "w") as f:
        # IMPORTANT: sqlite3 table creation script expects keys to be sorted
        json.dump(data, f, sort_keys=True)


def json_file_load(filename):
    return json.loads(read(filename))


def pydantic_model_list_dump(data: list[pydantic.BaseModel], filename):
    json_file_dump(list(map(lambda x: x.model_dump(mode="json"), data)), filename)


def get_sql_dir():
    path = os.path.dirname(os.path.abspath(__file__))
    path = Path(path)
    return path.parent.parent / "sql"


def read(filename):
    with open(filename, "r") as f:
        return f.read()
