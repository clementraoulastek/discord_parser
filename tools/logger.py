import logging

def logger() -> logging.Logger:
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('discord_parser.log')
    terminal_handler = logging.StreamHandler()
    terminal_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(terminal_handler)
    
    return logger