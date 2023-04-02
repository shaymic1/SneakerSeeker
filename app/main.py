from pathlib import Path

from sneaker_seeker import utils
from sneaker_seeker.simulation.simulator import Simulator
from sneaker_seeker.visualization.canvas import Canvas
from sneaker_seeker.game_obj.seeker import Seeker
from sneaker_seeker.game_obj.sneaker import Sneaker

SCENARIO_NAME = "scenario01"
SAVE_EVERY_N_FRAME = 10
VIDEO_X_SPEED = 1


@utils.my_timer
def main() -> None:
    config = utils.read_json("config.json")
    scenario = utils.read_json(f"scenarios/{SCENARIO_NAME}.json")
    out_path = utils.make_output_path(config["outputdir"], SCENARIO_NAME, empty_output_path=True)

    simulator = Simulator(scenario=scenario,
                          visualizer=Canvas(**scenario["canvas"]),
                          seekers=[Seeker(**scenario["seeker"]) for _ in range(scenario["seekers_num"])],
                          sneakers=[Sneaker(**scenario["sneaker"]) for _ in range(scenario["sneakers_num"])])

    simulator.run(out_path=Path(out_path / SCENARIO_NAME), save_every_n_frames=SAVE_EVERY_N_FRAME)

    # keeps the FPS so that the video time will allways be at normal speed.
    fps = (1000 * VIDEO_X_SPEED) // (scenario['time_step_ms'] * SAVE_EVERY_N_FRAME)
    utils.make_video(frames_dir=out_path, video_name=f"{SCENARIO_NAME}.avi", fps=fps)


if __name__ == "__main__":
    main()
