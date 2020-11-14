from managedState.registrar import KeyQueryFactory

from datetime import date


class Constants:
    STATE_FILENAME = "data.json"
    ICON_FILENAME = "blank_icon.ico"

    DATE_KEY_FORMAT = "%Y/%m/%d"

    MIN_DATE = date(2020, 1, 1)

    PATH_DYNAMIC_KEY = KeyQueryFactory(lambda sub_state, key: key)

    DIVIDER_SIZE = 4
    SUNKEN_BORDER_WIDTH = 2

    BASE_FONT = ("Verdana", 10)
    HEADER_FONT = ("Verdana", 10, "bold")
    SMALL_ITALICS_FONT = ("Verdana", 9, "normal", "italic")

    FRAME_UPDATE_DELAY = 250

    COLOURS = {
        "orange": "#FF9859",
        "yellow": "#FFD800",
        "blue": "#667FFF",
        "green": "#00B211",
        "grey": "#CCCCCC"
        }
