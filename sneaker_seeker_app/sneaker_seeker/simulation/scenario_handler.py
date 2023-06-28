from sneaker_seeker.path_planner.path_planner import PathPlanner
from sneaker_seeker.path_planner.path_planner_factory import PathPlannerFactory
from sneaker_seeker.deployer.deployer_factory import DeployerFactory
from sneaker_seeker.deployer.deployer import Deployer
from sneaker_seeker.game_obj.seeker import Seeker
from sneaker_seeker.game_obj.sneaker import Sneaker
from sneaker_seeker.game_obj.dkiz import DKIZ
from sneaker_seeker.game_obj.roi import ROI
from sneaker_seeker.visualization.canvas import Canvas


def create_seekers_groups(scenario: dict) -> list[list[Seeker]]:
    groups: list[list[Seeker]] = []
    for group in scenario['seeker']['groups']:
        groups.append([Seeker.from_dict(**group["data"]) for _ in range(group['num'])])
    return groups


def create_sneakers_groups(scenario: dict) -> list[list[Sneaker]]:
    groups: list[list[Sneaker]] = []
    for group in scenario['sneaker']['groups']:
        groups.append([Sneaker.from_dict(**group["data"]) for _ in range(group['num'])])
    return groups


def create_seekers_deployers(scenario: dict, **game_objs) -> list[Deployer]:
    deployers: list[Deployer] = []
    for group in scenario['seeker']['groups']:
        deployers.append(
            DeployerFactory.create(group["deployer"]["type"], **group["deployer"]["data"], **game_objs)
        )
    return deployers


def create_seekers_path_planners(scenario: dict, **game_objs) -> list[PathPlanner]:
    path_planners: list[PathPlanner] = []
    for group in scenario['seeker']['groups']:
        path_planners.append(
            PathPlannerFactory.create(group["path_planner"]["type"], **group["path_planner"]["data"], **game_objs))
    return path_planners


def create_sneakers_deployers(scenario: dict, **game_objs) -> list[Deployer]:
    deployers: list[Deployer] = []
    for group in scenario['sneaker']['groups']:
        deployers.append(
            DeployerFactory.create(group["deployer"]["type"], **group["deployer"]["data"], **game_objs)
        )
    return deployers


def create_sneakers_path_planner(scenario: dict, **game_objs) -> list[PathPlanner]:
    path_planners: list[PathPlanner] = []
    for group in scenario['sneaker']['groups']:
        path_planners.append(
            PathPlannerFactory.create(group["path_planner"]["type"], **group["path_planner"]["data"], **game_objs))
    return path_planners


def construct_scenario_objs(scenario: dict, visualizer_on: bool = True) -> dict:
    game_objects = {
        "roi": ROI.from_dict(**scenario["ROI"]),  # Region Of Interest of the game of seeking
        "dkiz": DKIZ.from_dict(**scenario["dkiz"]),
        "visualizer": Canvas(**scenario["board"], **scenario["canvas"]) if visualizer_on else None,
        "sneakers": create_sneakers_groups(scenario),
        "seekers": create_seekers_groups(scenario)
    }

    game_objects["deployers"] = {
        Seeker: create_seekers_deployers(scenario, **game_objects),
        Sneaker: create_sneakers_deployers(scenario, **game_objects)
    }
    game_objects["path_planners"] = {
        Seeker: create_seekers_path_planners(scenario, **game_objects),
        Sneaker: create_sneakers_path_planner(scenario, **game_objects)
    }

    return game_objects
