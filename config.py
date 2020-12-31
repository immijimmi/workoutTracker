from tracker.boards import *


class Config:
    STATE_FILE_PATH = "data.json"
    ICON_FILE_PATH = r"res/icon.ico"

    INITIAL_BOARDS_VISIBLE = {BoardController}
    BOARDS_LAYOUT = {  # Row and column must be provided. Rowspan and columnspan are defaulted to 1 if not provided
        BoardController: {"row": 0, "column": 0, "rowspan": 3},
        Actuals: {"row": 0, "column": 1, "rowspan": 2, "columnspan": 7},
        Schedule: {"row": 2, "column": 1, "rowspan": 2, "columnspan": 8},
        Tips: {"row": 4, "column": 1, "columnspan": 5},
        File: {"row": 0, "column": 8, "rowspan": 2, "columnspan": 3},
        ScheduleEditor: {"row": 2, "column": 9, "rowspan": 2, "columnspan": 5}
    }  # Note that boards can end up truncated if not given enough rows or columns
