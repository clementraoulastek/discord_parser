import datetime
import logging
import os
import re
from typing import Any

import discord
import nest_asyncio
import pyshark

from tools.constants import CONNECTION_MSG
from tools.enum import Canal, LogoChanel, PercoId

nest_asyncio.apply()


class Client(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(intents=intents)

    async def on_ready(self) -> None:
        """
        When the bot is ready, parse the tcp payload
        """
        date = datetime.datetime.now().strftime("%H:%M:%S")
        intro_msg = CONNECTION_MSG
        message = f"{LogoChanel.BOT_ON.value} **{date}** **__Bot__**:{intro_msg}"
        self.channel_id = os.getenv("CHANNEL_ID")
        await self.send_message(self.channel_id, message)

        try:
            await capture_tcp_payload("en0", self)
        except KeyboardInterrupt as error:
            logging.error(error)
            await self.on_error()
        except Exception as error:
            logging.error(error)

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

    async def on_error(self, *args, **kargs) -> None:
        """
        Send a message to the channel, and close the bot
        """
        try:
            date = datetime.datetime.now().strftime("%H:%M:%S")
            message = f"{LogoChanel.BOT_OFF.value} **{date}** **__Bot__**: Bot déconnecté"
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


async def capture_tcp_payload(interface_name: str, bot: Client):
    """
    Capture the tcp payload

    Args:
        interface_name (str): interface name
        bot (Client): discord bot
    """
    PORT = 443
    capture_filter = f"tcp.srcport == {PORT} and tcp.flags == 0x018 and ip"
    capture = pyshark.LiveCapture(interface=interface_name, display_filter=capture_filter)

    logging.info("Start capture")
    for packet in capture.sniff_continuously():
        tcp_packet = packet["TCP"]
        if payload := tcp_packet.get_field_value("payload"):
            payload_bytes = bytes.fromhex(payload.replace(":", ""))
            try:
                decoded_payload = payload_bytes.decode("utf-8", errors="strict")
            except UnicodeDecodeError:
                continue
            await get_message_from_payload(decoded_payload, bot)


async def get_message_from_payload(payload: str, bot: Client, filter: str = (Canal.GUILDE)) -> str:
    """
    Get the message from the payload

    Args:
        payload (str): payload

    Returns:
        str: message
    """

    if payload.startswith("g"):
        logging.debug(payload)  #! For debug purpose

    # Handle guild actions
    try:
        if payload.startswith(Canal.GENERAL.value):
            MESSAGE_PATTERN = "([^\|]+)\|(\d+)\|([^\|]+)\|([^\|]+)\|"
            match = re.match(MESSAGE_PATTERN, payload)
            if match[1] not in [canal.value for canal in Canal] or Canal(match[1]) not in filter:
                return

            type_canal = Canal(match[1])
            date = datetime.datetime.now().strftime("%H:%M:%S")
            user = match[3]
            message = match[4]
            message = update_escape_character(message)

            logo = LogoChanel[type_canal.name].value
            chanel_name = f"({type_canal.name.lower()})"
            message = f"{logo} {chanel_name} **{date}** de **__{user}__**: {message}"

            await bot.send_message(
                channel_id=os.getenv("CHANNEL_ID"),
                message=message,
            )
        # Handle perceptor actions
        elif payload.startswith(PercoId.ADD_SELF.value):
            MESSAGE_PATTERN = "(-?\d+)\|(-?\d+)\|(\w{1,}).?As"
            match = re.findall(MESSAGE_PATTERN, payload)
            if not match:
                return

            x_coord = match[0][0]
            y_coord = match[0][1]
            user_name = match[0][2]

            logo = LogoChanel.GUILDE.value
            date = datetime.datetime.now().strftime("%H:%M:%S")
            message = f"{logo} (guilde) **{date}** {LogoChanel.PERCO.value} Un percepteur à été **posé** en: **({x_coord}, {y_coord})** par **__{user_name}__**"
            await bot.send_message(
                channel_id=os.getenv("CHANNEL_ID"),
                message=message,
            )
        elif payload.startswith(PercoId.ADD_OTHER.value):
            logo, date, x_coord, y_coord, user_name = form_message(payload, has_username=True)
            message = f"{logo} (guilde) **{date}** {LogoChanel.PERCO.value} Un percepteur à été **posé** en: **({x_coord}, {y_coord})** par **__{user_name}__**"
            await bot.send_message(
                channel_id=os.getenv("CHANNEL_ID"),
                message=message,
            )
        elif payload.startswith(PercoId.REMOVE.value):
            logo, date, x_coord, y_coord, user_name = form_message(payload, has_username=True)
            message = f"{logo} (guilde) **{date}** {LogoChanel.PERCO.value} Un percepteur à été **retiré** en: **({x_coord}, {y_coord})** par **__{user_name}__**"
            await bot.send_message(
                channel_id=os.getenv("CHANNEL_ID"),
                message=message,
            )
        elif payload.startswith(PercoId.ATTACK.value):
            logo, date, x_coord, y_coord = form_message(payload)
            message = f"{logo} (guilde) **{date}** {LogoChanel.PERCO_ATTACK.value} Un percepteur est **attaqué** en: **({x_coord}, {y_coord})**"
            await bot.send_message(
                channel_id=os.getenv("CHANNEL_ID"),
                message=message,
            )
        elif payload.startswith(PercoId.SURVIVED.value):
            logo, date, x_coord, y_coord = form_message(payload)
            message = f"{logo} (guilde) **{date}** {LogoChanel.PERCO.value} Le percepteur en **({x_coord}, {y_coord})** à **survécu**"
            await bot.send_message(
                channel_id=os.getenv("CHANNEL_ID"),
                message=message,
            )
        elif payload.startswith(PercoId.LOOSE.value):
            logo, date, x_coord, y_coord = form_message(payload)
            message = f"{logo} (guilde) **{date}** {LogoChanel.PERCO.value} Le percepteur en **({x_coord}, {y_coord})** **n'a pas survécu**"
            await bot.send_message(
                channel_id=os.getenv("CHANNEL_ID"),
                message=message,
            )
    except ValueError as error:
        logging.error(error)


def form_message(payload: str, has_username: bool = False) -> list[str]:
    """
    Form the message

    Args:
        payload (str): payload
        has_username (False): has username

    Returns:
        list[str]: list of elements from the payload
    """
    splitted_payload = payload.split("|")
    if len(splitted_payload) < 3:
        raise ValueError(f"Payload is too short, can't form the message: {payload}")

    x_coord = splitted_payload[2]
    y_coord = splitted_payload[3]
    if has_username:
        user_name = splitted_payload[4]
    logo = LogoChanel.GUILDE.value
    date = datetime.datetime.now().strftime("%H:%M:%S")

    return (
        [logo, date, x_coord, y_coord, user_name]
        if has_username
        else [logo, date, x_coord, y_coord]
    )


def update_escape_character(payload: str) -> str:
    """
    Update escape character

    Args:
        payload (str): payload

    Returns:
        str: payload
    """
    return (
        payload.replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&amp;", "&")
        .replace("&apos;", "'")
        .replace("&tilde;", "~")
        .replace("&circ;", "^")
        .replace("&grave;", "`")
        .replace("&eacute;", "é")
        .replace("&Eacute;", "É")
        .replace("&egrave;", "è")
        .replace("&Egrave;", "È")
        .replace("&ecirc;", "ê")
        .replace("°0", "[Item]")
    )
