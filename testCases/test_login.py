import pytest
from selenium.webdriver.support import expected_conditions as EC
from src.pages.login_page import LoginPage
from src.utilities.capture_screenshot import capture_screenshot
from src.utilities.logger import get_logger


@pytest.mark.smoke
@pytest.mark.parametrize("username,password,expected_title", [
    ("rahulshettyacademy", "learning", "Rahul Shetty Academy - Login page"),
])
def test_login_smoke(driver, wait, settings, username, password, expected_title):
    log = get_logger()
    test_name = "test_login_smoke"

    try:
        log.info(f"=== START TEST: {test_name} ===")
        LoginPage(driver, wait).open(settings["url"]).login(username, password)
        wait.until(EC.title_is(expected_title))
        assert driver.title == expected_title
        log.info(f"✅ TEST PASSED: {test_name}")
    except Exception as e:
        log.error(f"❌ TEST FAILED: {e}")
        capture_screenshot(driver, test_name)
        raise
    finally:
        log.info(f"=== END TEST: {test_name} ===\n")