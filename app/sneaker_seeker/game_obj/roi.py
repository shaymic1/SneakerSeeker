import matplotlib


class Roi:
    def __init__(self, **kwargs) -> None:
        self.rectangle = matplotlib.patches.Rectangle(**kwargs, xy=(kwargs["x"], kwargs["y"]))

