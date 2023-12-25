"""Main module for the bot"""


import datetime
import logging

import discord
import nest_asyncio

from src.tools.constants import CONNECTION_MSG
from src.tools.enum import LogoChanel
from src.tools.sniffer import TcpSniffer

nest_asyncio.apply()


class Client(discord.Client):
    """
    Client discord bot

    Args:
        discord (discord.Client): discord bot
    """

    def __init__(self, channel: str, interface: str) -> None:
        self.interface = interface
        self.channel_id = channel
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tcp_sniffer = TcpSniffer(self.interface, self)

    # pylint: disable=broad-exception-caught
    # pylint: disable=too-many-function-args
    async def on_ready(self) -> None:
        """
        When the bot is ready, parse the tcp payload
        """
        date = datetime.datetime.now().strftime("%H:%M:%S")
        intro_msg = CONNECTION_MSG
        message = f"{LogoChanel.BOT_ON.value} **{date}** **__Bot__**:{intro_msg}"
        await self.send_message(self.channel_id, message)

        try:
            await self.tcp_sniffer.capture_tcp_payload(self.interface, self)
        except Exception as error:
            logging.error(error)
            await self.on_error()

    async def send_message(self, channel_id: str, message: discord.Message) -> None:
        """
        Send a message to a channel

        Args:
            channel_id (str): The channel id
            message (discord.Message): The message
        """
        channel_id = int(channel_id)
        channel = self.get_channel(channel_id)
        await channel.send(message)

    # pylint: disable=broad-exception-caught
    # pylint: disable=unused-argument
    async def on_error(self, *args, **kargs) -> None:
        """
        Send a message to the channel, and close the bot
        """
        try:
            date = datetime.datetime.now().strftime("%H:%M:%S")
            message = (
                f"{LogoChanel.BOT_OFF.value} **{date}** **__Bot__**: Bot déconnecté"
            )
            await self.send_message(self.channel_id, message)
            await self.close()
        except Exception:
            logging.error("Error: Can't close the bot, it's already closed")

    async def on_message(self, message: discord.Message) -> None:
        """
        When a message is received, log it

        Args:
            message (discord.Message): The message
        """
        if message.author == self.user:
            logging.info(message.content)
