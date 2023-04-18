from matplotlib.patches import Circle


class DKIZ:
    """this is the Dynamic Keep-in Zone of the sneakers"""

    __shapes = {"circle": Circle}

    def __init__(self, shape: dict, location: dict, **args: dict) -> None:
        self.name = shape["name"]
        self.shape = DKIZ.__shapes[name](**args["appearance"], **shape[name], xy=(location["x"], location["y"]))
