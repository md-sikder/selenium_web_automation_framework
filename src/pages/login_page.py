from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    USERNAME = (By.ID, "inputUsername")
    PASSWORD = (By.XPATH, "//input[@placeholder='Password']")
    SIGN_IN  = (By.XPATH, "//button[normalize-space()='Sign In']")

    # elements shown after successful login
    SUCCESS_MSG = (By.CSS_SELECTOR, "p")        # contains "You are successfully logged in."
    LOGOUT_BTN  = (By.XPATH, "//button[normalize-space()='Log Out']")

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open(self, base_url):
        self.driver.get(base_url)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME))
        return self

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME).clear()
        self.driver.find_element(*self.USERNAME).send_keys(username)
        self.driver.find_element(*self.PASSWORD).clear()
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.SIGN_IN).click()
        return self

    def wait_for_success(self):
        # either success message or logout button proves login
        self.wait.until(
            EC.any_of(
                EC.text_to_be_present_in_element(self.SUCCESS_MSG, "successfully logged in"),
                EC.visibility_of_element_located(self.LOGOUT_BTN)
            )
        )
        return self
