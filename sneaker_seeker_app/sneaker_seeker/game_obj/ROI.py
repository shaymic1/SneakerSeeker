class ROI:
    """this is the game Region Of Interest. the sneaking game should occur inside."""

    def __init__(self, x: int, y: int, height: int, width: int) -> None:
        self.x = x
        self.y = y
        self.height = height
        self.width = width
