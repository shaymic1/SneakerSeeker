from .path_planner import PathPlanner
from .path_planner_random_walk import PathPlannerRandomWalk
from .path_planner_strainght_line import PathPlannerStraightLine


class PathPlannerFactory:
    __path_planners = {'straight_line': PathPlannerStraightLine,
                       'random_walk': PathPlannerRandomWalk}

    @staticmethod
    def create(planner_type: str, **kwargs) -> PathPlanner:
        if planner_type not in PathPlannerFactory.__path_planners:
            raise ValueError(f'Invalid planner_type: {planner_type}')
        return PathPlannerFactory.__path_planners[planner_type](**kwargs)

    @staticmethod
    def add_path_planner(self, planner_type: str, planner) -> None:
        PathPlannerFactory.__path_planners[planner_type] = planner
