from tracker.boards import BoardController, Actuals, Tips, Schedule, File


class Config:
    STATE_FILENAME = "data.json"
    ICON_FILENAME = r"res/icon.ico"

    INITIAL_BOARDS_VISIBLE = {BoardController, Tips}
    BOARDS_LAYOUT = {  # row and column must be provided. rowspan and columnspan are defaulted to 1 if not provided
        BoardController: {"row": 0, "column": 0, "rowspan": 3},
        Actuals: {"row": 0, "column": 1, "columnspan": 2},
        Schedule: {"row": 1, "column": 1, "columnspan": 2},
        Tips: {"row": 2, "column": 1, "columnspan": 2},
        File: {"row": 0, "column": 3}
    }
