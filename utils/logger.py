"""
Logger utility module for the Behave Playwright Framework.

This module provides a centralized logging configuration that outputs logs to both
console and file. It ensures consistent logging behavior across the framework.

Functions:
    get_logger(name): Returns a configured logger instance with console and file handlers.

The logger is configured to output logs in the format:
    %(asctime)s - %(name)s - %(levelname)s - %(message)s

Log files are stored in the reports/logs directory.
"""
import logging
import os
from datetime import datetime

def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        ch = logging.StreamHandler()
        ch.setFormatter(log_format)
        logger.addHandler(ch)
        

        if not os.path.exists("reports/logs"):
            os.makedirs("reports/logs")
        fh = logging.FileHandler(f"reports/logs/test_run.log")
        fh.setFormatter(log_format)
        logger.addHandler(fh)
    return logger