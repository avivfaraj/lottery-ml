import sys
sys.path.append("..")
from utils.drawing import Drawing
from selenium import webdriver
# TODO: use Keys to press "Load More" button
from selenium.webdriver.common.keys import Keys  # noqa: F401
from selenium.webdriver.common.by import By


if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get("https://www.powerball.com/previous-results?gc=powerball")

    cards = driver.find_elements(By.CLASS_NAME, "card")

    drawing_ls = []
    for card in cards:
        link = str(card.get_attribute("href"))
        date = link.split("date=")[1]
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
        drawing_ls.append(drawing)

    for draw in drawing_ls:
        draw.print()
        print()
    driver.close()
