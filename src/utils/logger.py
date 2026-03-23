import logging
import os
from datetime import datetime
from utils.config import get_config


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
    config = get_config()

    log_dir = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        config["log_directory"]
    )
    try:
        os.makedirs(log_dir, exist_ok=True)
    except OSError as e:
        raise OSError(f"Failed to create log directory '{log_dir}': {e}")

    log_file = os.path.join(
        log_dir,
        f"scan_{datetime.now().strftime('%Y%m%d')}.log"
    )

    logger = logging.getLogger(name)
    log_level = getattr(logging, config["log_level"].upper(), logging.DEBUG)
    logger.setLevel(log_level)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(log_level)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger