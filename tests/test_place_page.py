from selenium import webdriver
from main import DRIVER_PATH, place_get_contact


def test_open_contact_page():
    url = "https://www.zillow.com/homedetails/325-Gilbert-St-Kenton-OH-43326/97144177_zpid/"
    driver = webdriver.Chrome(DRIVER_PATH)
    try:
        driver.get(url)
        contact = place_get_contact(driver)
        assert contact is not None

    finally:
        driver.quit()
