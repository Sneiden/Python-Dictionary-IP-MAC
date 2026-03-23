import logging
import os
from datetime import datetime


def setup_logger(name: str = "ip_mac_scanner") -> logging.Logger:
    """
    Sets up and returns a logger with both file and console handlers.

    Logs are saved daily to the logs/ directory at the project root.
    Console output is limited to INFO level and above.
    File output captures all levels from DEBUG and above.

    Args:
        name (str): Logger name. Defaults to 'ip_mac_scanner'.

    Returns:
        logging.Logger: Configured logger instance.

    Raises:
        OSError: If the log directory cannot be created.
    """
    pass