from sneaker_seeker import utils
from sneaker_seeker.path_planner import PathPlannerFactory
from sneaker_seeker.simulation import Simulator
from sneaker_seeker.visualization import Canvas
from sneaker_seeker.game_obj import Roi, Sneaker, Seeker

SCENARIO_NAME = "scenario01"
SAVE_FRAME_EVERY_N_STEP = 5
VID_SPEEDUP_FACTOR = 1


@utils.my_timer
def main() -> None:
    config = utils.read_json("config.json")
    scenario = utils.read_json(f"scenarios/{SCENARIO_NAME}.json")
    out_path = utils.make_output_path(outputdir=config["outputdir"], scenario_name=SCENARIO_NAME,
                                      empty_output_path=True)

    game_objects = {"roi": Roi(**scenario["roi"]),
                    "visualizer": Canvas(**scenario["canvas"]),
                    "seekers": [Seeker(**scenario["seeker"]) for _ in range(scenario["seekers_num"])],
                    "sneakers": [Sneaker(**scenario["sneaker"]) for _ in range(scenario["sneakers_num"])]}

    path_planners = {Seeker: PathPlannerFactory.create(scenario["seekers_path_planner"], **game_objects),
                     Sneaker: PathPlannerFactory.create(scenario["sneakers_path_planner"], **game_objects)}

    simulator = Simulator(out_path=out_path, scenario=scenario, path_planners=path_planners, **game_objects)
    simulator.run(save_frame_every_n_step=SAVE_FRAME_EVERY_N_STEP)

    utils.make_video(frames_dir=out_path, video_name=f"{SCENARIO_NAME}.avi",
                     fps=(VID_SPEEDUP_FACTOR * utils.real_time_fps(scenario['time_step_ms'], SAVE_FRAME_EVERY_N_STEP)))


if __name__ == "__main__":
    main()
