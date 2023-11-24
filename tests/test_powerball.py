import sys

sys.path.append("..")
from src.lottery.webscraping.powerball import ScrapePowerBall
import pytest
import os


# Run test manualy (local)
@pytest.mark.webtest
def test_load_30_drawings():
    with ScrapePowerBall() as spb:
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
        assert len(count) == 30


@pytest.mark.webtest
def test_load_60_drawings():
    with ScrapePowerBall() as spb:
        # pre-scraping
        assert len(spb.cards_ls) == 0

        # Loading 2 iteration (should be 60 cards)
        spb.load_drawings(num=2)
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
