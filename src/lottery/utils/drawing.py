# Prevent relative import error
try:
    from .powerball import Powerball
    from .megaball import Megaball
except ImportError:
    from powerball import Powerball
    from megaball import Megaball

import enum
from typing import List

# Regular winner numbers constant
WHITEBALL_COUNT = 5

DRAWING_TYPE_DICT = {
    "powerball": Powerball,
    # TODO: Implement Megaball class
    "megaball": Megaball,
}


# Define count error - there are 5 white balls and 1 powerball in each drawing.
class CountError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Drawing:
    def __init__(self, drawing_type: str, date: str, estimated_jackpot: int = -1):
        self.drawing_type = self.set_drawing_type(drawing_type)
        self.winning_numbers_ls = []
        self.date = date
        self.estimated_jackpot = estimated_jackpot

    def set_drawing_type(self, drawing_type: str) -> str:
        if drawing_type.lower() not in DRAWING_TYPE_DICT.keys():
            raise ValueError(f"{drawing_type} Drawing Does Not Exist!")

        return drawing_type.lower()

    def ensure_data_is_valid(self, number: int, is_power_ball: bool) -> None:
        """
        Ensure balls count (white and powerball) is within
        acceptable limit (5 and 1 respectively)

        Parameters
        ----------
            is_power_ball - boolean
                True if the number to be add is a powerball.

        Raise
        -----
            CountError - when number of whiteballs exceeds 5
                         or number of powerball exceeds 1.

            TypeError - when the number is not integer!
        """
        if not isinstance(number, int):
            raise TypeError("Winning number must be an integer!")

        whiteball_count = sum(
            [1 if i.type_.name == "Whiteball" else 0 for i in self.winning_numbers_ls]
        )
        powerball_count = sum(
            [1 if i.type_.name == "Powerball" else 0 for i in self.winning_numbers_ls]
        )

        if powerball_count == 1 and is_power_ball:
            raise CountError("Current drawing already has a powerball! (max)")

        if whiteball_count == 5 and not is_power_ball:
            raise CountError("Current drawing already has 5 (max) whiteballs!")

    def add_winning_number(self, number: int, is_power_ball: bool):
        """
        Adding one winning number to the drawing.
        The winning number can be either whiteball or powerball,
        depends on is_power_ball value.

        Parameters
        ----------
            is_power_ball - boolean
                True if the number to be add is a powerball.

        Returns
        -------
            Nothing is returned, but raises CountError if count is invalid.
        """
        self.ensure_data_is_valid(number, is_power_ball)
        index = len(self.winning_numbers_ls) + 1
        ball = DRAWING_TYPE_DICT[self.drawing_type](index, number, is_power_ball)
        self.winning_numbers_ls.append(ball)

    def add_winning_ls(self, winners_ls: List[int]) -> None:
        """
        Adding a list of winning numbers (whiteballs) to the current drawing.

        Parameters
        ----------
            winner_ls - List[int]
                list of winning numbers (white balls)
        """
        for number in winners_ls:
            self.add_winning_number(number, False)

    def print(self) -> None:
        """
        Prints drawing details to stdout.
        """
        # Final string that includes the winning numbers.
        str_ = f"Drawing Date: {self.date} \nWinning numbers: "

        # Store power ball number in case
        # it is not the last element in the list.
        power_ball = ""

        # Iterating over winning numbers
        for ball in self.winning_numbers_ls:
            # Ensure power ball is listed at the end!
            if ball.type_.name == "Powerball":
                power_ball = f" {ball}"

            # White balls are appended to the list as they are read.
            else:
                str_ += f" {ball}"

        # Append power ball at the end.
        str_ += f"{power_ball}"

        print(str_)

    def get_winning_ls(self) -> List[str]:
        _ = [ball.number for ball in self.winning_numbers_ls]
        _.insert(0, self.date)
        if self.estimated_jackpot != -1:
            _.append(self.get_formatted_jackpot())
        return _

    def get_formatted_jackpot(self) -> str:
        if self.estimated_jackpot != -1:
            return f"{self.estimated_jackpot:,d}"

        return "Jackpot is missing (was not scraped)"
