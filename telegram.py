"""
TELEGRAM API MODULE.
"""

import os

import requests
from dotenv import load_dotenv

import utils
from constants import IMAGE_DIR

load_dotenv()  # take environment variables from .env

API_BASE_URL: str = "https://api.telegram.org/bot{TOKEN}"
API_DOWNLOAD_FILE_URL: str = "https://api.telegram.org/file/bot{TOKEN}/{FILE_PATH}"
API_SEND_MSG: str = "/sendMessage"
API_SEND_IMG: str = "/sendPhoto"
API_GET_FILE: str = "/getFile"
API_SET_WEBHOOK: str = "/setWebHook"
GET_TIMEOUT: int = 30
POST_TIMEOUT: int = 50
ADMIN_ID: str = "TG_ADMIN_ID"  # testing purposes only
TG_TOKEN: str = os.environ.get("TG_TEXTOIMAGENBOT_KEY")


def get_tg_file(file_name: str, file_id: str) -> str:
    """
    Download a file received from Telegram message.
    :param file_name: File name to save.
    :param file_id: File id to get from telegram.
    :return: String with the output name.
    """
    response = requests.get(
        url=API_BASE_URL.format(TOKEN=TG_TOKEN) + API_GET_FILE,
        params=dict(file_id=file_id),
        timeout=GET_TIMEOUT,
    )
    if response.status_code != 200:
        raise Exception(f"Error getting file information: {response.text}")
    file_path = response.json()["result"]["file_path"]
    return utils.download_image(
        url=API_DOWNLOAD_FILE_URL.format(TOKEN=TG_TOKEN, FILE_PATH=file_path),
        file_name=file_name,
    )


def send_text(text: str, chat_id: int) -> dict:
    """
    Send Telegram message.
    :param text: Message to send.
    :param chat_id: Chat ID receiver.
    :return: Dict object with Response.
    :raise: Exception if request fail.
    """

    url: str = API_BASE_URL.format(TOKEN=TG_TOKEN) + API_SEND_MSG
    params: dict = dict(chat_id=chat_id, parse_mode="html", text=text)
    response = requests.get(url=url, params=params, timeout=GET_TIMEOUT)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Error sending a text message: {response.text}")


def send_photo(caption: str, photo: str, chat_id: int) -> dict:
    """
    Send Telegram message.
    :param caption: Caption to send.
    :param photo: Message to send.
    :param chat_id: Chat ID receiver.
    :return: Dict object with Response.
    :raise: Exception if request fail.
    """

    with open(os.path.join(photo), "rb") as image:
        response = requests.post(
            url=API_BASE_URL.format(TOKEN=TG_TOKEN) + API_SEND_IMG,
            params=dict(chat_id=chat_id, caption=caption),
            files=dict(photo=image.read()),
            timeout=POST_TIMEOUT
        )
        if response.status_code == 200:
            return response.json()
        raise Exception(response.status_code)


def set_webhook(bot_url: str) -> dict:
    """
    Set webhook for Telegram bot to comunicate with Telegram servers.
    Note: To be ran manually once, in order to set full URL of this server.
    :param bot_url: Server URL where bot is deployed.
    :return: Dict object with Response.
    :raise: Exception if GET request fail.
    """
    url: str = API_BASE_URL.format(TOKEN=TG_TOKEN) + API_SET_WEBHOOK
    params: dict = dict(url=bot_url)
    response = requests.get(url=url, params=params, timeout=GET_TIMEOUT)
    if response.status_code == 200:
        return response.json()
    raise Exception(response.status_code)


if __name__ == "__main__":
    pass
