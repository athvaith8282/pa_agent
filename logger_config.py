# logger_config.py
from loguru import logger
import sys

from config import LOGS_PATH

# Remove default logger
logger.remove()

# Add console logging
logger.add(sys.stdout, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}")

# Add file logging
logger.add(
    LOGS_PATH,
    rotation="100 MB",       # Rotate logs after 10MB
    retention="15 days",     # Keep for 7 days
    compression="zip",      # Compress old logs
    backtrace=True,
    diagnose=True,
)

# You can wrap this to control re-configuration
def get_logger():
    return logger
