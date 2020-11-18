from tkinter import Frame, Label, Button
from functools import partial

from ..constants import Constants as TrackerConstants
from .board import Board


class BoardController(Board):
    def __init__(self, parent, root_render_method):
        super().__init__(parent, root_render_method)

    @property
    def display_name(self):
        return "Boards"

    @property
    def is_needs_render(self):
        return False

    def update(self):
        pass

    def render(self):
        if self.frame:
            self.frame.destroy()
        self.frame = Frame(self.parent.frame, borderwidth=TrackerConstants.SUNKEN_WIDTH__LIGHT, relief="sunken")

        other_boards = [board for board in self.parent.boards if type(board) != BoardController]

        # Header
        row_index = 0
        Label(self.frame, text=self.display_name, font=TrackerConstants.BASE_FONT
              ).grid(columnspan=len(other_boards)+2)

        row_index += 1
        self.frame.grid_rowconfigure(row_index, minsize=TrackerConstants.DIVIDER_SIZE)
        self.frame.grid_columnconfigure(1, minsize=TrackerConstants.DIVIDER_SIZE)
        self.frame.grid_columnconfigure(0, minsize=100)

        row_index += 1
        for board_index, board in enumerate(other_boards):
            board_is_visible = board in self.parent.visible_boards

            Label(self.frame, text=board.display_name, font=TrackerConstants.BASE_FONT
                  ).grid(row=row_index)
            Button(self.frame, text="Hide" if board_is_visible else "View",
                   command=partial(self._toggle_board_visibility, board),
                   font=TrackerConstants.BASE_FONT
                   ).grid(row=row_index, column=2, sticky="nswe")

            row_index += 1

        return self.frame

    def _toggle_board_visibility(self, board):
        if board in self.parent.visible_boards:
            self.parent.visible_boards.remove(board)
        else:
            self.parent.visible_boards.add(board)

        self._trigger_render()
