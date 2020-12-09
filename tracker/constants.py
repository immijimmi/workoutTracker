from managedState.extensions import KeyQueryFactory


class Constants:
    WEEKDAY_KEY_STRINGS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

    PATH_DYNAMIC_KEY = KeyQueryFactory(lambda sub_state, key: key)

    WINDOW_MINSIZE = (255, 33)
    WINDOW_TITLE = "Workout Logger"

    DATE_KEY_FORMAT = "%Y/%m/%d"

    COLOURS = {
        "orange": "#FF9859",
        "yellow": "#FFD800",
        "blue": "#667FFF",
        "green": "#00B211",
        "grey": "#CCCCCC",
        "white": "#FFFFFF",
        "cool_off_white": "#F5F5FF",
        "cool_dark_grey": "#36393F",
    }

    DEFAULT_STYLE_ARGS = {
        "fg": COLOURS["cool_off_white"],
        "bg": COLOURS["cool_dark_grey"]
    }
