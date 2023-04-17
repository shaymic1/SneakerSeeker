from .path_planner import PathPlanner
from .path_planner_random_walk import PathPlannerRandomWalk
from .path_planner_strainght_line import PathPlannerStraightLine


class PathPlannerFactory:
    @staticmethod
    def create(planner_type: str, **kwargs) -> PathPlanner:
        if planner_type == 'straight_line':
            return PathPlannerStraightLine(**kwargs)
        elif planner_type == 'random_walk':
            return PathPlannerRandomWalk(**kwargs)
        else:
            raise ValueError(f'Invalid planner_type: {planner_type}')
