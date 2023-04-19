from sneaker_seeker.common_types.point2d import Point2D
import matplotlib
from matplotlib.patches import Circle
from .movable import Movable


class DKIZ(Movable):
    """this is the Dynamic Keep-in Zone of the sneakers"""

    __shapes = {"circle": Circle}

    def __init__(self, shape: dict, location: dict = None, speed: dict = None, **args: dict) -> None:
        super().__init__(location, speed)
        self.type: str = shape["type"]
        self.dimensions: dict = shape[self.type]
        self.max_dist_from_center = max(self.dimensions.values())
        self.shape: matplotlib.patches = DKIZ.__shapes[self.type](**args["appearance"], **shape[self.type],
                                                                  xy=(location["x"], location["y"]))

    def contains(self, other_location: Point2D):
        if self.type == 'circle':
            return self.location.dist(other_location) < self.dimensions['radius']
