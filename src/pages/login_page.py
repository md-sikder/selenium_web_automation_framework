from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.utilities.logger import get_logger
from src.utilities.capture_screenshot import capture_screenshot


class LoginPage:
    USERNAME = (By.ID, "inputUsername")
    PASSWORD = (By.XPATH, "//input[@placeholder='Password']")
    SIGN_IN  = (By.XPATH, "//button[normalize-space()='Sign In']")
    SUCCESS_MSG = (By.CSS_SELECTOR, "p")
    LOGOUT_BTN  = (By.XPATH, "//button[normalize-space()='Log Out']")

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait
        self.log = get_logger()
        self.log.info("LoginPage initialized")

    def open(self, base_url):
        try:
            self.log.info(f"Opening URL: {base_url}")
            self.driver.get(base_url)
            self.wait.until(EC.visibility_of_element_located(self.USERNAME))
            self.log.info("Login page loaded successfully.")
        except Exception as e:
            self.log.error(f"❌ Failed to open page or locate username field: {e}")
            capture_screenshot(self.driver, "open_login_page_failed")
            raise
        return self

    def login(self, username, password):
        try:
            self.log.info(f"Attempting login with username: {username}")
            user_field = self.driver.find_element(*self.USERNAME)
            pass_field = self.driver.find_element(*self.PASSWORD)

            user_field.clear()
            user_field.send_keys(username)
            self.log.debug("Entered username successfully.")

            pass_field.clear()
            pass_field.send_keys(password)
            self.log.debug("Entered password successfully.")

            self.driver.find_element(*self.SIGN_IN).click()
            self.log.info("Clicked 'Sign In' button.")
        except Exception as e:
            self.log.error(f"❌ Login action failed: {e}")
            capture_screenshot(self.driver, "login_action_failed")
            raise
        return self

    def wait_for_success(self):
        self.log.info("Waiting for successful login confirmation...")
        try:
            self.wait.until(
                EC.any_of(
                    EC.text_to_be_present_in_element(self.SUCCESS_MSG, "successfully logged in"),
                    EC.visibility_of_element_located(self.LOGOUT_BTN)
                )
            )
            self.log.info("✅ Login successful — success message or Logout button found.")
        except Exception as e:
            self.log.error(f"❌ Login verification failed: {e}")
            capture_screenshot(self.driver, "login_verification_failed")
            raise
        return self
