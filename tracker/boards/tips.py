from tkComponents.basicComponents import TextCarousel

from random import shuffle

from ..constants import Constants as TrackerConstants
from .constants import Constants
from .board import Board


class Tips(Board):
    TIP_PLACEHOLDER = "You have not added any tips."

    def __init__(self, parent, container):
        super().__init__(parent, container)

        self._tips = self.state.registered_get("workout_tips")
        shuffle(self._tips)

    @property
    def display_name(self):
        return "Tips"

    def _render(self):
        self._apply_frame_stretch(rows=[0], columns=[0])

        TextCarousel(
            self._frame,
            get_data=lambda carousel: self._tips,
            styles={
                "button": {
                    "font": Constants.SYMBOL_FONT,
                    "width": 1,
                    "padx": Constants.PAD__SMALL,
                    **TrackerConstants.DEFAULT_STYLE_ARGS
                },
                "label": {
                    "font": Constants.SMALL_ITALICS_FONT,
                    **TrackerConstants.DEFAULT_STYLE_ARGS
                }
            }
        ).render().grid(row=0, column=0, sticky="nswe")

    def _register_paths(self):
        self.state.register("workout_tips", ["workout_tips"], [[Tips.TIP_PLACEHOLDER]])
