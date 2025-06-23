import time

from selenium.webdriver.common.by import By
from src.base.base_driver import BaseDriver


class LoginPage(BaseDriver):
    def __init__(self, env='default'):
        super().__init__(env)
        self.textbox_username = (By.XPATH, "//input[@id='username']")
        self.textbox_password = (By.XPATH, "//input[@id='password']")
        self.button_signIn = (By.XPATH, "//button[@id='sign-in']")

    def maximize_browser(self):
        return self.driver.maximize_window()

    def set_username(self):
        return self.driver.find_element(*self.textbox_username).send_keys("admin")

    def set_password(self):
        return self.driver.find_element(*self.textbox_password).send_keys("admin")

    def click_signin_button(self):
        return self.driver.find_element(*self.button_signIn).click()

    def get_page_title(self):
        return self.driver.title

    def close_browser(self):
        self.driver.quit()
