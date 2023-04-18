from matplotlib.patches import Circle
from .movable import Movable


class DKIZ(Movable):
    """this is the Dynamic Keep-in Zone of the sneakers"""

    __shapes = {"circle": Circle}

    def __init__(self, shape: dict, location: dict = None, speed: dict = None, **args: dict) -> None:
        super().__init__(location, speed)
        self.name = shape["name"]
        self.shape = DKIZ.__shapes[self.name](**args["appearance"], **shape[self.name],
                                              xy=(location["x"], location["y"]))
