import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver, close_driver


def wait_for_page_to_load(driver, timeout=4):
    WebDriverWait(driver, timeout).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )


def count_datasets(driver, host):
    driver.get(f"{host}/dataset/list")
    wait_for_page_to_load(driver)

    try:
        amount_datasets = len(driver.find_elements(By.XPATH, "//table//tbody//tr"))
    except Exception:
        amount_datasets = 0
    return amount_datasets




def test_list_datasets():
    driver = initialize_driver()

    try:
        host = "http://web_app_container:5000"

        # Open the login page
        driver.get(f"{host}/login")
        wait_for_page_to_load(driver)

        # Log in
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")

        email_field.send_keys("user1@example.com")
        password_field.send_keys("1234")
        password_field.send_keys(Keys.RETURN)
        wait_for_page_to_load(driver)

        # Navigate to the datasets list page
        driver.get(f"{host}/dataset/list")
        wait_for_page_to_load(driver)

        # Check datasets are listed
        datasets = driver.find_elements(By.XPATH, "//table//tbody//tr")
        assert len(datasets) > 0, "No datasets found in the list!"
        print(f"{len(datasets)} datasets found in the list. Test passed!")

    finally:
        close_driver(driver)

# Call the test functions
test_list_datasets()
