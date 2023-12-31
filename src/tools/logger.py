"""Module for logger"""

import logging


def setup_logger() -> logging.Logger:
    """
    Create a very basic logger

    Returns:
        logging.Logger: logger
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler("discord_parser.log")
    file_handler.setLevel(logging.DEBUG)

    terminal_handler = logging.StreamHandler()
    terminal_handler.setLevel(logging.INFO)

    terminal_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(terminal_handler)

    return logger
