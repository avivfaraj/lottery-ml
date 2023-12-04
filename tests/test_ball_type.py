from src.lottery.utils.ball import BallType
import pytest


@pytest.fixture
def whiteball():
    return BallType.Whiteball


@pytest.fixture
def powerball():
    return BallType.Powerball


@pytest.fixture
def megaball():
    return BallType.Megaball


def test_whiteball_low(whiteball):
    assert whiteball.value["low"] == 1


def test_whiteball_high(whiteball):
    assert whiteball.value["high"] == 69


def test_powerball_low(powerball):
    assert powerball.value["low"] == 1


def test_powerball_high(powerball):
    assert powerball.value["high"] == 26


def test_megaball_low(megaball):
    assert megaball.value["low"] == 1


def test_megaball_high(megaball):
    assert megaball.value["high"] == 25
