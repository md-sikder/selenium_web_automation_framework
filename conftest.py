import os, pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from config.config_reader import read_config

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default=None, help="Environment name")

@pytest.fixture(scope="session")
def settings(request):
    return read_config(request.config.getoption("--env"))

@pytest.fixture(scope="session")
def driver(settings):
    opts = ChromeOptions()
    if os.getenv("HEADLESS", "true").lower() == "true":
        opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--disable-gpu"); opts.add_argument("--no-sandbox")
    drv = webdriver.Chrome(options=opts)   # Selenium Manager resolves driver
    drv.implicitly_wait(settings["implicit_wait"])
    yield drv
    drv.quit()

@pytest.fixture
def wait(driver, settings):
    return WebDriverWait(driver, settings["explicit_wait"])
