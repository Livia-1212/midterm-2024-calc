import logging
import os
from dotenv import load_dotenv

def configure_logging():
    """Configure logging settings based on environment variables."""
    load_dotenv()  # Load environment variables

    # Get log level and log file path from environment variables
    log_level = os.getenv('LOG_LEVEL', 'DEBUG').upper()  # Default to DEBUG if not set
    log_file = os.getenv('LOG_FILE', './app.log')  # Default to 'app.log' if not set

    # Set up log format
    log_format = '%(asctime)s - %(levelname)s - %(message)s'

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level, logging.DEBUG))

    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, log_level, logging.DEBUG))
    file_handler.setFormatter(logging.Formatter(log_format))

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level, logging.DEBUG))
    console_handler.setFormatter(logging.Formatter(log_format))

    # Clear existing handlers and add new ones
    logger.handlers = []
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Log the initial configuration
    logger.debug(f"Logging configured. Level: {log_level}, File: {log_file}")
