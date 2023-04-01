import glob
import os
from pathlib import Path
import json

import cv2


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


def read_json(fname: str = 'config.json') -> dict:
    try:
        with open(fname) as json_file:
            return json.load(json_file)
    except Exception as e:
        print(type(e), e, sep='\n')


def append_time_to_path(out_path: Path, time: int) -> Path:
    return Path(f"{str(out_path)}_{str(time).zfill(5)}")


def make_video(frames_dir: Path, video_name: str, fps: int) -> None:
    frames = [cv2.imread(f) for f in glob.glob(os.path.join(frames_dir, '*.png'))]
    frame_size = (frames[0].shape[1], frames[0].shape[0])
    out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), fps=fps, frameSize=frame_size)
    for frame in frames:
        out.write(frame)
    out.release()


def make_output_path(outputdir: str, SCENARIO_NAME: str, empty_output_path: bool = True) -> Path:
    out = Path(os.getcwd()) / outputdir / SCENARIO_NAME
    out.mkdir(parents=True, exist_ok=True)
    if empty_output_path:
        for f in glob.glob(os.path.join(out, '*.*')):
            os.remove(f)
    return out

