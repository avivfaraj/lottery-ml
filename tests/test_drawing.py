import sys

sys.path.append("..")
from src.lottery.utils.drawing import Drawing, CountError
from src.lottery.utils.ball import WHITEBALL_BG, RESET
from src.lottery.utils.powerball import POWERBALL_BG
import pytest


@pytest.fixture
def drawing_1():
    return Drawing("2023-06-10")


@pytest.fixture
def drawing_2():
    drawing2 = Drawing("2023-06-11")
    drawing2.add_winning_ls([1, 20, 50, 30, 40])
    drawing2.add_winning_number(2, True)
    return drawing2


# Testing adding functions
def test_add_winning_number(drawing_1):
    drawing_1.add_winning_number(10, False)
    assert drawing_1.winning_numbers_ls[0].number == 10


def test_adding_winning_list(drawing_1):
    drawing_1.add_winning_ls([1, 40, 30, 25, 4])
    assert len(drawing_1.winning_numbers_ls) == 5


# Testing print function
def test_print(capsys, drawing_2):
    # Print drawing results to stdout
    drawing_2.print()

    # Read stdout
    captured = capsys.readouterr()

    # '\n' kept raising an error, so removed it from string.
    assert captured.out.replace("\n", "") == (
        f"Drawing Date: 2023-06-11 Winning numbers:  {WHITEBALL_BG}1{RESET} {WHITEBALL_BG}20{RESET} {WHITEBALL_BG}50{RESET} {WHITEBALL_BG}30{RESET} {WHITEBALL_BG}40{RESET} {POWERBALL_BG}2{RESET}"  # noqa: E501
    )


# Testing errors
def test_type_error_float(drawing_1):
    with pytest.raises(TypeError):
        drawing_1.add_winning_number(1.1, False)


def test_type_error_str(drawing_1):
    with pytest.raises(TypeError):
        drawing_1.add_winning_number("s", True)


def test_count_error_whiteball(drawing_2):
    with pytest.raises(CountError):
        drawing_2.add_winning_number(1, False)


def test_count_error_powerball(drawing_2):
    with pytest.raises(CountError):
        drawing_2.add_winning_number(1, True)


def test_count_error_list(drawing_1):
    with pytest.raises(CountError):
        drawing_1.add_winning_ls([1, 2, 3, 4, 5, 6])
