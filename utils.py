""" Utils module """

import os

import requests
from requests import Response


def download_image(url: str, file_name: str) -> str:
    """
    Download an image.
    :param url: URL of the image.
    :param file_name: File name.
    :return: String with the output file name.
    :raise: Exception if request fail.
    """
    res: Response = requests.get(url=url, timeout=30)
    if res.status_code != 200:
        raise Exception(f"Error downloading the image: {res.text}")
    output_name: str = f"{file_name}.png"
    try:
        with open(os.path.join(output_name), "wb") as image:
            image.write(res.content)
    except Exception as ex:
        print(f"ERROR: downloading image from telegram failed. {ex}")
    return output_name
