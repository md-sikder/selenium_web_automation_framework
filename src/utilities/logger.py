# Enhance logging with more details and rotating file handler..

import logging
import os
from logging.handlers import RotatingFileHandler


class LogGen:
    @staticmethod
    def loggen():
        if not os.path.exists('logs'):
            os.makedirs('logs')
        logger = logging.getLogger()
        handler = RotatingFileHandler('logs/test.log', maxBytes=2000, backupCount=5)
        formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger
