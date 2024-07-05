import json


def read_json_file(filename: str) -> dict:
    with open(filename, "r") as f:
        return json.load(f)
