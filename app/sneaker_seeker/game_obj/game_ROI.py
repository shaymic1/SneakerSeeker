import matplotlib


class ROI:
    """this is the game Region Of Interest"""
    def __init__(self, **kwargs) -> None:
        self.rectangle = matplotlib.patches.Rectangle(**kwargs, xy=(kwargs["x"], kwargs["y"]))
