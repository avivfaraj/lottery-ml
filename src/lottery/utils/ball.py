WHITEBALL_BG="\033[30;47m"
POWERBALL_BG="\033[37;41m"
RESET="\033[0m"


class Ball():

    def __init__(self, index: int, number: int, is_power_ball: bool = False):

        self.power_ball = is_power_ball
        self.index = index
        self.number = number

    def __getattr__(self, name: str):
        return self.__dict__[f"_{name}"]

    def __setattr__(self, name, value):
        if name == "number":
            self.__dict__[f"_{name}"] = self.set_number(value)
        elif name == "index":
            self.__dict__[f"_{name}"] = self.set_index(value)
        else:
            self.__dict__[f"_{name}"] = value

    def set_number(self, number: int) -> int:

        # Ensure input type is int
        if isinstance(number,int):

            # Ensure power ball
            if self.power_ball:

                # Range for power ball is between 1 and 26 - otherwise raise an error
                if number > 26 or number < 1:
                    raise ValueError("Power ball must be between 1 and 26 (inclusive)")
                else:
                    return number

            # White ball
            else:

                # Range for white ball is between 1 and 69 - otherwise raise an error
                if number > 69 or number < 1:
                    raise ValueError("White ball must be between 1 and 69 (inclusive)")
                else:
                    return number

        # Raise type error when input is not int.
        else:
            raise TypeError("Number must be an integer!")

    def set_index(self, index: int) -> int:

        # Power Ball - has no index
        if self.power_ball:
            return -1

        # White ball - store index
        return index

    def __str__(self):
        return f"{POWERBALL_BG if self.power_ball else WHITEBALL_BG}{self.number}{RESET}"
