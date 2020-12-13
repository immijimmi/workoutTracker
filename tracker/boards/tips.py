from tkComponents.basicComponents import TextCarousel

from ..constants import Constants as TrackerConstants
from .constants import Constants
from .board import Board


class Tips(Board):
    def __init__(self, parent, container):
        super().__init__(parent, container)

    @property
    def display_name(self):
        return "Tips"

    def _render(self):
        def on_change__text_carousel(text_carousel, increment_amount):
            self.parent.tips_index = text_carousel.index

        self._apply_frame_stretch(rows=[0], columns=[0])

        TextCarousel(
            self._frame,
            get_data=lambda carousel: self.parent.tips,
            on_change=on_change__text_carousel,
            index=self.parent.tips_index,
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
