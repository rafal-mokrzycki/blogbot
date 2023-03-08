import json
from pathlib import Path

from fs_gcsfs import GCSFS


def load_config(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def load_config_gcs(file_bucket, file_name):
    file_system = GCSFS(file_bucket)
    with file_system.open(file_name) as f:
        return json.load(f)


if Path("config.json").is_file():
    config = load_config("config.json")
else:
    config = load_config(Path(__file__).parent.joinpath("config.json"))
