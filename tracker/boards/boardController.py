from tkinter import Label
from functools import partial

from ..components import ToggleButton
from ..constants import Constants as TrackerConstants
from .board import Board


class BoardController(Board):
    def __init__(self, parent, container):
        super().__init__(parent, container)

        self._full_view = True

    @property
    def display_name(self):
        return "Boards"

    def _render(self):
        def toggle_full_view(toggle_button):
            self._full_view = not self._full_view

            self.render()

        def toggle_board_visibility(board_class, toggle_button):
            if board_class in self.parent.visible_boards:
                self.parent.visible_boards.remove(board_class)
            else:
                self.parent.visible_boards.add(board_class)

            self.parent.render()

        self._apply_frame_stretch(rows=[0], columns=[0])

        row_index = 0

        ToggleButton(
            self._frame,
            text_values={True: self.display_name, False: self.display_name},
            on_change=toggle_full_view,
            styles={
                "button": {
                    "font": TrackerConstants.NORMAL_FONT,
                    "width": len(self.display_name),
                    "padx": TrackerConstants.PAD__SMALL,
                    "fg": TrackerConstants.DEFAULT_STYLE_ARGS["fg"],
                    "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"]
                }
            }
        ).render().grid(row=row_index, column=0, columnspan=2, sticky="nswe")

        if self._full_view:
            other_boards = [board for board in self.parent.boards if type(board) != BoardController]

            for other_board in other_boards:
                other_board_class = type(other_board)

                column_index = 0
                row_index += 1

                Label(self._frame, text=other_board.display_name, font=TrackerConstants.NORMAL_FONT,
                      width=len(other_board.display_name), padx=TrackerConstants.PAD__SMALL,
                      fg=TrackerConstants.DEFAULT_STYLE_ARGS["fg"],
                      bg=TrackerConstants.DEFAULT_STYLE_ARGS["bg"]
                      ).grid(row=row_index, column=column_index, sticky="nswe")
                column_index += 1

                ToggleButton(
                    self._frame,
                    get_data=partial(
                        lambda board_class, toggle_button: board_class in self.parent.visible_boards,
                        other_board_class),
                    on_change=partial(toggle_board_visibility, other_board_class),
                    styles={
                        "button": {
                            "font": TrackerConstants.NORMAL_FONT,
                            "width": 4,
                            "padx": TrackerConstants.PAD__SMALL,
                            "fg": TrackerConstants.DEFAULT_STYLE_ARGS["fg"],
                            "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"]
                        }
                    }
                ).render().grid(row=row_index, column=column_index, sticky="nswe")
