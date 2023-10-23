import datetime
from enum import unique, Enum
import logging
import os
import re
from typing import Any
import discord
import pyshark

import nest_asyncio

from tools.constants import CONNECTION_MSG

nest_asyncio.apply()


class Client(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())

    async def on_ready(self) -> None:
        """
        When the bot is ready
        """
        date = datetime.datetime.now().strftime("%H:%M:%S")
        intro_msg = CONNECTION_MSG
        message = (
            f"{LogoChanel.BOT_ON.value} **{date}** **__Bot__**:{intro_msg}"
        )
        channel_id = os.getenv("CHANNEL_ID")

        channel_id = int(channel_id)
        channel = self.get_channel(channel_id)
        await channel.send(message)

        try:
            await capture_tcp_payload("en0", self)
        except KeyboardInterrupt as error:
            await self.on_error()
            raise KeyboardInterrupt from error
        
    async def send_message(self, channel_id: str, message) -> None:
        """
        Send a message to a channel

        Args:
            channel_id (_type_): The channel id
            message (_type_): The message
        """
        channel_id = int(channel_id)
        channel = self.get_channel(channel_id)
        await channel.send(message)

    async def on_error(self) -> None:
        """
        Disconnect the bot
        """
        date = datetime.datetime.now().strftime("%H:%M:%S")
        message = f"{LogoChanel.BOT_OFF.value} **{date}** **__Bot__**: Bot déconnecté"
        channel_id = os.getenv("CHANNEL_ID")

        channel_id = int(channel_id)
        channel = self.get_channel(channel_id)

        await channel.send(message)
        
        try:
            await self.close()
        except Exception:
            logging.error("Error: Can't close the bot, it's already closed")


@unique
class Canal(Enum):
    GENERAL = "cMK"
    COMMERCE = "cMK:"
    RECRUTEMENT = "cMK?"
    GUILDE = "cMK%"

class PercoId(Enum):
    ADD_SELF = "gITM"
    ADD_OTHER = "gTS"
    REMOVE = "gTG"
    ATTACK = "gAA"
    SURVIVED = "gAS"
    LOOSE = "gAD"

@unique
class LogoChanel(Enum):
    GENERAL = "⚪"
    COMMERCE = "🟤"
    RECRUTEMENT = "🟡"
    GUILDE = "🟣"
    BOT_ON = "🟢"
    BOT_OFF = "🔴"
    PERCO = ":unicorn:"
    PERCO_ATTACK = ":warning:"
    PERCO_WIN = ":clap:"
    PERCO_LOOSE = ":skull:"


@unique
class RolesHexa(Enum):
    EVERYONE = "@everyone"


async def capture_tcp_payload(interface_name: str, bot: Client):
    """
    Capture the tcp payload

    Args:
        interface_name (str): interface name
        bot (Client): discord bot
    """
    PORT = 443
    capture_filter = f"tcp.srcport == {PORT} and tcp.flags == 0x018"
    capture = pyshark.LiveCapture(
        interface=interface_name, display_filter=capture_filter
    )

    logging.info("Start capture")
    for packet in capture.sniff_continuously():
        if "TCP" in packet:
            tcp_packet = packet["TCP"]
            if payload := tcp_packet.get_field_value("payload"):
                payload_bytes = bytes.fromhex(payload.replace(":", ""))
                decoded_payload = payload_bytes.decode("utf-8", errors="ignore")
                await get_message_from_payload(decoded_payload, bot)


async def get_message_from_payload(
    payload: str,
    bot: Client,
    filter: str = Canal.GUILDE,
) -> str:
    """
    Get the message from the payload

    Args:
        payload (str): payload

    Returns:
        str: message
    """
    
    if payload.startswith("g"):
        logging.info(payload) #! For debug purpose
        
    if payload.startswith(Canal.GENERAL.value):
        MESSAGE_PATTERN = "([^\|]+)\|(\d+)\|([^\|]+)\|([^\|]+)\|"
        match = re.match(MESSAGE_PATTERN, payload)
        if (
            match[1] not in [canal.value for canal in Canal]
            or Canal(match[1]) != filter
        ):
            return

        type_canal = Canal(match[1])
        date = datetime.datetime.now().strftime("%H:%M:%S")
        user = match[3]
        message = match[4]
        message = update_escape_character(message)
        message = message.replace("°0", "[Item]")

        logo = LogoChanel[type_canal.name].value
        chanel_name = f"({type_canal.name.lower()})"
        message = f"{logo} {chanel_name} **{date}** de **__{user}__**: {message}"

        await bot.send_message(
            channel_id=os.getenv("CHANNEL_ID"),
            message=message,
        )
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
        splitted_payload = payload.split("|")
        x_coord = splitted_payload[2]
        y_coord = splitted_payload[3]
        user_name = splitted_payload[4].replace(".", "")
        logo = LogoChanel.GUILDE.value
        date = datetime.datetime.now().strftime("%H:%M:%S")
        message = f"{logo} (guilde) **{date}** {LogoChanel.PERCO.value} Un percepteur à été **posé** en: **({x_coord}, {y_coord})** par **__{user_name}__**"
        await bot.send_message(
            channel_id=os.getenv("CHANNEL_ID"),
            message=message,
        )
    elif payload.startswith(PercoId.REMOVE.value):
        splitted_payload = payload.split("|")
        x_coord = splitted_payload[2]
        y_coord = splitted_payload[3]
        user_name = splitted_payload[4]
        logo = LogoChanel.GUILDE.value
        date = datetime.datetime.now().strftime("%H:%M:%S")
        message = f"{logo} (guilde) **{date}** {LogoChanel.PERCO.value} Un percepteur à été **retiré** en: **({x_coord}, {y_coord})** par **__{user_name}__**"
        await bot.send_message(
            channel_id=os.getenv("CHANNEL_ID"),
            message=message,
        )
    elif payload.startswith(PercoId.ATTACK.value):
        splitted_payload = payload.split("|")
        x_coord = splitted_payload[2]
        y_coord = splitted_payload[3]
        logo = LogoChanel.GUILDE.value
        date = datetime.datetime.now().strftime("%H:%M:%S")
        message = f"{logo} (guilde) **{date}** {LogoChanel.PERCO_ATTACK.value} Un percepteur est **attaqué** en: **({x_coord}, {y_coord})**"
        await bot.send_message(
            channel_id=os.getenv("CHANNEL_ID"),
            message=message,
        )
    elif payload.startswith(PercoId.SURVIVED.value):
        splitted_payload = payload.split("|")
        x_coord = splitted_payload[2]
        y_coord = splitted_payload[3]
        logo = LogoChanel.GUILDE.value
        date = datetime.datetime.now().strftime("%H:%M:%S")
        message = f"{logo} (guilde) **{date}** {LogoChanel.PERCO_WIN.value} Le percepteur en **({x_coord}, {y_coord})** à **survécue**"
        await bot.send_message(
            channel_id=os.getenv("CHANNEL_ID"),
            message=message,
        )
    elif payload.startswith(PercoId.LOOSE.value):
        splitted_payload = payload.split("|")
        x_coord = splitted_payload[2]
        y_coord = splitted_payload[3]
        logo = LogoChanel.GUILDE.value
        date = datetime.datetime.now().strftime("%H:%M:%S")
        message = f"{logo} (guilde) **{date}** {LogoChanel.PERCO_LOOSE.value} Le percepteur en **({x_coord}, {y_coord})** **n'a pas survécue**"
        await bot.send_message(
            channel_id=os.getenv("CHANNEL_ID"),
            message=message,
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
    )
