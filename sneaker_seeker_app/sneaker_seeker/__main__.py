import subprocess

from sneaker_seeker.utilities import utils
from sneaker_seeker.path_planner.path_planner_factory import PathPlannerFactory
from sneaker_seeker.deployer.deployer_factory import DeployerFactory
from sneaker_seeker.game_obj.seeker import Seeker
from sneaker_seeker.game_obj.sneaker import Sneaker
from sneaker_seeker.game_obj.dkiz import DKIZ
from sneaker_seeker.game_obj.roi import ROI
from sneaker_seeker.visualization.canvas import Canvas
from sneaker_seeker.simulation.simulator import Simulator


def construct_scenario_objs(args, scenario) -> dict:
    game_objects = {
        "roi": ROI.from_dict(**scenario["ROI"]),  # Region Of Interest of the game of seeking
        "dkiz": DKIZ.from_dict(**scenario["dkiz"]),
        "visualizer": Canvas(frame_format=args["frames_format"], **scenario["board"], **scenario["canvas"]),
        "sneakers": [Sneaker.from_dict(**scenario["sneaker"]["data"]) for _ in range(scenario["sneaker"]["num"])],
        "seekers": [Seeker.from_dict(**scenario["seeker"]["data"]) for _ in range(scenario["seeker"]["num"])]
    }

    sneaker_deployer_type = scenario["sneaker"]["deployer"]
    seeker_deployer_type = scenario["seeker"]["deployer"]
    game_objects["deployers"] = {
        Seeker: DeployerFactory.create(
            seeker_deployer_type, **scenario["deployers"][seeker_deployer_type], **game_objects),
        Sneaker: DeployerFactory.create(
            sneaker_deployer_type, **scenario["deployers"][sneaker_deployer_type], **game_objects)
    }

    sneaker_path_planner_type = scenario["sneaker"]["path_planner"]
    seeker_path_planner_type = scenario["seeker"]["path_planner"]
    game_objects["path_planners"] = {
        Seeker: PathPlannerFactory.create(
            seeker_path_planner_type, **scenario["path_planners"][seeker_path_planner_type], **game_objects),
        Sneaker: PathPlannerFactory.create(
            sneaker_path_planner_type, **scenario["path_planners"][sneaker_path_planner_type], **game_objects)
    }
    return game_objects


@utils.my_timer
# @utils.my_profiler
def main(debug_input=None) -> None:
    args = utils.parse_args_to_dict(debug_input)
    for scenario_json_path in args["scenarios"]:
        scenario = utils.read_json(str(scenario_json_path))
        out_path = utils.make_output_path(outputdir=args["out_path"], scenario_name=scenario_json_path.stem)
        utils.scale_world(scenario, args["scale_world_factor"])

        sim = Simulator(out_path, **construct_scenario_objs(args, scenario))
        sim.run(scenario["time_step_ms"], scenario["time_goal_ms"], args["save_frame_every_n_step"])

        vid_path = utils.make_video(
            frames_dir=out_path, frames_format=args["frames_format"], video_name=scenario_json_path.stem,
            keep_frames=args["keep_frames"], video_format="mp4",
            fps=(args["speed_up_video"] * utils.real_time_fps(scenario['time_step_ms'],
                                                              args["save_frame_every_n_step"]))
        )
        if args["play_video"]:
            subprocess.run(['start', str(vid_path)], shell=True)


if __name__ == "__main__":
    debug_args = [
        "--scenarios",
        r"C:\Users\shali\OneDrive\code\python\SneakerSeeker\sneaker_seeker_app\scenarios\debug.json",
        # r"C:\Users\shali\OneDrive\code\python\SneakerSeeker\sneaker_seeker_app\scenarios\up_left.json",
        # r"C:\Users\shali\OneDrive\code\python\SneakerSeeker\sneaker_seeker_app\scenarios\enough_time.json",
        # r"C:\Users\shali\OneDrive\code\python\SneakerSeeker\sneaker_seeker_app\scenarios\middle.json",
        # r"C:\Users\shali\OneDrive\code\python\SneakerSeeker\sneaker_seeker_app\scenarios\come_from_above.json",
        # r"C:\Users\shali\OneDrive\code\python\SneakerSeeker\sneaker_seeker_app\scenarios\massive_attack.json",
        "--out_path", r"D:\output",
        "--scale_world_factor", "1",
        "--speed_up_video", "5",
        "--save_frame_every_n_step", "10",
        "--play_video",
        # "--keep_frames"
    ]
    main(debug_args)
