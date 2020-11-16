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
        self._boards = {coords: Config.BOARDS[coords](self.state, self._render) for coords in Config.BOARDS}

        self._render()
        self._window.mainloop()

    @property
    def _is_needs_render(self):
        return any([board.is_needs_render for board in self._boards.values()])

    def _update(self):
        if self._is_needs_render:
            self._render()

        else:
            for board in self._boards.values():
                board.update()

            self._frame.after(Constants.FRAME_UPDATE_DELAY, self._update)

    def _render(self):
        if self._frame:
            self._frame.destroy()
        self._frame = Frame(self._window)

        self._update()

        self._arrange_boards()
        self._frame.pack()

    def _arrange_boards(self):
        board_frames = {board_coords: self._boards[board_coords].render(self._frame) for board_coords in self._boards}
        for frame in board_frames.values():
            frame.update()  # Must be called beforehand to pull the updated dimensions

        column_widths = []
        row_heights = []

        column_count = max((coords[0] for coords in self._boards))+1
        row_count = max((coords[1] for coords in self._boards))+1

        # Calculate the width of each column by getting the width of the widest frame in that column
        for column_index in range(column_count):
            column_width = 0

            column_frames_coords = filter(lambda coords: coords[0] == column_index, board_frames.keys())

            for column_frame_coords in column_frames_coords:
                column_frame = board_frames[column_frame_coords]

                column_width = max(column_width, column_frame.winfo_reqwidth())

            column_widths.append(column_width)

        # Likewise, get the tallest frame's height for each row
        for row_index in range(row_count):
            row_height = 0

            row_frames_coords = filter(lambda coords: coords[1] == row_index, board_frames.keys())

            for row_frame_coords in row_frames_coords:
                row_frame = board_frames[row_frame_coords]

                row_height = max(row_height, row_frame.winfo_reqheight())

            row_heights.append(row_height)

        # Set all frames to the width of the widest frame in their column
        # This is done by adding a new column to that frame with the extra required pixel width
        for column_index, column_width in enumerate(column_widths):
            column_frames_coords = filter(lambda coords: coords[0] == column_index, board_frames.keys())

            for column_frame_coords in column_frames_coords:
                column_frame = board_frames[column_frame_coords]

                current_column_width = column_frame.winfo_reqwidth()

                if current_column_width < column_width:
                    subcolumns_count = column_frame.grid_size()[0]
                    column_frame.grid_columnconfigure(subcolumns_count, minsize=column_width-current_column_width)

        # Likewise again for rows
        for row_index, row_height in enumerate(row_heights):
            row_frames_coords = filter(lambda coords: coords[1] == row_index, board_frames.keys())

            for row_frame_coords in row_frames_coords:
                row_frame = board_frames[row_frame_coords]

                current_row_height = row_frame.winfo_reqheight()

                if current_row_height < row_height:
                    subrows_count = row_frame.grid_size()[1]
                    row_frame.grid_rowconfigure(subrows_count, minsize=row_height-current_row_height)

        for frame_coords in board_frames:
            frame = board_frames[frame_coords]
            frame.grid(row=frame_coords[1], column=frame_coords[0])

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
            "completed_sets_single_entry",
            ["workout_log", Constants.PATH_DYNAMIC_KEY, Constants.PATH_DYNAMIC_KEY],
            [{}, {}, 0])
