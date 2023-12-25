"""Module for main TCP sniffer"""


import datetime
import logging
import os
import re
from typing import Coroutine

import pyshark

from src.tools.enum import Canal, LogoChanel, PercoId
from src.tools.utils import update_escape_character


class TcpSniffer:
    """
    TCP sniffer
    """

    def __init__(self, interface_name: str, client):
        self.interface_name = interface_name
        self.client = client
        self.port = 443
        self.capture_filter = (
            f"tcp.srcport == {self.port} and tcp.flags == 0x018 and ip"
        )
        self.capture_filter = "tcp and ip"

    async def capture_tcp_payload(self) -> Coroutine:
        """
        Capture the tcp payload

        Args:
            interface_name (str): interface name
            bot (Client): discord bot
        """

        capture = pyshark.LiveCapture(
            interface=self.interface_name, display_filter=self.capture_filter
        )

        logging.info("Start capture")
        for packet in capture.sniff_continuously():
            tcp_packet = packet["TCP"]
            if payload := tcp_packet.get_field_value("payload"):
                payload_bytes = bytes.fromhex(payload.replace(":", ""))
                try:
                    decoded_payload = payload_bytes.decode("utf-8", errors="strict")
                except UnicodeDecodeError:
                    continue
                await self.get_message_from_payload(decoded_payload)

    async def get_message_from_payload(self, payload: str) -> str:
        """
        Get the message from the payload

        Args:
            payload (str): payload

        Returns:
            str: message
        """
        try:
            if payload.startswith(Canal.GENERAL.value):
                await self.handle_general_message(payload)
            elif payload.startswith(PercoId.ADD_SELF.value):
                await self.handle_self_perco_pos_message(payload)
            elif payload.startswith(PercoId.ADD_OTHER.value):
                await self.handle_pos_perco_by_members(payload)
            elif payload.startswith(PercoId.REMOVE.value):
                await self.handle_remove_perco_by_members(payload)
            elif payload.startswith(PercoId.ATTACK.value):
                await self.handle_attack_perco(payload)
            elif payload.startswith(PercoId.SURVIVED.value):
                await self.handle_perco_survived(payload)
            elif payload.startswith(PercoId.LOOSE.value):
                await self.handle_perco_loose(payload)
        except ValueError as error:
            logging.error(error)

    async def handle_general_message(self, payload: str) -> Coroutine:
        """
        Handle all general message

        Args:
            payload (str): payload

        Returns:
            Coroutine: coroutine
        """
        message_pattern = "([^\|]+)\|(\d+)\|([^\|]+)\|([^\|]+)\|"
        match = re.match(message_pattern, payload)
        if (
            match[1] not in [canal.value for canal in Canal]
            or Canal(match[1]) not in Canal
        ):
            return

        type_canal = Canal(match[1])
        date = datetime.datetime.now().strftime("%H:%M:%S")
        user = match[3]
        message = match[4]
        message = update_escape_character(message)

        logo = LogoChanel[type_canal.name].value
        chanel_name = f"({type_canal.name.lower()})"
        message = f"{logo} {chanel_name} **{date}** de **__{user}__**: {message}"

        await self.client.send_message(
            channel_id=os.getenv("CHANNEL_ID"),
            message=message,
        )

    async def handle_self_perco_pos_message(self, payload: str) -> Coroutine:
        """
        Handle self perco pos message

        Args:
            payload (str): payload

        Returns:
            Coroutine: coroutine
        """
        message_pattern = "(-?\d+)\|(-?\d+)\|(\w{1,}).?As"
        match = re.findall(message_pattern, payload)
        if not match:
            return

        x_coord = match[0][0]
        y_coord = match[0][1]
        user_name = match[0][2]

        logo = LogoChanel.GUILDE.value
        date = datetime.datetime.now().strftime("%H:%M:%S")
        message = f"{logo} (guilde) **{date}** {LogoChanel.PERCO.value} Un percepteur à été **posé** en: **({x_coord}, {y_coord})** par **__{user_name}__**"
        await self.client.send_message(
            channel_id=os.getenv("CHANNEL_ID"),
            message=message,
        )

    async def handle_pos_perco_by_members(self, payload: str) -> Coroutine:
        """
        Handle pos perco by members

        Args:
            payload (str): payload

        Returns:
            Coroutine: coroutine
        """
        logo, date, x_coord, y_coord, user_name = self.form_message(
            payload, has_username=True
        )
        message = f"{logo} (guilde) **{date}** {LogoChanel.PERCO.value} Un percepteur à été **posé** en: **({x_coord}, {y_coord})** par **__{user_name}__**"
        await self.client.send_message(
            channel_id=os.getenv("CHANNEL_ID"),
            message=message,
        )

    async def handle_remove_perco_by_members(self, payload: str) -> Coroutine:
        """
        Handle remove perco by members

        Args:
            payload (str): payload

        Returns:
            Coroutine: coroutine
        """
        logo, date, x_coord, y_coord, user_name = self.form_message(
            payload, has_username=True
        )
        message = f"{logo} (guilde) **{date}** {LogoChanel.PERCO.value} Un percepteur à été **retiré** en: **({x_coord}, {y_coord})** par **__{user_name}__**"
        await self.client.send_message(
            channel_id=os.getenv("CHANNEL_ID"),
            message=message,
        )

    async def handle_attack_perco(self, payload: str) -> Coroutine:
        """
        Handle attack perco

        Args:
            payload (str): payload

        Returns:
            Coroutine: coroutine
        """
        logo, date, x_coord, y_coord = self.form_message(payload)
        message = f"{logo} (guilde) **{date}** {LogoChanel.PERCO_ATTACK.value} Un percepteur est **attaqué** en: **({x_coord}, {y_coord})**"
        await self.client.send_message(
            channel_id=os.getenv("CHANNEL_ID"),
            message=message,
        )

    async def handle_perco_survived(self, payload: str) -> Coroutine:
        """
        Handle perco survived

        Args:
            payload (str): payload

        Returns:
            Coroutine: coroutine
        """
        logo, date, x_coord, y_coord = self.form_message(payload)
        message = f"{logo} (guilde) **{date}** {LogoChanel.PERCO.value} Le percepteur en **({x_coord}, {y_coord})** à **survécu**"
        await self.client.send_message(
            channel_id=os.getenv("CHANNEL_ID"),
            message=message,
        )

    async def handle_perco_loose(self, payload: str) -> Coroutine:
        """
        Handle perco loose

        Args:
            payload (str): payload

        Returns:
            Coroutine: coroutine
        """
        logo, date, x_coord, y_coord = self.form_message(payload)
        message = f"{logo} (guilde) **{date}** {LogoChanel.PERCO.value} Le percepteur en **({x_coord}, {y_coord})** **n'a pas survécu**"
        await self.client.send_message(
            channel_id=os.getenv("CHANNEL_ID"),
            message=message,
        )

    def form_message(self, payload: str, has_username: bool = False) -> list[str]:
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
