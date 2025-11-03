import pytest
from selenium.webdriver.support import expected_conditions as EC
from src.pages.login_page import LoginPage

@pytest.mark.smoke
@pytest.mark.parametrize("username,password,expected_title", [
    ("admin","admin","Expected Text"),
])
def test_login_smoke(driver, wait, settings, username, password, expected_title):
    LoginPage(driver, wait).open(settings["url"]).login(username, password)
    wait.until(EC.title_is(expected_title))
    assert driver.title == expected_title
