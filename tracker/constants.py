from managedState.registrar import KeyQueryFactory


class Constants:
    STATE_FILENAME = "data.json"
    ICON_FILENAME = "blank_icon.ico"

    PATH_DYNAMIC_KEY = KeyQueryFactory(lambda sub_state, key: key)

    WINDOW_MINSIZE = (270, 80)
    DIVIDER_SIZE = 3

    BASE_FONT = ("Verdana", 10)
    HEADER_FONT = ("Verdana", 10, "bold")
    SMALL_ITALICS_FONT = ("Verdana", 9, "normal", "italic")

    FRAME_UPDATE_DELAY = 250
