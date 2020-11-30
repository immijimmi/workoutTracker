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

        Tracker(self._window, config).render().pack(expand=True, fill='both')
        self._window.mainloop()
