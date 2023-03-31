import os
from pathlib import Path
import json

class JsonReader:

    def __init__(self, fname: str = "config.json"):
        try:
            with open(fname) as json_file:
                data = json.load(json_file)
                for k, v in data.items():
                    setattr(self, k, v)
        except Exception as e:
            print(type(e), e, sep='\n')
            exit(-1)


def read_json(fname: str = 'config.json'):
    try:
        with open(fname) as json_file:
            return json.load(json_file)
    except Exception as e:
        print(type(e), e, sep='\n')


def append_time_to_path(out_path: Path, time: int) -> Path:
    return Path(f"{str(out_path)}_{str(time).zfill(5)}")


def make_output_path(outputdir, SCENARIO_NAME) -> Path:
    out = Path(os.getcwd()) / outputdir
    out.mkdir(exist_ok=True)
    output = out / SCENARIO_NAME
    output.mkdir(exist_ok=True)
    return output / SCENARIO_NAME
