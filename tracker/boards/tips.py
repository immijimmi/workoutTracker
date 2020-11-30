from tkinter import Label, Button, StringVar
from random import shuffle

from ..constants import Constants as TrackerConstants
from tracker.boards.board import WorkoutBoard


class Tips(WorkoutBoard):
    TIP_PLACEHOLDER = "You have not added any tips."

    def __init__(self, parent, root_render_method):
        super().__init__(parent, root_render_method)

        self._frame_stretch["columns"].append(1)
        self._frame_stretch["rows"].append(0)

        self._tips = self.state.registered_get("workout_tips")
        shuffle(self._tips)

        self._tip_index = 0
        self._tip__var = StringVar()

        if not self._tips:
            self._tip__var.set(Tips.TIP_PLACEHOLDER)

    @property
    def display_name(self):
        return "Tips"

    @property
    def is_needs_render(self):
        return False

    def update(self):
        if self._tips:
            self._tip__var.set(self._tips[self._tip_index])

    def render(self):
        self._refresh_frame(**TrackerConstants.BOARD_FRAME_STYLE)

        tip_index_max = len(self._tips)-1

        Button(self.frame, text=TrackerConstants.SYMBOLS["arrows"]["left"],
               command=lambda: self._increment_self_var("_tip_index", -1, max_value=tip_index_max, min_value=0),
               font=TrackerConstants.BASE_FONT, state="disabled" if self._tip_index == 0 else "normal"
               ).grid(ipadx=TrackerConstants.IPADX_SMALL, sticky="nswe")
        Label(self.frame, textvariable=self._tip__var, font=TrackerConstants.SMALL_ITALICS_FONT,
              borderwidth=TrackerConstants.RIDGE_WIDTH__NORMAL, relief="ridge"
              ).grid(row=0, column=1, ipadx=TrackerConstants.IPADX_SMALL, sticky="nswe")
        Button(self.frame, text=TrackerConstants.SYMBOLS["arrows"]["right"],
               command=lambda: self._increment_self_var("_tip_index", 1, max_value=tip_index_max, min_value=0),
               font=TrackerConstants.BASE_FONT, state="disabled" if self._tip_index == tip_index_max else "normal"
               ).grid(row=0, column=2, ipadx=TrackerConstants.IPADX_SMALL, sticky="nswe")

        return self.frame

    def _register_paths(self):
        self.state.register("workout_tips", ["workout_tips"], [[]])
