import argparse
import glob
import math
from functools import wraps
import os
from pathlib import Path
import json

import colorama
import cv2
from typing import Optional, Tuple, Any

from sneaker_seeker.common_types.vec2d import Vec2D
from sneaker_seeker.game_obj.roi import ROI


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


def my_timer(orig_fun):
    import time
    from functools import wraps
    @wraps(orig_fun)  # will prevent the stacking problem to occure
    def wrapper(*args, **kwargs):
        start = time.time()
        result = orig_fun(*args, **kwargs)
        time_took = round(time.time() - start, 4)
        print(f'{orig_fun.__name__} Run in {time_took} sec')
        return result

    return wrapper


def my_profiler(orig_fun):
    import cProfile
    import pstats
    @wraps(orig_fun)
    def wrapper(*args, **kwargs):
        with cProfile.Profile() as profile:
            result = orig_fun(*args, **kwargs)
        res = pstats.Stats(profile)
        res.sort_stats(pstats.SortKey.TIME)
        res.print_stats()
        res.dump_stats(f"{orig_fun.__name__}_profiling.prof")
        print(f'profiling dump into "{orig_fun.__name__}_profiling.prof" file.\n'
              'you can use the cmd: "pip install tune" \n'
              'followed by: "tuna results.prof" in the cwd for html view.')
        return result

    return wrapper


def progress_bar(progress, total, width=25, color=colorama.Fore.YELLOW):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent // (100 / width)) + '-' * (width - int(percent // (100 / width)))
    if percent < 100:
        print(color + f'\r|{bar}| {percent:.2f}%', end='\r')
    else:
        color = colorama.Fore.GREEN
        print(color + f'\r|{bar}| {percent:.2f}%', end='\r')
        print(colorama.Fore.RESET)


def read_json(fname: str = 'config.json') -> dict:
    try:
        with open(fname) as json_file:
            return json.load(json_file)
    except Exception as e:
        print(type(e), e, sep='\n')


def append_time_to_path(out_path: Path, time: float) -> Path:
    return Path(f"{str(Path(out_path / 'fig'))}_{str(time).zfill(9)}")


def parse_args_to_dict(debug_input=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--scenarios", required=True, type=Path, nargs='+',
                        help="provide the list of paths to *.json scenario files")
    parser.add_argument("-o", "--out_path", required=False, default=Path(os.getcwd()), type=Path,
                        help="output path")
    parser.add_argument("-p", "--play_video", required=False, default=False, action='store_true',
                        help="boolean flag for playing the video after run.")
    parser.add_argument("-k", "--keep_frames", required=False, default=False, action='store_true',
                        help="boolean flag for keeping the frames of every step.")
    parser.add_argument("--frames_format", required=False, default="jpg", choices=['jpg', 'png'], type=str,
                        help="set the frames format. jpg or png")
    parser.add_argument("--speed_up_video", required=False, default=1, type=int,
                        help="speed up the video by that factor")
    parser.add_argument("--scale_world_factor", required=False, default=1, type=float,
                        help="scale the scenario world by that factor")
    parser.add_argument("--save_frame_every_n_step", required=False, default=1, type=int,
                        help="dilute the number of frames in the video to speed up the run time of the application.")
    return parser.parse_args(debug_input).__dict__


# @my_timer
def make_video(frames_dir: Path, frames_format: str, video_name: str, fps: float, keep_frames: bool = False,
               video_format: str = "avi") -> Path:
    png_files_path = os.path.join(frames_dir, f'*.{frames_format}')
    frames = [cv2.imread(f) for f in glob.glob(png_files_path)]
    if not frames:
        print(f'no *.png file found in "{png_files_path}"')
        return
    if not keep_frames:
        for f in glob.glob(os.path.join(frames_dir, '*.*')):
            os.remove(f)
    frame_size = (frames[0].shape[1], frames[0].shape[0])
    vid_path = frames_dir / f"{video_name}.{video_format}"
    out = cv2.VideoWriter(str(vid_path), cv2.VideoWriter_fourcc(*'MP4V' if video_format == "mp4" else 'DIVX'), fps=fps,
                          frameSize=frame_size)
    for frame in frames:
        out.write(frame)
    out.release()
    return vid_path


def make_output_path(outputdir: str, scenario_name: str, empty_output_path: bool = False) -> Path:
    out = outputdir / scenario_name
    out.mkdir(parents=True, exist_ok=True)
    if empty_output_path:
        for f in glob.glob(os.path.join(out, '*.*')):
            os.remove(f)
    return out


def scale_world(scenario: dict, scale_factor):
    for name in ["board"]:
        for k in scenario[name].keys():
            scenario[name][k] *= scale_factor
    for name, sub_name in [["canvas", "fig_size"]]:
        for k in scenario[name][sub_name].keys():
            scenario[name][sub_name][k] *= scale_factor
    scenario['ROI']['height'] *= scale_factor
    scenario['ROI']['width'] *= scale_factor


def real_time_fps(time_step_ms, save_frame_every_n_step) -> float:
    return 1000 / (time_step_ms * save_frame_every_n_step)


def calc_angle(x: float, y: float) -> float:
    return math.degrees(math.atan2(y, x))


def __aim_ahead(dist: Vec2D, relative_speed_vec: Vec2D, friendly_speed_magnitude: float) -> Optional[float]:
    "calculate the time till possible impact."
    # Quadratic equation coefficients a*t^2 + b*t + c = 0
    a = relative_speed_vec.magnitude ** 2 - friendly_speed_magnitude ** 2
    b = 2 * (relative_speed_vec.x * dist.x + relative_speed_vec.y * dist.y)
    c = (dist.x ** 2 + dist.y ** 2)
    desc = b ** 2 - 4 * a * c
    if desc < 0 or (math.sqrt(desc) - b) == 0:  # If the discriminant is negative, then there is no solution
        return None
    return (2 * c) / (math.sqrt(desc) - b)


def calc_possible_collision_point_and_time(trgt_loc: Vec2D, trgt_spd: Vec2D,
                                           friendly_loc: Vec2D, friendly_spd: float) -> Optional[Tuple[Vec2D, float]]:
    """
        calculate the point of future impact.
            return: 'None' if friendly cannot reach.
    """
    dist2d: Vec2D = trgt_loc - friendly_loc
    relative_speed_vec: Vec2D = trgt_spd
    if dt_until_collision := __aim_ahead(dist2d, relative_speed_vec, friendly_spd):
        return trgt_loc + trgt_spd * dt_until_collision, dt_until_collision
    return None


def point_in_roi(point: Vec2D, roi: ROI):
    x1, y1 = roi.location.x, roi.location.y
    x2, y2 = x1 + roi.width, y1 + roi.height
    x, y = point.x, point.y
    return x1 <= x <= x2 and y1 <= y <= y2


def point_in_rectangle(point: Vec2D, x1: float, y1: float, width: float, height: float):
    x2, y2 = x1 + width, y1 + height
    x, y = point.x, point.y
    return x1 <= x <= x2 and y1 <= y <= y2


def flat(list_of_list: list[list[Any]]) -> list[Any]:
    return [e for inner_list in list_of_list for e in inner_list]


def ll_count(ll: list[list[Any]]) -> int:
    return sum(len(s) for s in ll)


def remove_from_list_of_list(list_of_list: list[list[Any]], element):
    for inner_list in list_of_list:
        if element in inner_list:
            inner_list.remove(element)
