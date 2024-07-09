import json
from typing import Any, Dict, cast


def read_json_file(file_path: str, init_if_empty: bool = True) -> Dict[str, Any]:
    """
    Reads a JSON file.
    :param file_path: Path to json file.
    :param init_if_empty: Initializes empty dictionary in file.
    :return: File JSON as object.
    """
    file_content = read_file(file_path)
    if init_if_empty and len(file_content) == 0:
        return {}
    return cast(Dict[str, Any], json.loads(file_content))


def read_file(file_path: str):
    with open(file_path, "r") as f:
        return f.read()
