from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class TestDatasetModule:

    def setup_method(self, method):
        # Set up the Selenium WebDriver
        options = Options()
        options.add_argument("--headless")  # Run headless if necessary
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service("/usr/bin/chromedriver")  # Point to the manually installed chromedriver
        self.driver = webdriver.Chrome(service=service, options=options)

    def teardown_method(self, method):
        # Close the browser after each test
        self.driver.quit()

    def test_empty_datasets_message(self):
        self.driver.get("http://web_app_container:5000/")
        self.driver.set_window_size(927, 1012)

        # Log in
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.ID, "email").send_keys("user4@example.com")
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "submit").click()

        # Navigate to datasets list
        self.driver.get("http://web_app_container:5000/dataset/list")
        no_datasets_message = self.driver.find_element(By.CSS_SELECTOR, ".card-title").text
        assert (
            "No datasets found" in no_datasets_message
        ), "Message for no datasets is missing."

        # Log out
        self.driver.find_element(By.CSS_SELECTOR, ".text-dark").click()
        self.driver.find_element(By.LINK_TEXT, "Log out").click()

    def test_user_datasets_list(self):
        self.driver.get("http://web_app_container:5000/")
        self.driver.set_window_size(927, 1012)

        # Log in
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.ID, "email").send_keys("user1@example.com")
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "submit").click()

        # Navigate to datasets list
        self.driver.get("http://web_app_container:5000/dataset/list")

        # Verify datasets are displayed
        dataset_list = self.driver.find_elements(By.XPATH, "//table//tbody//tr")
        assert len(dataset_list) > 0, "No datasets displayed, but the user has datasets."

        # Log out
        self.driver.find_element(By.CSS_SELECTOR, ".text-dark").click()
        self.driver.find_element(By.LINK_TEXT, "Log out").click()

