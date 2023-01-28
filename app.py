""" Main module """

import os
from typing import List

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

SPACE: str = " "
JUMP: str = "\n"
TEXT_FONT: str = "FreeSerif.ttf"
FOOTER_TEXT: str = "t.me/textoimagenbot"
FOOTER_FONT: str = "FreeMonoBold.ttf"


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
    words_list: List[str] = text.split(SPACE)
    result: str = ""
    result_size: float = 0.0
    index: int = 0
    while index < len(words_list):
        if result_size < max_width:
            result += words_list[index] + SPACE
        else:
            lines.append(result)
            result = words_list[index] + SPACE
        if index == len(words_list) - 1:
            lines.append(result)
        result_size = font.getlength(text=result)
        index += 1
    return JUMP.join(lines)


def generate_image_with_caption(image_name: str, caption: str) -> None:
    """
    Generate the image with caption at top.
    :param image_name: Name of the target file.
    :param caption: Caption to add.
    :return: None
    """
    # Caption for the image

    # Load image
    image_path: str = os.path.join(image_name)
    image: Image = Image.open(fp=image_path)

    caption_font_size: int = int(image.width / 18)

    # Create fonts
    try:
        font: FreeTypeFont = ImageFont.truetype(TEXT_FONT, caption_font_size)
        footer_font: FreeTypeFont = ImageFont.truetype(
            FOOTER_FONT, int(caption_font_size * 0.5)
        )
    except:
        font: ImageFont = ImageFont.load_default()
        footer_font: ImageFont = ImageFont.load_default()

    # Split original caption by jump lines
    captions: List[str] = []
    for sentence in caption.split(JUMP):
        caption = _wrap_text(
            font=font,
            text=sentence,
            max_width=image.width - caption_font_size * 4.3,
        )
        captions.append(caption)
    caption: str = JUMP.join(captions)

    # Determine caption lines required
    lines: int = len(caption.split(JUMP)) if JUMP in caption else 1

    # Determine blank space to draw caption
    top_size: int = int(caption_font_size * (lines + 1))
    new_height: int = image.height + top_size + int(caption_font_size * 0.6)

    # Create new image adding the white space to the target image
    new_image: Image = Image.new(
        mode=image.mode, size=(image.width + 20, new_height), color="white"
    )

    # Create draw object to insert caption (header) and footer
    result: ImageDraw = ImageDraw.Draw(new_image)
    result.text(
        (caption_font_size, int(caption_font_size * 0.5)),
        caption,
        font=font,
        fill=(0, 0, 0),
    )  # Header
    result.text(
        (
            int(image.width / 2)
            - int(footer_font.getlength(text=FOOTER_TEXT) / 2),
            image.height + top_size,
        ),
        text=FOOTER_TEXT,
        font=footer_font,
        fill=(0, 0, 0),
        align="right",
    )  # Footer
    # Paste the draw object to the new image
    new_image.paste(im=image, box=(10, top_size))
    # Save result
    new_image.save(os.path.join(f"edited-{image_name}"))


def demo():
    """main function"""
    generate_image_with_caption(
        image_name="carbon.png",
        caption="Hello world.",
    )


if __name__ == "__main__":
    demo()
