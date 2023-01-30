""" Telegram API module """

import os

import requests
from requests import Response

import utils
from constants import GET_TIMEOUT, POST_TIMEOUT


class Telegram:
    """
    Telegram HTTP API.
    """

    def __init__(self, token: str) -> None:
        """
        Init function.
        :param token: String with Telegram bot token.
        :return: None
        """
        self._base_api_url: str = f"https://api.telegram.org/bot{token}"
        self._download_file_url: str = f"https://api.telegram.org/file/bot{token}/"
        self.send_message_url: str = self._base_api_url + "/sendMessage"
        self.send_photo_url: str = self._base_api_url + "/sendPhoto"
        self.get_file_info_url: str = self._base_api_url + "/getFile"
        self.set_webhook_url: str = self._base_api_url + "/setWebHook"

    def get_tg_file(self, file_name: str, file_id: str) -> str:
        """
        Download a file received from Telegram message.
        :param file_name: File name to save.
        :param file_id: File id to get from telegram.
        :return: String with the output name.
        """
        res: Response = requests.get(
            url=self.get_file_info_url,
            params=dict(file_id=file_id),
            timeout=GET_TIMEOUT,
        )
        if res.status_code != 200:
            raise Exception(f"Error getting file information: {res.text}")
        file_path = res.json()["result"]["file_path"]
        return utils.download_image(
            url=self._download_file_url + file_path,
            file_name=file_name,
        )

    def send_text(self, text: str, chat_id: int) -> dict:
        """
        Send Telegram message.
        :param text: Message to send.
        :param chat_id: Chat ID receiver.
        :return: Dict object with Response.
        :raise: Exception if request fail.
        """

        res: Response = requests.get(
            url=self.send_message_url,
            params=dict(chat_id=chat_id, text=text, parse_mode="html"),
            timeout=GET_TIMEOUT,
        )
        if res.status_code == 200:
            return res.json()
        raise Exception(f"Error sending a text message: {res.text}")

    def send_photo(self, caption: str, photo: str, chat_id: int) -> dict:
        """
        Send Telegram message.
        :param caption: Caption to send.
        :param photo: Message to send.
        :param chat_id: Chat ID receiver.
        :return: Dict object with Response.
        :raise: Exception if request fail.
        """

        with open(os.path.join(photo), "rb") as image:
            res: Response = requests.post(
                url=self.send_photo_url,
                params=dict(chat_id=chat_id, caption=caption),
                files=dict(photo=image.read()),
                timeout=POST_TIMEOUT,
            )
            if res.status_code == 200:
                return res.json()
            raise Exception(f"Error sending a photo message: {res.text}")

    def set_webhook(self, bot_url: str) -> dict:
        """
        Set webhook for Telegram bot to comunicate with Telegram servers.
        Note: To be ran manually once, in order to set full URL of this server.
        :param bot_url: Server URL where bot is deployed.
        :return: Dict object with Response.
        :raise: Exception if GET request fail.
        """

        res: Response = requests.get(
            url=self.set_webhook_url, params=dict(url=bot_url), timeout=GET_TIMEOUT
        )
        if res.status_code == 200:
            return res.json()
        raise Exception(f"Error setting webhook: {res.text}")


if __name__ == "__main__":
    pass
