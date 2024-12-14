from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class TestProfile:

    def setup_method(self):
        options = Options()
        options.add_argument("--headless")  # Modo sin interfaz gráfica
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service("/usr/bin/chromedriver")  # Ajusta la ruta si es necesario
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 10)  # Tiempo de espera explícita

    def teardown_method(self):
        self.driver.quit()

    def test_edit_profile_valid_data(self):
        """Caso positivo: Editar perfil con datos válidos."""
        self.driver.get("http://web_app_container:5000/")
        self.driver.set_window_size(927, 1012)

        # Inicia sesión
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.ID, "email").send_keys("user3@example.com")
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "submit").click()
        assert self.driver.current_url == "http://web_app_container:5000/", "Login failed or incorrect page loaded."

        # Despliega el menú lateral y selecciona "Edit profile"
        menu_toggle = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".js-sidebar-toggle")))
        menu_toggle.click()
        edit_profile_button = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Edit profile")))
        edit_profile_button.click()
        assert "edit" in self.driver.current_url, "Failed to navigate to the Edit Profile page."

        # Cierra sesión
        self.driver.find_element(By.CSS_SELECTOR, ".text-dark").click()
        self.driver.find_element(By.LINK_TEXT, "Log out").click()
        assert "login" in self.driver.current_url or "signup" in self.driver.page_source.lower(), "Logout failed."

    def test_view_my_profile(self):
        """Caso positivo: Navegar a "My Profile"."""
        self.driver.get("http://web_app_container:5000/")
        self.driver.set_window_size(927, 1012)

        # Inicia sesión
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.ID, "email").send_keys("user3@example.com")
        self.driver.find_element(By.ID, "password").send_keys("1234")
        self.driver.find_element(By.ID, "submit").click()
        assert self.driver.current_url == "http://web_app_container:5000/", "Login failed or incorrect page loaded."

        # Accede a "My Profile"
        self.driver.find_element(By.CSS_SELECTOR, ".text-dark").click()
        self.driver.find_element(By.LINK_TEXT, "My profile").click()
        assert "profile" in self.driver.current_url, "Failed to navigate to My Profile page."

        # Cierra sesión
        self.driver.find_element(By.CSS_SELECTOR, ".text-dark").click()
        self.driver.find_element(By.LINK_TEXT, "Log out").click()
        assert "login" in self.driver.current_url or "signup" in self.driver.page_source.lower(), "Logout failed."

