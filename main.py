from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from typing import Optional
import time
import pandas as pd
import random

RANDOM_SLEEP_MAX_TIME = 5

TWO_MINUTES = 120


def random_sleep(max_time: float):
    time.sleep(random.uniform(0, max_time))


DRIVER_PATH = "/Users/miguellobo/chromedriver"

CONTACTS_XPATH = "//*[@id='ds-data-view']/ul/li[15]/div/section/form/div[1]/section[2]/div/div/label/div/div[2]"

PLACE_WINDOW_ID = "ds-container"

def place_get_contact(driver) -> Optional[str]:
    try:
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, CONTACTS_XPATH))
        )
        contacts = driver.find_elements_by_xpath(CONTACTS_XPATH)
        for contact in contacts:
            title = contact.find_element_by_xpath(".//h6").text
            if title == "Property Owner":
                try:
                    number = contact.find_element_by_xpath(".//p").text
                    return number
                except NoSuchElementException:
                    print("This home owner did not have a contact.")
                    break
    except TimeoutException:
        print("For some reason it was not possible to find the contacts list.")


def main():
    driver = webdriver.Chrome(DRIVER_PATH)
    driver.implicitly_wait(10)

    driver.get(
        f"https://www.zillow.com/oh/fsbo_att/?searchQueryState=%7B%22mapBounds%22%3A%7B%22west%22%3A-86.2343149765625%2C%22east%22%3A-79.1041880234375%2C%22south%22%3A39.11643555094673%2C%22north%22%3A41.647479166325795%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22att%22%3A%7B%22value%22%3A%22fsbo%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A8%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A44%2C%22regionType%22%3A2%7D%5D%2C%22usersSearchTerm%22%3A%22Ohio%22%2C%22schoolId%22%3Anull%7D"
    )

    data = pd.DataFrame(columns=["link", "property owner contact"])

    try:
        results_grid = WebDriverWait(driver, TWO_MINUTES).until(
            ec.presence_of_element_located((By.ID, "grid-search-results"))
        )
        places = results_grid.find_elements_by_class_name("list-card")
        random.shuffle(places)
        contacts_found = 0
        for place in places:
            random_sleep(RANDOM_SLEEP_MAX_TIME)
            place.click()
            print(f"Current url: {driver.current_url}")
            contact = place_get_contact(driver)
            if contact is not None:
                data.loc[contacts_found] = (driver.current_url, contact)
                data.to_csv("contacts.csv", sep="\t", index=False)
                contacts_found += 1
                print(f"\ncurrent data: {data}")
            random_sleep(RANDOM_SLEEP_MAX_TIME)
            driver.back()
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
