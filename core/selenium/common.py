from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager


from selenium.webdriver.chrome.options import Options

def initialize_driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")  # Run in headless mode for Docker
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")  # Enable DevTools debugging

    driver = webdriver.Remote(
        command_executor="http://selenium_container:4444/wd/hub",
        options=options
    )
    return driver


def close_driver(driver):
    driver.quit()
