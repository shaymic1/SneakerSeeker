import os
from pathlib import Path
from sneaker_seeker import utils
from sneaker_seeker.simulation.simulator import Simulator
from sneaker_seeker.visualization.canvas import Canvas
from sneaker_seeker.game_obj.seeker import Seeker
from sneaker_seeker.game_obj.sneaker import Sneaker


SCENARIO_NAME = "scenario01"


def main() -> None:
    config = utils.read_json("config.json")
    out_path = utils.make_output_path(config["outputdir"], SCENARIO_NAME)

    scenario = utils.read_json(f"scenarios/{SCENARIO_NAME}.json")
    canvas = Canvas(**scenario["canvas"])
    seekers = [Seeker(**scenario["seeker"]) for _ in range(scenario["seekers_num"])]
    sneakers = [Sneaker(**scenario["sneaker"]) for _ in range(scenario["sneakers_num"])]

    simulator = Simulator(scenario=scenario, visualizer=canvas, seekers=seekers, sneakers=sneakers)

    simulator.run(out_path)


if __name__ == "__main__":
    main()
