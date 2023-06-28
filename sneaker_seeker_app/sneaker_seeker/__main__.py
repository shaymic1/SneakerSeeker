import subprocess

from sneaker_seeker.utilities import utils
from sneaker_seeker.simulation.simulator import Simulator
from sneaker_seeker.simulation.scenario_handler import construct_scenario_objs


@utils.my_timer
# @utils.my_profiler
def main(debug_input=None) -> None:
    args = utils.parse_args_to_dict(debug_input)
    for scenario_json_path in args["scenarios"]:
        scenario = utils.read_json(str(scenario_json_path))
        out_path = utils.make_output_path(outputdir=args["out_path"], scenario_name=scenario_json_path.stem)
        utils.scale_world(scenario, args["scale_world_factor"])

        sim = Simulator(out_path, **construct_scenario_objs(scenario))
        sim.run(scenario["time_step_ms"], scenario["time_goal_ms"], args["save_frame_every_n_step"])

        vid_path = utils.make_video(
            frames_dir=out_path, frames_format=args["frames_format"], video_name=scenario_json_path.stem,
            keep_frames=args["keep_frames"], video_format="avi",
            fps=(args["speed_up_video"] * utils.real_time_fps(scenario['time_step_ms'],
                                                              args["save_frame_every_n_step"]))
        )
        if args["play_video"]:
            subprocess.run(['start', str(vid_path)], shell=True)


if __name__ == "__main__":
    debug_args = [
        "--scenarios",
        # r"C:\Users\shali\OneDrive\code\python\SneakerSeeker\sneaker_seeker_app\scenarios\debug.json",
        # r"C:\Users\shali\OneDrive\code\python\SneakerSeeker\sneaker_seeker_app\scenarios\up_left.json",
        r"C:\Users\shali\OneDrive\code\python\SneakerSeeker\sneaker_seeker_app\scenarios\enough_time.json",
        # r"C:\Users\shali\OneDrive\code\python\SneakerSeeker\sneaker_seeker_app\scenarios\middle.json",
        # r"C:\Users\shali\OneDrive\code\python\SneakerSeeker\sneaker_seeker_app\scenarios\come_from_above.json",
        # r"C:\Users\shali\OneDrive\code\python\SneakerSeeker\sneaker_seeker_app\scenarios\massive_attack.json",
        "--out_path", r"D:\output",
        "--scale_world_factor", "1",
        "--speed_up_video", "5",
        "--save_frame_every_n_step", "1",
        "--play_video",
        # "--keep_frames"
    ]
    main(debug_args)
