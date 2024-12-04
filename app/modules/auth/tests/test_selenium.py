from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver, close_driver


def test_login_and_check_element():

    driver = initialize_driver()

    try:
        host = "http://web_app_container:5000"

        # Open the login page
        driver.get(f'{host}/login')

        # Wait a little while to make sure the page has loaded completely
        time.sleep(4)

        # Find the username and password field and enter the values
        email_field = driver.find_element(By.NAME, 'email')
        password_field = driver.find_element(By.NAME, 'password')

        email_field.send_keys('user1@example.com')
        password_field.send_keys('1234')

        # Send the form
        password_field.send_keys(Keys.RETURN)

        # Wait a little while to ensure that the action has been completed
        time.sleep(4)

        try:
            driver.find_element(By.XPATH, "//h1[contains(@class, 'h2 mb-3') and contains(., 'Latest datasets')]")
            print('Test passed!')

        except NoSuchElementException:
            raise AssertionError('Test failed!')

    finally:
        # Close the browser
        close_driver(driver)


def test_register_user():
    driver = initialize_driver()

    try:
        host = "http://web_app_container:5000"

        # Open the signup page
        driver.get(f'{host}/signup/')
        print("Navigated to:", driver.current_url)

        # Debugging: Ensure the page is correct
        if "signup" not in driver.current_url:
            raise AssertionError("Failed to load the signup page!")

        # Wait for the email field to be present
        try:
            email_field = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.NAME, "email"))
            )
        except TimeoutException:
            print("Email field not found!")
            print("Current URL:", driver.current_url)
            with open("page_source.html", "w") as f:
                f.write(driver.page_source)  # Save the page source for debugging
            raise

        # Use a unique email for registration
        email = f"testuser_{int(time.time())}@example.com"
        email_field.send_keys(email)

        # Fill out the rest of the form
        driver.find_element(By.NAME, 'password').send_keys('password123')
        driver.find_element(By.NAME, 'name').send_keys('Test')
        driver.find_element(By.NAME, 'surname').send_keys('User')

        # Submit the form
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'btn-primary'))  # Matches the class for the submit button
        )
        submit_button.click()

        # Wait for the signup success
        try:
            WebDriverWait(driver, 10).until(
                lambda driver: "Welcome" in driver.page_source or driver.current_url == f"{host}/"
            )
            print('Signup test passed!')
        except TimeoutException:
            print('Signup test failed! Success message or redirection not found.')
            print("Page Source:\n", driver.page_source)
            raise

    finally:
        close_driver(driver)


# Call the test function
test_login_and_check_element()
test_register_user()
