from managedState import State
from managedState.registrar import Registrar
from managedState.listeners import Listeners

import json
import logging
from tkinter import Tk, Frame

from .constants import Constants
from .config import Config


class Tracker:
    def __init__(self):
        self._window = Tk()
        self._window.title("Workout Logger")
        self._window.iconbitmap(Config.ICON_FILENAME)
        self._window.resizable(False, False)

        # Make the window expand to fill the screen
        self._window.columnconfigure(0, weight=1)
        self._window.rowconfigure(0, weight=1)

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

        self.frame = None

        self.boards = []
        self.visible_boards = set()
        for board_class in Config.BOARDS:
            board = board_class(self, self._render)
            self.boards.append(board)

            if board_class in Config.INITIAL_BOARDS_VISIBLE:
                self.visible_boards.add(board)

        self._render()
        self._window.mainloop()

    @property
    def _is_needs_render(self):
        return any([(board in self.visible_boards and board.is_needs_render) for board in self.boards])

    def _update(self):
        if self._is_needs_render:
            self._render()

        else:
            for board in self.boards:
                board.update()

            self.frame.after(Constants.FRAME_UPDATE_DELAY, self._update)

    def _render(self):
        if self.frame:
            self.frame.destroy()
        self.frame = Frame(self._window)
        # Make the frame expand to fill the window
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self._update()

        self._arrange_boards()
        self.frame.grid(sticky="nswe")

    def _arrange_boards(self):
        boards_lookup = {type(board): board for board in self.boards}
        board_frames_grid_layout = []

        for boards_column in Config.BOARDS_COLUMNS:
            frames_column = []

            for board_class in boards_column:
                board = boards_lookup[board_class]

                if board in self.visible_boards:  # Filter out non-visible boards
                    frame = board.render()
                    frames_column.append(frame)

            board_frames_grid_layout.append(frames_column)

        # Remove empty columns
        board_frames_grid_layout = [col for col in board_frames_grid_layout if col != []]

        for column_index, frames_column in enumerate(board_frames_grid_layout):
            for row_index, frame in enumerate(frames_column):
                frame.grid(row=row_index, column=column_index, sticky="nswe")

    def _load_state(self):
        try:
            with open(Config.STATE_FILENAME, "r") as data_file:
                self.state.set(json.loads(data_file.read()))

        except (FileNotFoundError, json.decoder.JSONDecodeError) as ex:
            logging.warning("Unable to load application state from file: {0}".format(ex))

    def _save_state(self):
        with open(Config.STATE_FILENAME, "w") as data_file:
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
            "completed_reps_single_entry",
            ["workout_log", Constants.PATH_DYNAMIC_KEY, Constants.PATH_DYNAMIC_KEY],
            [{}, {}, 0])
