# example
import time

import pytest
from src.pages.login_page import LoginPage
from src.utilities.logger import LogGen
from src.utilities.capture_screenshot import capture_screenshot

logger = LogGen.loggen()


class TestExample:
    @pytest.fixture(scope="class")
    def setup(self, request, env):
        self.page = LoginPage(env=env)
        request.cls.page = self.page
        yield
        self.page.close_browser()

    @pytest.mark.smoke
    @pytest.mark.usefixtures("setup")
    def test_example(self):
        logger.info("Starting test_example")
        try:
            self.page.maximize_browser()
            self.page.set_username()
            self.page.set_password()
            self.page.click_signin_button()
            time.sleep(5)
            self.page.close_browser()
            text = self.page.get_page_title()
            assert text == "Expected Text"
            logger.info("login test passed")
        except AssertionError as e:
            capture_screenshot(self.page.driver, "test_example")
            logger.error(f"test_example failed: {e}")
            raise
