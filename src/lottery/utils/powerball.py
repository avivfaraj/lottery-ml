try:
    from .ball import Ball, BallType
except ImportError:
    from ball import Ball, BallType


POWERBALL_BG = "\033[37;41m"


class Powerball(Ball):
    def __init__(self, index: int, number: int, is_power_ball: bool = False):
        self.type_ = is_power_ball
        self.index = index
        self.number = number

    def set_type_(self, is_power_ball: bool):
        if is_power_ball:
            return BallType.Powerball

        return BallType.Whiteball

    def set_index(self, index: int) -> int:
        # Power Ball - has no index
        if super().is_unique_ball():
            return -1

        # White ball - store index
        return index

    def __str__(self):
        if super().is_unique_ball():
            return super().format_str(POWERBALL_BG)

        return super().__str__()
