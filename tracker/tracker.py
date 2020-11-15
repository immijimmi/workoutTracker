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
        self._window.iconbitmap(Constants.ICON_FILENAME)
        self._window.resizable(False, False)

        self.state = State(extensions=[Registrar, Listeners])
        self._load_state()
        self._register_paths()
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

        self._arrange_boards((board.render(self._frame) for board in self._boards))
        self._frame.pack()

    @staticmethod
    def _arrange_boards(rendered_boards):
        for board in rendered_boards:
            board.pack()

    def _load_state(self):
        try:
            with open(Constants.STATE_FILENAME, "r") as data_file:
                self.state.set(json.loads(data_file.read()))

        except (FileNotFoundError, json.decoder.JSONDecodeError) as ex:
            logging.warning("Unable to load application state from file: {0}".format(ex))

    def _save_state(self):
        with open(Constants.STATE_FILENAME, "w") as data_file:
            data_file.write(json.dumps(self.state.get()))

    def _register_paths(self):
        self.state.register("workout_types", ["workout_types"], [{}])
        self.state.register("workout_type_details", ["workout_types", Constants.PATH_DYNAMIC_KEY], [{}, {}])
        self.state.register("is_workout_disabled",
                            ["workout_types", Constants.PATH_DYNAMIC_KEY, "disabled"], [{}, {}, False])

        self.state.register(
            "scheduled_sets_single_entry",
            ["workout_schedules", Constants.PATH_DYNAMIC_KEY, Constants.PATH_DYNAMIC_KEY],
            [{}, {}, 0])
        self.state.register(
            "completed_sets_single_entry",
            ["workout_log", Constants.PATH_DYNAMIC_KEY, Constants.PATH_DYNAMIC_KEY],
            [{}, {}, 0])
