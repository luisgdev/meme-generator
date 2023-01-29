"""
A very simple Flask app for Telegram bots.
"""
import os
from pprint import pformat

from dotenv import load_dotenv
from flask import Flask, request

import telegram
from generator import add_caption_to_image

app = Flask(__name__)
load_dotenv()  # take environment variables from .env

SERVER_BOT_ENDPOINT: str = os.environ.get("TG_BOT_ENDPOINT")
ANSWER_CAPTION: str = "@textoimagenbot"
ANSWER_REQUIREMENT: str = "Debe enviar la imagen y el texto en el comentario."
ANSWER_ERROR: str = "Ha ocurrido un error!"


# BOT ENDPOINT
@app.route(f"/{SERVER_BOT_ENDPOINT}", methods=["POST"])
def main():
    """
    Endpoint for the Telegram bot
    """
    data = request.json
    print(f"DATA FROM TELEGRAM: {data}")
    chat_id = data["message"]["chat"]["id"]

    if "caption" not in data["message"] or "photo" not in data["message"]:
        answer = "Debe enviar la imagen y el texto en el comentario."
        print(telegram.send_text(text=answer, chat_id=chat_id))
        return "ok", 200

    caption = data["message"]["caption"]
    file_name = data["message"]["photo"][-1]["file_unique_id"]
    file_id = data["message"]["photo"][-1]["file_id"]

    try:
        target_image = telegram.get_tg_file(file_name=file_name, file_id=file_id)
        edited_image = add_caption_to_image(image_name=target_image, caption=caption)
        print(
            telegram.send_photo(
                caption=ANSWER_CAPTION, photo=edited_image, chat_id=chat_id
            )
        )
        os.remove(target_image)
        os.remove(edited_image)
    except Exception as ex:
        answer = f"Error: {pformat(ex)}"
        print(telegram.send_text(text=answer, chat_id=chat_id))

    return "ok", 200
