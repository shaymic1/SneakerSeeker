from sneaker_seeker.path_planner.path_planner import PathPlanner
from sneaker_seeker.path_planner.path_planner_random_walk import PathPlannerRandomWalk
from sneaker_seeker.path_planner.path_planner_strainght_line import PathPlannerStraightLine
from sneaker_seeker.path_planner.path_planner_dkiz import PathPlannerDKIZ
from sneaker_seeker.path_planner.path_planner_heuristic import PathPlannerHeuristic


class PathPlannerFactory:
    __path_planners = {'straight_line': PathPlannerStraightLine,
                       'random_walk': PathPlannerRandomWalk,
                       'dkiz': PathPlannerDKIZ,
                       'heuristic': PathPlannerHeuristic}

    @staticmethod
    def create(planner_type: str, **kwargs) -> PathPlanner:
        if planner_type not in PathPlannerFactory.__path_planners:
            raise ValueError(f'Invalid planner_type: {planner_type}')
        return PathPlannerFactory.__path_planners[planner_type](**kwargs)

    @staticmethod
    def add_path_planner(self, planner_type: str, planner) -> None:
        PathPlannerFactory.__path_planners[planner_type] = planner
