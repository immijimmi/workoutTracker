from tracker.boards import Actuals


class Config:
    STATE_FILENAME = "data.json"
    ICON_FILENAME = "icon.ico"

    """
    BOARDS = {BoardController, Actuals, Schedule, Tips}

    INITIAL_BOARDS_VISIBLE = {BoardController, Tips}
    BOARDS_COLUMNS = (
        (BoardController,),
        (Actuals, Schedule, Tips)
    )
    """

    BOARDS = {Actuals}

    INITIAL_BOARDS_VISIBLE = {Actuals}
    BOARDS_COLUMNS = (
        (Actuals,),
    )
