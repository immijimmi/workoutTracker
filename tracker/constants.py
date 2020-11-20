from managedState.registrar import KeyQueryFactory

from datetime import date


class Constants:
    DATE_KEY_FORMAT = "%Y/%m/%d"
    MIN_DATE = date(2020, 1, 1)
    WEEKDAY_KEY_STRINGS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

    PATH_DYNAMIC_KEY = KeyQueryFactory(lambda sub_state, key: key)

    WINDOW_MINSIZE = (255, 33)
    IPADX_TINY = 1
    IPADX_SMALL = 3
    IPADX_NORMAL = 10
    DIVIDER_SIZE = 4
    SUNKEN_WIDTH__SMALL = 1
    RIDGE_WIDTH__NORMAL = 2

    BASE_FONT = ("Verdana", 10)
    BOLD_FONT = ("Verdana", 10, "bold")
    SMALL_ITALICS_FONT = ("Verdana", 9, "normal", "italic")

    SYMBOLS = {
        "arrows": {
            "up": "^",
            "down": "v",
            "left": "<",
            "right": ">",
        }
    }

    BOARD_FRAME_STYLE = {"borderwidth": SUNKEN_WIDTH__SMALL, "relief": "sunken"}

    FRAME_UPDATE_DELAY = 250

    COLOURS = {
        "orange": "#FF9859",
        "yellow": "#FFD800",
        "blue": "#667FFF",
        "green": "#00B211",
        "grey": "#CCCCCC"
        }
