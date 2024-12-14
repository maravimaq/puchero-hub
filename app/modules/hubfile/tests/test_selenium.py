from selenium.common.exceptions import NoSuchElementException
import time
import os
from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver, close_driver


def test_hubfile_index():

    driver = initialize_driver()

    try:
        host = "http://web_app_container:5000"


        # Open the index page
        driver.get(f'{host}/hubfile')

        # Wait a little while to make sure the page has loaded completely
        time.sleep(4)

        try:

            pass

        except NoSuchElementException:
            raise AssertionError('Test failed!')

    finally:

        # Close the browser
        close_driver(driver)

def test_hubfile_file_download():
    driver = initialize_driver()

    try:
        host = "http://web_app_container:5000"

        # Replace `1` with a valid `file_id` that exists in your database
        file_id = 1
        driver.get(f"{host}/file/download/{file_id}")
        time.sleep(2)  # Wait for the page to load

        try:
            # Check if the page contains some expected text (adjust based on response behavior)
            page_content = driver.page_source
            assert "File not found" not in page_content, "File not found error displayed!"
            print("File download page test passed!")
        except AssertionError as e:
            print(str(e))
            raise

    finally:
        close_driver(driver)

def test_hubfile_file_view():
    driver = initialize_driver()

    try:
        host = "http://web_app_container:5000"

        # Replace `1` with a valid `file_id` that exists in your database
        file_id = 1
        driver.get(f"{host}/file/view/{file_id}")
        time.sleep(2)  # Wait for the page to load

        try:
            # Check if the page contains file content
            page_content = driver.page_source
            assert "File not found" not in page_content, "File not found error displayed!"
            assert "success" in page_content.lower(), "Expected 'success' not found in the response!"
            print("File view page test passed!")
        except AssertionError as e:
            print(str(e))
            raise

    finally:
        close_driver(driver)

def test_hubfile_invalid_file_download():
    driver = initialize_driver()

    try:
        host = "http://web_app_container:5000"

        # Use an ID that does not exist in your database
        invalid_file_id = 9999
        driver.get(f"{host}/file/download/{invalid_file_id}")
        time.sleep(2)  # Wait for the page to load

        try:
            # Check for an error message or response indicating the file was not found
            page_content = driver.page_source
            assert "File not found" in page_content or "404" in page_content, \
                "Expected 'File not found' message or a 404 response not displayed!"
            print("Invalid file download test passed!")

        except AssertionError as e:
            print(str(e))
            raise

    finally:
        close_driver(driver)

def test_hubfile_view_cookie_set():
    driver = initialize_driver()

    try:
        host = "http://web_app_container:5000"

        # Use a valid file ID that exists in your database
        valid_file_id = 1
        driver.get(f"{host}/file/view/{valid_file_id}")
        time.sleep(2)  # Wait for the page to load

        try:
            # Verify that the 'view_cookie' is set
            cookies = driver.get_cookies()
            cookie_names = [cookie['name'] for cookie in cookies]
            assert "view_cookie" in cookie_names, "Expected 'view_cookie' not found in browser cookies!"
            print("View cookie test passed! 'view_cookie' was successfully set.")

        except AssertionError as e:
            print(str(e))
            raise

    finally:
        close_driver(driver)

def test_hubfile_file_view_and_download_workflow():
    driver = initialize_driver()

    try:
        host = "http://web_app_container:5000"

        # Use a valid file ID
        valid_file_id = 1  # Replace with a valid file ID in your database

        # Step 1: View the file
        driver.get(f"{host}/file/view/{valid_file_id}")
        time.sleep(2)  # Wait for the page to load

        # Verify that the 'view_cookie' is set
        cookies = driver.get_cookies()
        print("Cookies after file view:", cookies)
        cookie_names = [cookie['name'] for cookie in cookies]
        assert "view_cookie" in cookie_names, "Expected 'view_cookie' not found after file view!"

        # Step 2: Download the file
        driver.get(f"{host}/file/download/{valid_file_id}")
        time.sleep(3)  # Wait for the download to initiate

        # Verify that the 'file_download_cookie' is set
        cookies = driver.get_cookies()
        print("Cookies after file download:", cookies)
        cookie_names = [cookie['name'] for cookie in cookies]
        assert "file_download_cookie" in cookie_names, "Expected 'file_download_cookie' not found after file download!"

        # Additional Validation: Ensure both cookies are set
        assert "view_cookie" in cookie_names, "View cookie was lost after file download!"
        print("Workflow test passed: File view and download workflow is correct.")

    except AssertionError as e:
        print(f"Test failed: {e}")
        raise

    finally:
        close_driver(driver)

# Call the test function
test_hubfile_index()
test_hubfile_file_download()
test_hubfile_file_view()
test_hubfile_invalid_file_download()
test_hubfile_view_cookie_set()
test_hubfile_file_view_and_download_workflow()
