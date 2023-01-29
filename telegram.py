"""
TELEGRAM API MODULE.
"""

import os
from pprint import pprint
from typing import Optional

import requests
from dotenv import load_dotenv

import utils

load_dotenv()  # take environment variables from .env

API_BASE_URL: str = "https://api.telegram.org/bot{TOKEN}"
API_SEND_MSG: str = "/sendMessage"
API_SEND_IMG: str = "/sendPhoto"
API_SET_WEBHOOK: str = "/setWebHook"
GET_TIMEOUT: int = 30
POST_TIMEOUT: int = 50
API_KEY_NAME: str = "TG_TEXTOIMAGENBOT_KEY"
ADMIN_ID: str = "TG_ADMIN_ID"


def get_tg_file(filename: str) -> str:
    """
    Download a file received from Telegram message.
    :param filename: File name to download.
    :return: String with the output name.
    """
    url: str = (
        f"https://api.telegram.org/file/bot{os.environ.get(API_KEY_NAME)}/{filename}"
    )
    return utils.download_image(url=url,file_name=filename)


def send_text(text: str, chat_id: int) -> dict:
    """
    Send Telegram message.
    :param text: Message to send.
    :param chat_id: Chat ID receiver.
    :return: Dict object with Response.
    :raise: Exception if request fail.
    """

    url: str = API_BASE_URL.format(TOKEN=os.environ.get(API_KEY_NAME)) + API_SEND_MSG
    params: dict = dict(chat_id=chat_id, parse_mode="html", text=text)
    response = requests.get(url=url, params=params, timeout=GET_TIMEOUT)
    if response.status_code == 200:
        return response.json()
    raise Exception(response.status_code)


def send_photo(caption: str, photo: str, chat_id: int) -> dict:
    """
    Send Telegram message.
    :param caption: Caption to send.
    :param photo: Message to send.
    :param chat_id: Chat ID receiver.
    :return: Dict object with Response.
    :raise: Exception if request fail.
    """

    url: str = API_BASE_URL.format(TOKEN=os.environ.get(API_KEY_NAME)) + API_SEND_IMG
    params: dict = dict(chat_id=chat_id, caption=caption)
    files = dict(photo=open(photo, "rb").read())
    response = requests.post(url=url, params=params, files=files, timeout=POST_TIMEOUT)
    if response.status_code == 200:
        return response.json()
    raise Exception(response.status_code)


def set_webhook(bot_url: str) -> dict:
    """
    Set webhook for Telegram bot to comunicate with Telegram servers.
    :param bot_url: Server URL where bot is deployed.
    :return: Dict object with Response.
    :raise: Exception if GET request fail.
    """
    url: str = API_BASE_URL.format(os.environ.get(API_KEY_NAME)) + API_SET_WEBHOOK
    params: dict = dict(url=bot_url)
    response = requests.get(url=url, params=params, timeout=GET_TIMEOUT)
    if response.status_code == 200:
        return response.json()
    raise Exception(response.status_code)


if __name__ == "__main__":
    ADMIN_ID = os.environ.get(ADMIN_ID)
    pprint(send_text(text="Probando!", chat_id=ADMIN_ID))
