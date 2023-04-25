import subprocess
from pathlib import Path

from sneaker_seeker.utilities import utils
from sneaker_seeker.path_planner.path_planner_factory import PathPlannerFactory
from sneaker_seeker.game_obj.seeker import Seeker
from sneaker_seeker.game_obj.sneaker import Sneaker
from sneaker_seeker.game_obj.DKIZ import DKIZ
from sneaker_seeker.game_obj.ROI import ROI
from sneaker_seeker.visualization.canvas import Canvas
from sneaker_seeker.simulation.simulator import Simulator


def run_scenario(scenario: dict, args: dict, out_path: Path) -> None:
    game_objects = { "roi": ROI(**scenario["ROI"]),  # Region Of Interest of the game of seeking
        "dkiz": DKIZ(**scenario["sneaker"]["deployment"]["DKIZ"]),  # this the Dynamic Keep-In Zone for the Sneakers.
        "visualizer": Canvas(frame_format=args["frames_format"], **scenario["world"], **scenario["canvas"]),
        "sneakers": [Sneaker(**scenario["sneaker"]["common_data"]) for _ in range(scenario["sneaker"]["num"])],
        "seekers": [Seeker(**scenario["seeker"]["common_data"]) for _ in range(scenario["seeker"]["num"])]
    }
    path_planners = {Seeker: PathPlannerFactory.create(scenario["seeker"]["path_planner"], **game_objects),
                     Sneaker: PathPlannerFactory.create(scenario["sneaker"]["path_planner"], **game_objects)}
    simulator = Simulator(out_path=out_path, scenario=scenario, path_planners=path_planners, **game_objects)
    simulator.run(save_frame_every_n_step=args["save_frame_every_n_step"])


@utils.my_timer
# @utils.my_profiler
def main(debug_input=None) -> None:
    args = utils.parse_args_to_dict(debug_input)
    for scenario_json_path in args["scenario"]:
        scenario = utils.read_json(str(scenario_json_path))
        out_path = utils.make_output_path(outputdir=args["out_path"], scenario_name=scenario["name"])
        utils.scale_world(scenario, args["scale_world_factor"])
        run_scenario(scenario, args, out_path)
        vid_path = utils.make_video(frames_dir=out_path, frames_format=args["frames_format"],
                                    video_name=f"{scenario['name']}.avi", keep_frames=args["keep_frames"],
                                    fps=(args["speed_up_video"] * utils.real_time_fps(scenario['time_step_ms'],
                                                                                      args["save_frame_every_n_step"])))
        if args["play_video"]:
            subprocess.run(['start', str(vid_path)], shell=True)


if __name__ == "__main__":
    debug = [
        "--scenario", r"C:\Users\shali\OneDrive\code\python\SneakerSeeker\sneaker_seeker_app\scenarios\scenario01.json",
        "--out_path", r"C:\Users\shali\Desktop",
        "--scale_world_factor", "1",
        "--speed_up_video", "10",
        "--save_frame_every_n_step", "5",
        "--play_video",
        # "--keep_frames"
    ]
    main(debug)
