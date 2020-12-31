from tkinter import Frame, Label, Button

from ..components import SchedulePicker, StringEditor
from ..constants import Constants as TrackerConstants
from .board import Board


class ScheduleEditor(Board):
    def __init__(self, parent, container):
        super().__init__(parent, container)

    @property
    def display_name(self):
        return "Schedule Editor"

    def _render(self):
        def get_data__string_editor(editor):
            if active_schedule_id is None:
                return ""

            return self.state.registered_get("workout_schedule", [active_schedule_id])["name"]

        def on_change__string_editor(editor, old_value):
            self.children["save_button"].configure(state="normal" if editor.is_unsaved else "disabled")

        def save_schedule_name():
            if active_schedule_id is None:
                return

            new_name = string_editor.value

            schedules = self.state.registered_get("workout_schedules")
            schedules[active_schedule_id]["name"] = new_name

            self.state.registered_set(schedules, "workout_schedules")

            self.parent.render()

        def delete_schedule():
            if active_schedule_id is None:
                return

            self.parent.state__del_schedule(active_schedule_id)

            self.parent.render()

        self._apply_frame_stretch(rows=[3], columns=[1])
        self._apply_dividers(rows=[1, 3], columns=[1])

        schedule_picker = SchedulePicker(self, self._frame, new_schedule_button=True)
        schedule_picker.render().grid(row=0, column=0, rowspan=5, sticky="nswe")

        active_schedule_id = schedule_picker.current_value

        title_column_char_width = 5

        # ID Row
        id_frame = Frame(
            self._frame,
            bg=TrackerConstants.DEFAULT_STYLE_ARGS["bg"],
            **TrackerConstants.DEFAULT_STYLES["highlight"]
        )
        id_title_label = Label(
            id_frame, text="id", width=title_column_char_width, anchor="w",
            **TrackerConstants.DEFAULT_STYLES["label"])
        id_value_label = Label(
            id_frame, text=str(active_schedule_id), anchor="w", **TrackerConstants.DEFAULT_STYLES["label"])

        id_title_label.grid(row=0, column=0, sticky="nswe")
        id_value_label.grid(row=0, column=1,  sticky="nswe")
        id_frame.grid(row=0, column=2, columnspan=3, sticky="nswe")

        # Name Row
        name_frame = Frame(
            self._frame,
            bg=TrackerConstants.DEFAULT_STYLE_ARGS["bg"],
            **TrackerConstants.DEFAULT_STYLES["highlight"]
        )
        name_title_label = Label(
            name_frame, text="name", width=title_column_char_width, anchor="w",
            **TrackerConstants.DEFAULT_STYLES["label"])
        string_editor = StringEditor(
            name_frame,
            get_data=get_data__string_editor,
            on_change=on_change__string_editor,
            update_interval=TrackerConstants.INTERVAL__SHORT_DELAY,
            styles={
                "frame": {
                    "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"],
                    "padx": TrackerConstants.DEFAULT_STYLE_ARGS["padx"],
                    "pady": TrackerConstants.DEFAULT_STYLE_ARGS["pady"],
                },
                "entry": {
                    "bg": TrackerConstants.COLOURS["cool_less_dark_grey"],
                    "font": TrackerConstants.DEFAULT_STYLE_ARGS["font"],
                    "insertbackground": TrackerConstants.DEFAULT_STYLE_ARGS["fg"],
                },
                "entry_unsaved": {
                    **TrackerConstants.DEFAULT_STYLES["unsaved"]
                },
                "entry_saved": {
                    "fg": TrackerConstants.DEFAULT_STYLE_ARGS["fg"]
                }
            }
        )
        self.children["string_editor"] = string_editor

        name_title_label.grid(row=0, column=0, sticky="nswe")
        string_editor.render().grid(row=0, column=1, sticky="nswe")
        name_frame.grid(row=2, column=2, columnspan=3, sticky="nswe")

        # Buttons
        save_button = Button(
            self._frame, text="Save", width=6, command=save_schedule_name, **TrackerConstants.DEFAULT_STYLES["button"])
        self.children["save_button"] = save_button
        delete_button = Button(
            self._frame, text="Delete", width=6, command=delete_schedule, **TrackerConstants.DEFAULT_STYLES["button"])

        save_button.grid(row=4, column=3, sticky="nswe")
        delete_button.grid(row=4, column=4, sticky="nswe")

        save_button.configure(state="disabled")
        if active_schedule_id is None:
            string_editor.children["entry"].configure(state="disabled")
            delete_button.configure(state="disabled")

        max_title_column_width = name_title_label.winfo_reqwidth()
        self._frame.grid_columnconfigure(2, minsize=max_title_column_width)
