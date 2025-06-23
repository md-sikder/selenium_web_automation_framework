# Include better exception handling and dynamic driver loading..

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
import os
from config.config_reader import read_config


class BaseDriver:
    def __init__(self, env='test'):
        config = read_config(env)
        self.driver = None
        browser = config['browser']
        try:
            if browser == 'chrome':
                self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            elif browser == 'firefox':
                self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
            else:
                raise ValueError("Unsupported browser!")
            self.driver.implicitly_wait(config['implicit_wait'])
            self.driver.get(config['url'])
        except Exception as e:
            print(f"Error initializing the driver: {e}")
