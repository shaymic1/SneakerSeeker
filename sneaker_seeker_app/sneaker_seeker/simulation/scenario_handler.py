from sneaker_seeker.path_planner.path_planner_factory import PathPlannerFactory
from sneaker_seeker.deployer.deployer_factory import DeployerFactory
from sneaker_seeker.game_obj.seeker import Seeker
from sneaker_seeker.game_obj.sneaker import Sneaker
from sneaker_seeker.game_obj.dkiz import DKIZ
from sneaker_seeker.game_obj.roi import ROI
from sneaker_seeker.visualization.canvas import Canvas


def construct_scenario_objs(scenario) -> dict:
    game_objects = {
        "roi": ROI.from_dict(**scenario["ROI"]),  # Region Of Interest of the game of seeking
        "dkiz": DKIZ.from_dict(**scenario["dkiz"]),
        "visualizer": Canvas(**scenario["board"], **scenario["canvas"]),
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
