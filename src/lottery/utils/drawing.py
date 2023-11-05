# Prevent relative import error
try:
    from .ball import Ball
except ImportError:
    from ball import Ball

# Regular winner numbers constant
WHITEBALL_COUNT = 5

# Define count error - there are 5 white balls, so count must match.
class CountError(Exception):
    def __init__(self, count, message=""):
        self.count = count
        self.message = message
        if not self.message:
            if count > WHITEBALL_COUNT:
                self.message = f"Too many white balls ({self.count}). There are only 5 in each drawing!"

            if count < WHITEBALL_COUNT:
                self.message = f"Missing white balls (got {self.count} instead of 5)."

        super().__init__(self.message)

class Drawing():

    def __init__(self, date):
        self.winning_numbers_ls = []
        self.date = date

    def add_winning_number(self, number, is_power_ball):
        index = len(self.winning_numbers_ls) + 1
        ball = Ball(index, number, is_power_ball)
        self.winning_numbers_ls.append(ball)

    def add_winning_ls(self, winners_ls):
        total_winners = len(winners_ls) + len(self.winning_numbers_ls)
        if not total_winners == WHITEBALL_COUNT:
            raise CountError(total_winners)

        for number in winners_ls:
            index = len(self.winning_numbers_ls) + 1
            ball = Ball(index, number, False)
            self.winning_numbers_ls.append(ball)

    def print(self):
        str_ = ""
        for ball in self.winning_numbers_ls:
            str_ += f" {ball}"
        print(str_)

if __name__=="__main__":
    test = Drawing("2023-06-20")
    test.add_winning_ls([6,12,10,30, 45 , 60])
    # test.add_winning_number(6, False)
    # test.add_winning_number(12, False)
    # test.add_winning_number(10, False)
    # test.add_winning_number(30, False)
    # test.add_winning_number(45, False)
    # test.add_winning_number(3, True)
    test.print()
