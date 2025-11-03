import os
import re
import time
import pytest
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait

from config.config_reader import read_config


# ---------- Paths ----------
ROOT = Path(__file__).parent
LOGS_DIR = ROOT / "logs"
REPORTS_DIR = ROOT / "reports"
SCREENSHOTS_DIR = ROOT / "screenshots"


# ---------- Pytest bootstrapping ----------
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default=None, help="Environment name")


def pytest_sessionstart(session):
    # Ensure folders exist on a fresh clone
    for d in (LOGS_DIR, REPORTS_DIR, SCREENSHOTS_DIR):
        d.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def settings(request):
    """Returns the selected environment config (falls back to YAML default)."""
    return read_config(request.config.getoption("--env"))


@pytest.fixture(scope="session")
def driver(settings):
    """Session-scoped WebDriver (Selenium Manager resolves ChromeDriver)."""
    opts = ChromeOptions()
    if os.getenv("HEADLESS", "true").lower() == "true":
        opts.add_argument("--headless=new")
        opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")

    drv = webdriver.Chrome(options=opts)
    drv.implicitly_wait(settings["implicit_wait"])
    yield drv
    drv.quit()


@pytest.fixture
def wait(driver, settings):
    """Per-test explicit wait helper."""
    return WebDriverWait(driver, settings["explicit_wait"])


# ---------- Failure screenshot hook ----------
def _sanitize_file_component(text: str) -> str:
    """Make a safe filename part from a nodeid/test name."""
    # Replace path separators and pytest's :: with underscores, remove bad chars
    text = text.replace(os.sep, "_").replace("::", "_")
    return re.sub(r'[^A-Za-z0-9._-]+', "_", text)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    After each test phase, if the call phase failed:
      - capture a PNG screenshot into ./screenshots
      - attach it to pytest-html (if plugin is loaded)
    """
    outcome = yield
    rep = outcome.get_result()

    # Only on the 'call' phase (i.e., the test body), and only on failure
    if rep.when != "call" or rep.passed:
        return

    driver = item.funcargs.get("driver", None)
    if not driver:
        return  # No driver fixture available for this test

    # Build a unique, sanitized file name
    ts = int(time.time())
    base = _sanitize_file_component(item.nodeid) or "test"
    png_path = SCREENSHOTS_DIR / f"{base}_{ts}.png"

    # Attempt screenshot
    try:
        driver.save_screenshot(str(png_path))
    except Exception:
        # Don't break reporting if screenshot fails
        return

    # If pytest-html is installed, attach the image to the report
    plugin = item.config.pluginmanager.getplugin("html")
    if plugin:
        try:
            from pytest_html import extras
        except Exception:
            return

        # Ensure rep.extra exists
        extra = getattr(rep, "extra", [])
        # Add embedded image and a link to open the file
        extra.append(extras.image(str(png_path)))
        extra.append(extras.url(str(png_path), name="Open screenshot"))
        rep.extra = extra
