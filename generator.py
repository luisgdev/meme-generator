""" Image generator module """

import os
from typing import List

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

from constants import FOOTER_FONT, FOOTER_TEXT, HEADER_FONT, IMAGE_PADDING


def _wrap_text(font: ImageFont, text: str, max_width: int) -> str:
    """
    Add jump lines to wrap the space to the max width.
    :param font: ImageFont object.
    :param text: Caption str.
    :param max_width: Max widht to wrap.
    :return: String with the wrapped caption.
    """
    if font.getlength(text=text) < max_width:
        return text
    lines: List[str] = []
    words_list: List[str] = text.split(" ")
    result: str = ""
    result_size: float = 0.0
    index: int = 0
    while index < len(words_list):
        if result_size < max_width:
            result += words_list[index] + " "
        else:
            lines.append(result)
            result = words_list[index] + " "
        if index == len(words_list) - 1:
            lines.append(result)
        result_size = font.getlength(text=result)
        index += 1
    return "\n".join(lines)


def add_caption_to_image(image_name: str, caption: str) -> str:
    """
    Generate the image with caption at top.
    :param image_name: Name of the target file.
    :param caption: Caption to add.
    :return: String with the output filename.
    """
    # Caption for the image

    # Load image
    image_path: str = os.path.join(image_name)
    image: Image = Image.open(fp=image_path)

    caption_font_size: int = int(image.width / 18)

    # Create fonts
    try:
        font: FreeTypeFont = ImageFont.truetype(HEADER_FONT, caption_font_size)
        footer_font: FreeTypeFont = ImageFont.truetype(
            FOOTER_FONT, int(caption_font_size * 0.5)
        )
    except Exception:
        font: ImageFont = ImageFont.load_default()
        footer_font: ImageFont = ImageFont.load_default()

    # Split original caption by jump lines
    captions: List[str] = []
    for sentence in caption.split("\n"):
        caption = _wrap_text(
            font=font,
            text=sentence,
            max_width=image.width - caption_font_size * 4.3,
        )
        captions.append(caption)
    caption: str = "\n".join(captions)

    # Determine caption lines required
    lines: int = len(caption.split("\n")) if "\n" in caption else 1

    # Determine blank space to draw caption (margin top)
    header_height: int = int(caption_font_size * (lines + 1))
    new_height: int = image.height + header_height + int(caption_font_size * 0.6)

    # Create new image adding the white space to the target image
    new_image: Image = Image.new(
        mode=image.mode, size=(image.width + IMAGE_PADDING, new_height), color="white"
    )

    # Create draw object to insert caption (header) and footer
    result: ImageDraw = ImageDraw.Draw(new_image)
    result.text(
        (caption_font_size, int(caption_font_size * 0.5)),
        caption,
        font=font,
        fill="black",
    )  # Header
    result.text(
        (
            int(image.width / 2 - footer_font.getlength(text=FOOTER_TEXT) / 2),
            image.height + header_height,
        ),
        text=FOOTER_TEXT,
        font=footer_font,
        fill="black",
    )  # Footer
    # Paste the draw object to the new image
    new_image.paste(im=image, box=(int(IMAGE_PADDING / 2), header_height))
    # Save result
    output_name: str = f"edited-{image_name}"
    new_image.save(os.path.join(output_name))
    return output_name


def demo():
    """main function"""
    add_caption_to_image(
        image_name="carbon.png",
        caption="Hello world.",
    )


if __name__ == "__main__":
    demo()
