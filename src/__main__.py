"""Main entry point"""


import os

from dotenv import load_dotenv

from src.bot.bot import Client
from src.tools.logger import setup_logger
from src.tools.parser import arg_parser

# pylint: disable=broad-exception-caught
if __name__ == "__main__":
    parser = arg_parser()
    load_dotenv()
    setup_logger()
    try:
        discord_bot = Client(parser.channel, parser.interface)
        discord_bot.run(os.getenv("DISCORD_TOKEN"))
    except Exception as error:
        print(f"Bot stopped. Error: {error}")
