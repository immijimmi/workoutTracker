from tkinter import Tk

from .tracker import Tracker
from .constants import Constants


class App:
    def __init__(self, config):
        self._window = Tk()
        self._window.title(Constants.WINDOW_TITLE)
        self._window.iconbitmap(config.ICON_FILENAME)
        self._window.minsize(*Constants.WINDOW_MINSIZE)
        self._window.resizable(False, False)

        # Make the window expand to fill the screen
        self._window.columnconfigure(0, weight=1)
        self._window.rowconfigure(0, weight=1)

        self.tracker = Tracker(self._window, config).render()
        self.tracker.grid(sticky="nswe")

        self._window.mainloop()
