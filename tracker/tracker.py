from managedState import State
from managedState.extensions import Registrar, Listeners

import sys
sys.path.insert(0, "C:/Repos/tkComponents")
from tkComponents import Component

import json
import logging

from .constants import Constants


class Tracker(Component):
    def __init__(self, container, config):
        super().__init__(container)

        self._config = config

        self.state = State(extensions=[Registrar, Listeners])
        self._load_state()
        self._register_paths()
        self.state.add_listener("set", lambda metadata: self._save_state())

        self.boards = []
        self.visible_boards = set(self._config.INITIAL_BOARDS_VISIBLE)

    def _render(self):
        self.boards = [BoardClass(self, self._frame) for BoardClass in self._config.BOARDS]

        self._arrange_boards()

    def _arrange_boards(self):
        boards_lookup = {type(board): board for board in self.boards}
        board_frames_grid_layout = []

        for boards_column in self._config.BOARDS_COLUMNS:
            frames_column = []

            for BoardClass in boards_column:
                board = boards_lookup[BoardClass]

                if BoardClass in self.visible_boards:  # Filter out non-visible boards
                    frame = board.render()
                    frames_column.append(frame)

            board_frames_grid_layout.append(frames_column)

        # Remove empty columns
        board_frames_grid_layout = [column for column in board_frames_grid_layout if column]

        for column_index, frames_column in enumerate(board_frames_grid_layout):
            for row_index, frame in enumerate(frames_column):
                frame.grid(row=row_index, column=column_index, sticky="nswe")

    def _load_state(self):
        try:
            with open(self._config.STATE_FILENAME, "r") as data_file:
                self.state.set(json.loads(data_file.read()))

        except (FileNotFoundError, json.decoder.JSONDecodeError) as ex:
            logging.warning("Unable to load application state from file: {0}".format(ex))

    def _save_state(self):
        with open(self._config.STATE_FILENAME, "w") as data_file:
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
