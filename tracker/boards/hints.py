from tkinter import Label, Button, StringVar
from random import shuffle

from ..constants import Constants as TrackerConstants
from .board import WorkoutBoard


class Hints(WorkoutBoard):
    HINT_PLACEHOLDER = "Unable to load hints"

    def __init__(self, parent, root_render_method):
        super().__init__(parent, root_render_method)

        self._hints = self.state.registered_get("workout_hints")
        shuffle(self._hints)

        self._hint_index = 0
        self._hint__var = StringVar()

        if not self._hints:
            self._hint__var.set(Hints.HINT_PLACEHOLDER)

    @property
    def display_name(self):
        return "Hints"

    @property
    def is_needs_render(self):
        return False

    def update(self):
        if self._hints:
            self._hint__var.set(self._hints[self._hint_index])

    def render(self):
        self._refresh_frame(**TrackerConstants.BOARD_FRAME_STYLE)

        Button(self.frame, text="<", command=lambda: self._update_hint(-1), font=TrackerConstants.BASE_FONT
               ).grid(sticky="nswe")
        Label(self.frame, textvariable=self._hint__var, font=TrackerConstants.BASE_FONT,
              borderwidth=TrackerConstants.RIDGE_WIDTH__NORMAL, relief="ridge"
              ).grid(row=0, column=1, sticky="nswe")
        Button(self.frame, text=">", command=lambda: self._update_hint(1), font=TrackerConstants.BASE_FONT
               ).grid(row=0, column=2, sticky="nswe")

        return self.frame

    def _register_paths(self):
        self.state.register("workout_hints", ["workout_hints"], [[]])

    def _update_hint(self, index_offset):
        """
        Will be deprecated in favour of using a generic method attached to the Board class
        once _trigger_render has been shifted to self.update() or _trigger_update project_wide
        """
        if self._hints:
            self._hint_index = (self._hint_index + index_offset) % len(self._hints)

            self.update()
