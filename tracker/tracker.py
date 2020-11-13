from managedState import State
from managedState.registrar import Registrar
from managedState.listeners import Listeners

import json
import logging
from tkinter import Tk, Frame

from .constants import Constants


class Tracker:
    def __init__(self, boards=()):
        self._window = Tk()
        self._window.title("Workout Logger")
        self._window.minsize(*Constants.WINDOW_MINSIZE)
        self._window.iconbitmap(Constants.ICON_FILENAME)

        self.state = State(extensions=[Registrar, Listeners])
        self._load_state()
        self.state.add_listener("set", lambda metadata: self._save_state())
        """
        Render on state set disabled for the time being due to a bug that it appears to cause in managedState.
        In the meantime, render method will injected into boards so that they can manually trigger it
        in methods that edit the state.
        """
        # self.state.add_listener("set", lambda metadata: self._render())

        self._frame = None
        self._boards = [board(self.state, self._render) for board in boards]

        self._render()
        self._window.mainloop()

    @property
    def _is_needs_render(self):
        return any([board.is_needs_render for board in self._boards])

    def _update(self):
        if self._is_needs_render:
            self._render()

        else:
            for board in self._boards:
                board.update()

            self._frame.after(Constants.FRAME_UPDATE_DELAY, self._update)

    def _render(self):
        if self._frame:
            self._frame.destroy()
        self._frame = Frame(self._window)

        self._update()
        
        for board in self._boards:
            board.render(self._frame).pack()

        self._frame.pack()

    def _load_state(self):
        try:
            with open(Constants.STATE_FILENAME, "r") as data_file:
                self.state.set(json.loads(data_file.read()))

        except (FileNotFoundError, json.decoder.JSONDecodeError) as ex:
            logging.warning("Unable to load application state from file: {0}".format(ex))

    def _save_state(self):
        with open(Constants.STATE_FILENAME, "w") as data_file:
            data_file.write(json.dumps(self.state.get()))
