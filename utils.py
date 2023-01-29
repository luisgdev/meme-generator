""" Utils module """

import requests
from requests import Response


def download_image(url: str, file_name: str) -> str:
    """
    Download an image.
    :param url: URL of the image.
    :param file_name: File name.
    :return: String with the output file name.
    """
    res: Response = requests.get(url)
    output_name: str = f"{file_name}.png"
    with open(output_name, "wb") as fi:
        fi.write(res.content)
    return output_name