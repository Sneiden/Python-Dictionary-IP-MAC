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
    log_dir = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "logs"
    )
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(
        log_dir,
        f"scan_{datetime.now().strftime('%Y%m%d')}.log"
    )

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
