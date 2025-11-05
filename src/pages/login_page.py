# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
#
#
# class LoginPage:
#     USERNAME = (By.ID, "inputUsername")
#     PASSWORD = (By.XPATH, "//input[@placeholder='Password']")
#     SIGN_IN  = (By.XPATH, "//button[normalize-space()='Sign In']")
#
#     # elements shown after successful login
#     SUCCESS_MSG = (By.CSS_SELECTOR, "p")        # contains "You are successfully logged in."
#     LOGOUT_BTN  = (By.XPATH, "//button[normalize-space()='Log Out']")
#
#     def __init__(self, driver, wait):
#         self.driver = driver
#         self.wait = wait
#
#     def open(self, base_url):
#         self.driver.get(base_url)
#         self.wait.until(EC.visibility_of_element_located(self.USERNAME))
#         return self
#
#     def login(self, username, password):
#         self.driver.find_element(*self.USERNAME).clear()
#         self.driver.find_element(*self.USERNAME).send_keys(username)
#         self.driver.find_element(*self.PASSWORD).clear()
#         self.driver.find_element(*self.PASSWORD).send_keys(password)
#         self.driver.find_element(*self.SIGN_IN).click()
#         return self
#
#     def wait_for_success(self):
#         # either success message or logout button proves login
#         self.wait.until(
#             EC.any_of(
#                 EC.text_to_be_present_in_element(self.SUCCESS_MSG, "successfully logged in"),
#                 EC.visibility_of_element_located(self.LOGOUT_BTN)
#             )
#         )
#         return self

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.utilities.logger import get_logger


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
        self.log.info(f"Opening URL: {base_url}")
        self.driver.get(base_url)
        self.log.debug("Page load started, waiting for username field to be visible...")
        self.wait.until(EC.visibility_of_element_located(self.USERNAME))
        self.log.info("Login page loaded successfully.")
        return self

    def login(self, username, password):
        self.log.info(f"Attempting to log in with username: {username}")

        self.log.debug("Clearing username field...")
        self.driver.find_element(*self.USERNAME).clear()
        self.driver.find_element(*self.USERNAME).send_keys(username)
        self.log.debug("Username entered successfully.")

        self.log.debug("Clearing password field...")
        self.driver.find_element(*self.PASSWORD).clear()
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.log.debug("Password entered successfully.")

        self.log.debug("Clicking Sign In button...")
        self.driver.find_element(*self.SIGN_IN).click()
        self.log.info("Sign In button clicked.")
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
            raise
        return self
