import os
import time

def capture_screenshot(driver, test_name):
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_name = f"screenshots/{test_name}_{timestamp}.png"
    driver.save_screenshot(screenshot_name)
    return screenshot_name
