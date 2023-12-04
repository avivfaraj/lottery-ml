from abc import ABC, abstractmethod
import enum


WHITEBALL_BG = "\033[30;47m"
RESET = "\033[0m"


class BallType(enum.Enum):
    Whiteball = {"low": 1, "high": 69}
    Powerball = {"low": 1, "high": 26}
    Megaball = {"low": 1, "high": 25}


class Ball(ABC):
    def __getattr__(self, name: str):
        return self.__dict__[f"_{name}"]

    def __setattr__(self, name, value):
        if name == "number":
            # num, reg_h, reg_l, uniq_h, uniq_l = value
            self.__dict__[f"_{name}"] = self.set_number(value)
        elif name == "type_":
            self.__dict__[f"_{name}"] = self.set_type_(value)
        elif name == "index":
            self.__dict__[f"_{name}"] = self.set_index(value)
        else:
            self.__dict__[f"_{name}"] = value

    def set_number(self, number: int) -> int:
        # Ensure input type is int
        if isinstance(number, int):
            if self.type_:
                # Unpack dictionary
                low, high = self.type_.value.values()
                type_ = self.type_.name
                # Range for power ball is between 1 and 26 - otherwise raise an error
                if number > high or number < low:
                    raise ValueError(f"{type_} must be between {low} and {high} (inclusive)")
                else:
                    return number

        # Raise type error when input is not int.
        else:
            raise TypeError("Number must be an integer!")

    def is_unique_ball(self) -> bool:
        if self.type_.name == "Whiteball":
            return False

        return True

    @abstractmethod
    def set_index(self, index: int) -> int:
        pass

    @abstractmethod
    def set_type_(self):
        pass

    def format_str(self, ansi_color: str) -> str:
        return f"{ansi_color}{self.number}{RESET}"

    def __str__(self) -> str:
        return f"{WHITEBALL_BG}{self.number}{RESET}"
