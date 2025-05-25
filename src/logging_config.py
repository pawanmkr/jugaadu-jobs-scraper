import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = "logs"
LOG_FILE = "naukri_scraper.log"

Path(LOG_DIR).mkdir(parents=True)


def silence_noisy_logs() -> None:
    noisy_loggers = [
        "aiosqlite",
        "sqlalchemy.engine.Engine",
        "sqlalchemy.engine",
        "sqlalchemy.pool",
        "httpx",
        "httpcore.connection",
        "httpcore.http11",
        "urllib3",
    ]
    for logger_name in noisy_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.CRITICAL)  # Only CRITICAL messages will pass
        logger.handlers.clear()
        logger.propagate = (
            False  # Stop messages from propagating to root logger handlers
        )


def setup_logging() -> None:
    log_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
    )

    file_handler = RotatingFileHandler(
        Path(LOG_DIR) / LOG_FILE,
        maxBytes=1_000_000,  # 1 MB per file
        backupCount=10,
    )
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.DEBUG)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Silence specific noisy libraries
    silence_noisy_logs()
