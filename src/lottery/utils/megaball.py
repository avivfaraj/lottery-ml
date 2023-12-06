try:
    from .ball import Ball, BallType
except ImportError:
    from ball import Ball, BallType


MEGABALL_BG = "\033[30;43m"


class Megaball(Ball):
    def __init__(self, index: int, number: int, is_mega_ball: bool = False):
        self.type_ = is_mega_ball
        self.index = index
        self.number = number

    def set_type_(self, is_mega_ball: bool):
        if is_mega_ball:
            return BallType.Megaball

        return BallType.Whiteball

    def set_index(self, index: int) -> int:
        # Power Ball - has no index
        if super().is_unique_ball():
            return -1

        # White ball - store index
        return index

    def __str__(self):
        if super().is_unique_ball():
            return super().format_str(MEGABALL_BG)

        return super().__str__()
