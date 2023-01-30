""" Constants module """


# Logging config
LOG_FILENAME: str = "server.log"
LOG_FORMAT: str = "%(asctime)s - %(message)s"

# Image generator
HEADER_FONT: str = "FreeSerif.ttf"
FOOTER_FONT: str = "FreeMonoBold.ttf"
FOOTER_TEXT: str = "t.me/textoimagenbot"
IMAGE_PADDING: int = 20

# Requests
GET_TIMEOUT: int = 30
POST_TIMEOUT: int = 50

# Predefined answers to user
ANSWER_CAPTION: str = "@textoimagenbot"
ANSWER_REQUIREMENT: str = "Debe enviar la imagen y el texto en el comentario. "
ANSWER_ERROR: str = "Ha ocurrido un error! "
