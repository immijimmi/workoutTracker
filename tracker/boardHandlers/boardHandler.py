from abc import ABC


class BoardHandler(ABC):
    def __init__(self, tracker):
        self.tracker = tracker

    @property
    def board_classes(self):
        raise NotImplementedError

    def arrange_boards(self):
        """
        This function should return a kwargs dict for Component._apply_frame_stretch, to be used by the tracker
        """
        raise NotImplementedError
