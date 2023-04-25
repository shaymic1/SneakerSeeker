from sneaker_seeker.game_obj.movable import Movable


class ROI(Movable):
    """this is the game Region Of Interest. the sneaking game should occur inside.
       +------------------+
       |                  |
     height               |
       |                  |
     (x,y)-----width------|
    """
    def __init__(self, location: dict, height: int, width: int, speed: dict = None) -> None:
        super().__init__(location, speed)
        self.height = height
        self.width = width
