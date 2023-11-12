import sys
sys.path.append("..")
from utils.drawing import Drawing
from selenium import webdriver
# TODO: use Keys to press "Load More" button
from selenium.webdriver.common.keys import Keys  # noqa: F401
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from typing import Any
from selenium.webdriver.remote.webelement import WebElement

OPTIONS = FirefoxOptions()
OPTIONS.add_argument("--headless")
WEBSITE_TO_SCRAPE = "https://www.powerball.com/previous-results?gc=powerball"


class ScrapePowerBall():

    def __init__(self, end_date: str = ""):
        self.end_date = end_date

        # pre-processing (raw results from web scraping)
        self.cards_ls = []

        # post-processing results
        self.drawings_ls = []

        # TODO: Replace DRIVER constant with protected variable
        #       to allow choosing different drivers (chrome, opera, etc.)
        self.driver = webdriver.Firefox(options=OPTIONS)
        self.driver.get(WEBSITE_TO_SCRAPE)

    def __getattr__(self, name: str):
        return self.__dict__[f"_{name}"]

    def __setattr__(self, name: str, value: Any):
        self.__dict__[f"_{name}"] = value

    def extract_date(self, card: WebElement) -> str:
        link = str(card.get_attribute("href"))
        date = link.split("date=")[1]
        return date

    def scrape_last_drawing_date(self) -> str:
        return self.extract_date(self.cards_ls[-1])

    def scrape_drawings(self) -> None:
        for card in self.cards_ls:
            date = self.extract_date(card)
            drawing = Drawing(date)
            drawing.add_winning_ls(
                [
                    int(item.text)
                    for item in card.find_elements(By.CLASS_NAME, "white-balls")
                ]
            )

            drawing.add_winning_number(
                int(card.find_element(By.CLASS_NAME, "powerball").text), True
            )
            self.drawings_ls.append(drawing)

    def load_drawings(self, num: int = 1) -> None:
        for i in range(num):
            print(f"Scroll #{i+1} Done")
            elem = self.driver.find_element(By.ID, "loadMore")
            elem.send_keys(Keys.RETURN)

        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        self.cards_ls = self.driver.find_elements(By.CLASS_NAME, "card")

    def print_drawings(self) -> None:
        for drawing in self.drawings_ls:
            drawing.print()
            print()

    def __del__(self) -> None:
        print("Closing driver")
        self.driver.quit()
        print("Driver Closed!")


if __name__ == "__main__":
    spb = ScrapePowerBall()
    spb.load_drawings(num=3)
    # print(spb.scrape_last_drawing_date())
    spb.scrape_drawings()
    spb.print_drawings()
    del spb
