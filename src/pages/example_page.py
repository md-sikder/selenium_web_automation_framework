# Structure the POM with clear separation of page elements and actions..
from selenium.webdriver.common.by import By
from src.base.base_driver import BaseDriver


class ExamplePage(BaseDriver):
    def __init__(self, env='default'):
        super().__init__(env)
        self.example_element = (By.ID, "exampleId")

    def get_example_text(self):
        return self.driver.find_element(*self.example_element).text

    def close_browser(self):
        self.driver.quit()
