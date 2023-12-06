import sys

sys.path.append("..")
from src.lottery.utils.megaball import Megaball
import pytest


@pytest.fixture
def whiteball():
    ball = Megaball(1, 10, False)
    return ball


@pytest.fixture
def megaball():
    ball = Megaball(-1, 23, True)
    return ball


# Testing whiteball:
# numbers must be between 1 and 69!
def test_ball_is_white(whiteball):
    assert whiteball.type_.name == "Whiteball"


def test_whiteball_is_less_than_70(whiteball):
    # Setting number to 69 - no error
    whiteball.number = 69

    with pytest.raises(ValueError):
        whiteball.number = 70


def test_whiteball_is_more_than_0(whiteball):
    # Setting number to 1 - no error
    whiteball.number = 1

    with pytest.raises(ValueError):
        whiteball.number = 0


def test_whiteball_invalid_number(whiteball):
    with pytest.raises(TypeError):
        whiteball.number = "1"


# Testing megaball:
# numbers must be between 1 and 25!
def test_ball_is_megaball(megaball):
    assert megaball.type_.name == "Megaball"


def test_megaball_is_less_than_25(megaball):
    # Setting number to 25 - no error
    megaball.number = 25

    # Setting number to 26 - value error
    with pytest.raises(ValueError):
        megaball.number = 26


def test_megaball_is_more_than_0(megaball):
    with pytest.raises(ValueError):
        megaball.number = 0


def test_megaball_invalid_number(megaball):
    with pytest.raises(TypeError):
        megaball.number = "1"
