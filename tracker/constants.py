from managedState.registrar import KeyQueryFactory

from datetime import date


class Constants:
    DATE_KEY_FORMAT = "%Y/%m/%d"
    MIN_DATE = date(2020, 1, 1)
    WEEKDAY_KEY_STRINGS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

    PATH_DYNAMIC_KEY = KeyQueryFactory(lambda sub_state, key: key)

    DIVIDER_SIZE = 4
    SUNKEN_WIDTH__LIGHT = 1
    RIDGE_WIDTH__NORMAL = 2

    BASE_FONT = ("Verdana", 10)
    HEADER_FONT = ("Verdana", 10, "bold")
    SMALL_ITALICS_FONT = ("Verdana", 9, "normal", "italic")

    BOARD_FRAME_STYLE = {"borderwidth": SUNKEN_WIDTH__LIGHT, "relief": "sunken"}

    FRAME_UPDATE_DELAY = 250

    COLOURS = {
        "orange": "#FF9859",
        "yellow": "#FFD800",
        "blue": "#667FFF",
        "green": "#00B211",
        "grey": "#CCCCCC"
        }
