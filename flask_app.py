""" A very simple Flask app for Telegram bots. """
import logging as logger
import os
from pprint import pformat

from dotenv import load_dotenv
from flask import Flask, request

from constants import (
    ANSWER_CAPTION,
    ANSWER_ERROR,
    ANSWER_REQUIREMENT,
    LOG_FILENAME,
    LOG_FORMAT,
)
from generator import add_caption_to_image
from telegram import Telegram

# to log info about the failure if an exection is raised.
logger.basicConfig(filename=LOG_FILENAME, format=LOG_FORMAT, level=logger.DEBUG)

load_dotenv()  # take environment variables from .env
SERVER_BOT_ENDPOINT: str = os.environ.get("TG_BOT_ENDPOINT")
ADMIN_ID: str = os.environ.get("TG_ADMIN_ID")  # To notify admin about failures

app = Flask(__name__)
telegram = Telegram(token=os.environ.get("TG_TEXTOIMAGENBOT_KEY"))


@app.route(f"/{SERVER_BOT_ENDPOINT}", methods=["POST"])
def main():
    """
    Endpoint for the Telegram bot
    """
    data = request.json
    chat_id = data["message"]["chat"]["id"]

    if "caption" not in data["message"] or "photo" not in data["message"]:
        telegram.send_text(text=ANSWER_REQUIREMENT, chat_id=chat_id)
        return "ok", 200

    caption = data["message"]["caption"]
    file_name = data["message"]["photo"][-1]["file_unique_id"]
    file_id = data["message"]["photo"][-1]["file_id"]

    try:
        target_image = telegram.get_tg_file(file_name=file_name, file_id=file_id)
        edited_image = add_caption_to_image(image_name=target_image, caption=caption)
        telegram.send_photo(caption=ANSWER_CAPTION, photo=edited_image, chat_id=chat_id)
        os.remove(target_image)
        os.remove(edited_image)
    except Exception as ex:
        telegram.send_text(text=ANSWER_ERROR + pformat(ex), chat_id=chat_id)
        telegram.send_text(text=pformat(ex), chat_id=ADMIN_ID)
        logger.info("Error processing this: %s", data)
        logger.info(pformat(ex))

    return "ok", 200
