from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


import time

from core.selenium.common import initialize_driver, close_driver


def setup_method(self, method):
    self.driver = initialize_driver()
    self.vars = {}


def test_search_datasets_by_multiple_criteria():
    driver = initialize_driver()

    try:
        host = "http://web_app_container:5000"

        # Open the explore page
        driver.get(f'{host}/explore')

        # Wait for the page to load
        time.sleep(2)

        # Find the author search field and enter the value
        author_field = driver.find_element(By.ID, 'author')
        author_field.send_keys('Author One')

        # Find the publication type field and select the value
        publication_type_field = driver.find_element(By.ID, 'publication_type')
        publication_type_field.send_keys('Journal Article')
        publication_type_field.send_keys(Keys.RETURN)

        # Wait for the results to load
        time.sleep(2)

        # Verify that the results contain the expected dataset
        results = driver.find_elements(By.CSS_SELECTOR, '.card')
        assert len(results) > 0, "No datasets found."
        assert any("Dataset 1" in result.text for result in results), "Dataset 1 not found in the results."

    finally:
        close_driver(driver)


# Call the test function
test_search_datasets_by_multiple_criteria()