from tracker.boards import BoardController, Actuals, Tips


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

    BOARDS = {BoardController, Actuals, Tips}

    INITIAL_BOARDS_VISIBLE = {BoardController, Tips}
    BOARDS_COLUMNS = (
        (BoardController,),
        (Actuals, Tips)
    )
