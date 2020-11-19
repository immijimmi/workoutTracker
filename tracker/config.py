from .boards import Actuals, Schedule, BoardController, Tips


class Config:
    STATE_FILENAME = "data.json"
    ICON_FILENAME = "blank_icon.ico"

    BOARDS = {BoardController, Actuals, Schedule, Tips}

    INITIAL_BOARDS_VISIBLE = {BoardController, Tips}
    BOARDS_COLUMNS = (
        (Actuals, Schedule, Tips),
        (BoardController,)
    )
