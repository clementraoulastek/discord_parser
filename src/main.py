import logging
import os

from dotenv import load_dotenv

from tools.bot import Client
from tools.logger import logger

if __name__ == "__main__":
    load_dotenv()
    logger()
    try:
        discord_bot = Client()
        discord_bot.run(os.getenv("DISCORD_TOKEN"))
    except Exception:
        print("Bot stopped.")