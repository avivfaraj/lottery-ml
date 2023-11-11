import sys
sys.path.append("..")
from src.lottery.utils.ball import Ball
import pytest


@pytest.fixture
def whiteball():
    ball = Ball(1, 10, False)
    return ball


@pytest.fixture
def powerball():
    ball = Ball(-1, 23, True)
    return ball


# Testing whiteball:
# numbers must be between 1 and 69!
def test_ball_is_white(whiteball):
    assert not whiteball.power_ball


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


# Testing powerball:
# numbers must be between 1 and 26!
def test_ball_is_powerball(powerball):
    assert powerball.power_ball


def test_whiteball_is_less_than_26(powerball):
    # Setting number to 26 - no error
    powerball.number = 26

    # Setting number to 27 - value error
    with pytest.raises(ValueError):
        powerball.number = 27


def test_powerball_is_more_than_0(powerball):
    with pytest.raises(ValueError):
        powerball.number = 0


def test_powerball_invalid_number(powerball):
    with pytest.raises(TypeError):
        powerball.number = "1"
