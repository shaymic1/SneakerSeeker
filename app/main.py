from pathlib import Path

from sneaker_seeker import utils
from sneaker_seeker.simulation.simulator import Simulator
from sneaker_seeker.visualization.canvas import Canvas
from sneaker_seeker.game_obj.seeker import Seeker
from sneaker_seeker.game_obj.sneaker import Sneaker


SCENARIO_NAME = "scenario01"


def main() -> None:
    config = utils.read_json("config.json")
    scenario = utils.read_json(f"scenarios/{SCENARIO_NAME}.json")
    out_path = utils.make_output_path(config["outputdir"], SCENARIO_NAME, empty_output_path=True)

    simulator = Simulator(scenario=scenario,
                          visualizer=Canvas(**scenario["canvas"]),
                          seekers=[Seeker(**scenario["seeker"]) for _ in range(scenario["seekers_num"])],
                          sneakers=[Sneaker(**scenario["sneaker"]) for _ in range(scenario["sneakers_num"])])

    simulator.run(out_path=Path(out_path/SCENARIO_NAME))

    utils.make_video(frames_dir=out_path, video_name=f"{SCENARIO_NAME}.avi", fps=1000//scenario['time_step_ms'])



if __name__ == "__main__":
    main()



