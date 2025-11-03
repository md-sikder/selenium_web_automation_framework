from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SIGN_IN  = (By.ID, "sign-in")

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open(self, base_url):
        self.driver.get(base_url)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME))
        return self

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME).send_keys(username)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.SIGN_IN).click()
