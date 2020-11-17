from tkinter import Frame, Label, Button
from functools import partial

from ..constants import Constants as TrackerConstants
from .board import Board


class BoardController(Board):
    def __init__(self, parent, root_render_method):
        super().__init__(parent, root_render_method)

    @property
    def is_needs_render(self):
        return False

    def update(self):
        pass

    def render(self):
        if self.frame:
            self.frame.destroy()
        self.frame = Frame(self.parent.frame, borderwidth=TrackerConstants.SUNKEN_BORDER_WIDTH, relief="sunken")

        other_boards = [board for board in self.parent.boards if type(board) != BoardController]

        # Header
        row_index = 0
        Label(self.frame, text="Boards", font=TrackerConstants.BASE_FONT
              ).grid(columnspan=len(other_boards)+2)

        row_index += 1
        self.frame.grid_rowconfigure(row_index, minsize=TrackerConstants.DIVIDER_SIZE)

        row_index += 1
        Label(self.frame, text="Visibility", font=TrackerConstants.BASE_FONT
              ).grid(row=row_index)
        self.frame.grid_columnconfigure(1, minsize=TrackerConstants.DIVIDER_SIZE)
        for board_index, board in enumerate(other_boards):
            Button(self.frame, text=type(board).__name__,
                   command=partial(self._toggle_board_visibility, board),
                   font=TrackerConstants.BASE_FONT
                   ).grid(row=row_index, column=board_index+2)

        return self.frame

    def _toggle_board_visibility(self, board):
        if board in self.parent.visible_boards:
            self.parent.visible_boards.remove(board)
        else:
            self.parent.visible_boards.add(board)

        self._trigger_render()
