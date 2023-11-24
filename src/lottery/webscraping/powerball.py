try:
    import sys

    sys.path.append("..")
    from utils.drawing import Drawing
except ModuleNotFoundError:
    from src.lottery.utils.drawing import Drawing
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # noqa: F401
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from typing import Any, List
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import csv
import os

OPTIONS = FirefoxOptions()
OPTIONS.add_argument("--headless")
WEBSITE_TO_SCRAPE = "https://www.powerball.com/previous-results?gc=powerball"


class ScrapePowerBall:
    def __init__(self, end_date: str = "", with_jackpot: bool = True):
        # TODO: Use end_date to limit number of new drawings
        self.end_date = end_date

        # Scraping estimated jackpot requires opening a new link (new tab)
        # So it takes more time to scrape. Set to False to skip that part.
        self.jackpot = with_jackpot

        # pre-processing (raw results from web scraping)
        self.cards_ls = []

        # post-processing results
        self.drawings_ls = []
        self.len_drawings = 0

    # Credits to Leodanis Pozo Ramos (realpython) for the __getattr__ and __setattr__
    # https://realpython.com/python-getter-setter/#the-__setattr__-and-__getattr__-methods
    def __getattr__(self, name: str):
        return self.__dict__[f"_{name}"]

    def __setattr__(self, name: str, value: Any):
        self.__dict__[f"_{name}"] = value

    def __enter__(self) -> WebElement:
        # TODO: Replace DRIVER constant with protected variable
        #       to allow choosing different drivers (chrome, opera, etc.)
        # print("Connected!")
        self.driver = webdriver.Firefox(options=OPTIONS)
        self.driver.set_page_load_timeout(2)
        self.get_website(WEBSITE_TO_SCRAPE)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        # print("Closing driver")
        self.driver.quit()
        # print("Driver Closed!")

    def extract_date(self, card: WebElement) -> str:
        """
        Reads and returns the date of a specific drawing

        Parameters
        ----------
            Card - WebElement (Selenium)
                Element read from powerball website

        Returns
        --------
            Date - String
        """
        link = str(card.get_attribute("href"))
        date = link.split("date=")[1]
        return date

    def scrape_last_drawing_date(self) -> str:
        """
        Return the date of the last drwaing that was scraped.

        Returns
        --------
            Date - String
        """
        return self.extract_date(self.cards_ls[-1])

    def get_website(self, link) -> None:
        # Some links takes long time to load. If so, stop and extract data.
        try:
            self.driver.get(link)
        except TimeoutException:
            self.driver.execute_script("window.stop();")

    def scrape_jackpot(self, card) -> int:
        # Extract link of the specific drawing
        link = str(card.get_attribute("href"))

        # Open link in a new tab
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])

        self.get_website(link)

        # Find div where estimated jackpot is located in.
        try:
            jackpot_div = self.driver.find_elements(By.CLASS_NAME, "estimated-jackpot")[
                0
            ].get_attribute("innerHTML")
            est_jackpot = jackpot_div.split("<span>")[-1].split("</span>")[0]
            est_jackpot = est_jackpot.replace("$", "")
        except IndexError:
            return -1

        # Close new tab
        self.driver.close()

        # Switch to main tab - list of drawings
        self.driver.switch_to.window(self.driver.window_handles[0])

        jackpot_int = float(est_jackpot.split(" ")[0])
        if "Million" in est_jackpot:
            return int(jackpot_int * 10**6)

        if "Billion" in est_jackpot:
            return int(jackpot_int * 10**9)

    def scrape_drawings(self) -> None:
        """
        Scrape lottery cards (drawings) from powerball website.
        """
        self.drawings_ls = []
        self.len_drawings = 0
        for card in self.cards_ls:
            date = self.extract_date(card)
            drawing = Drawing(date, self.scrape_jackpot(card))
            drawing.add_winning_ls(
                [int(item.text) for item in card.find_elements(By.CLASS_NAME, "white-balls")]
            )

            drawing.add_winning_number(
                int(card.find_element(By.CLASS_NAME, "powerball").text), True
            )
            self.drawings_ls.append(drawing)
            self.len_drawings += 1

            # print(f"{drawing.date}, {drawing.get_formatted_jackpot()}")

    def load_drawings(self, num: int = 1) -> None:
        """
        Pressing the "Load More" button to get more drawings.
        Each press loads about 30 lottery drawings.

        Parameters
        ----------
            num - int
                Represent the times to press the button.

        Returns
        --------
            Date - String
        """
        self.cards_ls = []

        for i in range(num):
            WebDriverWait(self.driver, timeout=5).until(lambda x: x.find_element(By.ID, "loadMore"))
            print(f"Scroll #{i+1} Done")
            elem = self.driver.find_element(By.ID, "loadMore")
            elem.send_keys(Keys.RETURN)

        WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "card"))
        )
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        self.cards_ls = self.driver.find_elements(By.CLASS_NAME, "card")

    def print_drawings(self) -> None:
        """
        Print lottery drawings one after the other using Drawing.print method
        """
        for drawing in self.drawings_ls:
            drawing.print()
            print()

    def sort_drawings_by_date(self, descending: bool = True) -> List[Drawing]:
        """
        Sort drawing by date in descending order if decending is True.

        Parameters
        ----------
            descending - boolean
                If True, drawings are sorted in descending order

        Returns
        --------
            Ordered Drawings - List of Drawing
        """
        return sorted(self.drawings_ls, key=lambda x: x.date, reverse=descending)

    def to_csv(self, path: str, file_name: str) -> None:
        """
        Export results to csv file.

        Parameters
        ----------
            path - str
                Folder in which the csv file is stored.

            file_name - str
                Name of the csv file. If doesn't contain .csv,
                extension will be added.

        Errors
        --------
            ValueError - Folder doesn't exist (path is invalid)
        """
        if not os.path.exists(path):
            raise ValueError("Invalid path")

        if ".csv" not in file_name:
            file_name += ".csv"

        headers = ["date", "ball_1", "ball_2", "ball_3", "ball_4", "ball_5", "powerball"]
        if self.jackpot:
            headers.append("estimated_jackpot")

        with open(f"{path}/{file_name}", "w") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for drawing in self.sort_drawings_by_date():
                writer.writerow(drawing.get_winning_ls())
