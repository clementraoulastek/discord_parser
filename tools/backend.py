import threading
import time
import requests
from typing import Optional, Tuple
import logging
from tools.logger import logger
import json
import random
from dotenv import load_dotenv
import os

logger()
load_dotenv()

TOKEN = "NDQ2MzU2NzU1MDYxMTQ1NjEy.GGwpCk.yVbEaQ8lRi4tsMOgghfUoTaHlOs9i1LjQANpfg"


def parse_messages(channel_id: str, token: Optional[str]) -> Tuple[dict, str]:
    header = {"Authorization": token}

    endpoint = f"https://discord.com/api/v10/channels/{channel_id}/messages?limit=1"
    response = requests.get(endpoint, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Error: {response.text}")


def response_to_message(message_id: str, channel_id: str, token: str, message) -> None:
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
    }
    # Define the message data with a message reference
    message_data = {"content": message, "message_reference": {"message_id": message_id}}
    endpoint = f"https://discord.com/api/v10/channels/{channel_id}/messages"

    # Send the POST request
    response = requests.post(endpoint, headers=headers, data=json.dumps(message_data))


def send_message(channel_id: str, message: str) -> None:
    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json",
    }
    # Define the message data with a message reference
    endpoint = f"https://discord.com/api/v10/channels/{channel_id}/messages"

    message_data = {"content": message}
    response = requests.post(
        endpoint, headers=headers, data=json.dumps(message_data)
    )
    if response.status_code != 200:
        print(response.text)


def have_permission(channel_id: int) -> bool:
    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json",
    }
    endpoint = f"https://discord.com/api/v10/channels/{channel_id}"
    response = requests.get(endpoint, headers=headers)
    return response.status_code == 200


def get_channel_id(guild_id: int) -> str:
    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json",
    }
    endpoint = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Error: {response.status_code}")


def check_if_message_is_everyone(channel_id) -> None:
    while True:
        response = parse_messages(channel_id, TOKEN)
        if response and "@everyone" in response[0]["content"].lower():
            response_to_message(
                response[0]["id"], channel_id, TOKEN, message="ta yeule"
            )
        time.sleep(random.randint(5, 10))


def check_message(channel_id) -> None:
    response = parse_messages(channel_id, TOKEN)
    print(response)
    


check_message("1165686485245251654")