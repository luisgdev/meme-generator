"""
A very simple Flask app for Telegram bots.
"""
import os
from pprint import pprint

from dotenv import load_dotenv
from flask import Flask, request

import telegram
import utils
from generator import add_caption_to_image

app = Flask(__name__)
load_dotenv()  # take environment variables from .env

SERVER_BOT_ENDPOINT: str = os.environ.get("TG_BOT_ENDPOINT")


# BOT ENDPOINT
@app.route(SERVER_BOT_ENDPOINT, methods=["POST"])
def main():
    """
    Endpoint for the Telegram bot
    """
    data = request.json
    print("DATA FROM TELEGRAM:")
    pprint(data)
    chat_id = data["message"]["chat"]["id"]

    if "caption" not in data["message"] or "photo" not in data["message"]:
        response = "Debe enviar la imagen y el texto en el comentario."
        print(telegram.send_text(text=response, chat_id=chat_id))
        return "ok", 200

    caption = data["message"]["caption"]
    file_name = data["message"]["photo"][-1]["file_unique_id"]
    file_path = data["message"]["photo"][-1]["file_id"]

    try:
        target_image = telegram.get_tg_file(filename=file_name)
        edited_image = add_caption_to_image(image_name=target_image, caption=caption)
        print(telegram.send_photo(caption=caption, photo=edited_image, chat_id=chat_id))
    except Exception as ex:
        response = f"Error: {ex}"
        print(telegram.send_text(text=response, chat_id=chat_id))

    return "ok", 200
