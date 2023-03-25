import json
import os
import sys
from pathlib import Path
from dataclasses import dataclass

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

@dataclass
class JsonScenarioReader:
    __slots__ = {
        "seekers_num",
        "sneakers_num",
        "time_goal",
        "board_width",
        "board_height"
    }

    seekers_num: int
    sneakers_num: int
    time_goal: float
    board_width: float
    board_height: float


if __name__ == "__main__":
    senario_params = JsonScenarioReader(**read_json("./senarios/senario01.json"))
    print(senario_params.board_height)
