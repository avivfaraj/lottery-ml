import sys

sys.path.append("..")
from src.lottery.webscraping.powerball import ScrapePowerBall

# from src.lottery.utils.ball import WHITEBALL_BG, POWERBALL_BG, RESET
import pytest
import os


@pytest.fixture
def spb():
    return ScrapePowerBall()


@pytest.fixture
def spb_2():
    return ScrapePowerBall()


# Run test manualy (local)
@pytest.mark.webtest
def test_load_30_drawings(spb):
    # pre-scraping
    assert len(spb.cards_ls) == 0

    # Loading 1 iteration (should be 30 cards)
    spb.load_drawings(num=1)
    spb.scrape_drawings()
    spb.to_csv("./", "test")
    with open("./test.csv", "r") as file:
        content = file.read()

    # Remove headers
    count = content.split("\n")[1:]

    # remove empty rows
    count = [i for i in count if i]

    os.remove("./test.csv")

    # post-scarping (pre-processing)
    assert len(count) == 60


# Run test manualy (local)
@pytest.mark.webtest
def test_load_60_drawings(spb_2):
    # pre-scraping
    assert len(spb_2.cards_ls) == 0

    # Loading 1 iteration (should be 30 cards)
    spb_2.load_drawings(num=2)
    spb_2.scrape_drawings()
    spb_2.to_csv("./", "test")
    with open("./test.csv", "r") as file:
        content = file.read()

    # Remove headers
    count = content.split("\n")[1:]

    # remove empty rows
    count = [i for i in count if i]

    os.remove("./test.csv")

    # post-scarping (pre-processing)
    assert len(count) == 90
