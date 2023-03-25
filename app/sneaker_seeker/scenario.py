from pydantic import BaseModel, PositiveInt, PositiveFloat


class Scenario(BaseModel):
    __slots__ = {
        "seekers_num",
        "sneakers_num",
        "time_goal",
        "board_width",
        "board_height"
    }

    seekers_num: PositiveInt
    sneakers_num: PositiveInt
    time_goal: PositiveFloat
    board_width: PositiveFloat
    board_height: PositiveFloat


