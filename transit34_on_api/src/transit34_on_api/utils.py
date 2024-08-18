import json


def compact_dump(data):
    return json.dumps(data, separators=(",", ":"))