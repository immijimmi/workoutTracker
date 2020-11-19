from .boards import Actuals, Schedule, BoardController, Hints


class Config:
    STATE_FILENAME = "data.json"
    ICON_FILENAME = "blank_icon.ico"

    BOARDS = {BoardController, Actuals, Schedule, Hints}

    INITIAL_BOARDS_VISIBLE = {BoardController, Hints}
    BOARDS_COLUMNS = (
        (Actuals, Schedule),
        (BoardController, Hints)
    )
