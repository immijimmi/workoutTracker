from datetime import datetime
from functools import partial
from os import path
from tkinter import Label, Button, StringVar
from tkinter.filedialog import askopenfilename, asksaveasfilename

from ..constants import Constants as TrackerConstants
from ..components import Alert
from .board import Board


class File(Board):
    def __init__(self, parent, container):
        super().__init__(parent, container, update_interval=TrackerConstants.INTERVAL__SHORT_DELAY)

        self.active_alerts = {}

        self._file_path__var = StringVar()
        self._file_path__var.set(self.parent.state_file_path)

    @property
    def display_name(self):
        return "File"

    def _update(self):
        self._file_path__var.set(self.parent.state_file_path)
        self._set_path_label_style()

    def _render(self):
        def get_data__alert(message, alert):
            alert.started = self.active_alerts[message]
            return message

        def set_file_config(operation):
            if operation not in ("Open", "Import", "Save As"):
                raise ValueError

            filetypes = (("JSON Files", "*.json"), ("All Files", "*.*"))
            if operation in ("Open", "Import"):
                selected_file_path = askopenfilename(title=operation, filetypes=filetypes)
            else:
                selected_file_path = asksaveasfilename(title="Save As", filetypes=filetypes, defaultextension=".json")

            if selected_file_path == "":
                return

            selected_file_path = path.relpath(selected_file_path)
            if selected_file_path == self.parent.state_file_path:
                return self._add_alert("Selected file is already open.")

            if operation in ("Open", "Import"):
                loaded = self.parent.load_state(selected_file_path, catch=True)
                if not loaded:
                    return self._add_alert("Unable to open selected file.")
            else:
                saved = self.parent.save_state(selected_file_path, catch=True)
                if not saved:
                    return self._add_alert("Unable to save as selected file name.")

            if operation in ("Open", "Save As"):
                self.parent.state_file_path = selected_file_path
                self.parent.is_state_unsaved = False
            else:
                self.parent.is_state_unsaved = True

            self.parent.render()

        self._expire_alerts()

        self.children["file_path_label"] = None
        self.children["alerts"] = []

        self._apply_frame_stretch(
            rows=[3+len(self.active_alerts)] + ([len(self.active_alerts)] if self.active_alerts else []),
            columns=[0, 4])

        row_index = -1

        for alert_message in self.active_alerts:
            row_index += 1
            alert_component = Alert(
                self._frame,
                TrackerConstants.ALERT_DURATION,
                get_data=partial(get_data__alert, alert_message),
                on_change=lambda alert: self.render(),
                styles={
                    "frame": {
                        "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"],
                        "relief": "ridge",
                        "borderwidth": TrackerConstants.BORDERWIDTH__TINY
                    },
                    "label": {
                        **TrackerConstants.DEFAULT_STYLES["label"],
                        "font": TrackerConstants.SMALL_ITALICS_FONT
                    },
                    "progress_bar": {
                        "frame": {
                            "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"],
                            "padx": TrackerConstants.DEFAULT_STYLE_ARGS["padx"]
                        },
                        "filled_bar_frame": {
                            "bg": TrackerConstants.COLOURS["cool_dark_grey"],
                            "relief": "ridge",
                            "borderwidth": TrackerConstants.BORDERWIDTH__TINY
                        },
                        "empty_bar_frame": {"bg": TrackerConstants.COLOURS["default_grey"]}
                    }
                }
            )
            self.children["alerts"].append(alert_component)
            alert_component.render().grid(row=row_index, column=0, columnspan=5, sticky="nswe")

        row_index += 2
        Label(self._frame, text="Save Location", **TrackerConstants.DEFAULT_STYLES["label"]
              ).grid(row=row_index, column=0, columnspan=5, sticky="nswe")

        row_index += 1
        path_label = Label(self._frame, textvariable=self._file_path__var,
                           **{
                               **TrackerConstants.DEFAULT_STYLES["label"],
                               "relief": "ridge",
                               "borderwidth": TrackerConstants.BORDERWIDTH__SMALL,
                           })
        self.children["file_path_label"] = path_label
        self._set_path_label_style()
        path_label.grid(row=row_index, column=0, columnspan=5, sticky="nswe")

        row_index += 2
        Button(self._frame, text="Open...", width=8, command=lambda: set_file_config("Open"),
               **TrackerConstants.DEFAULT_STYLES["button"]
               ).grid(row=row_index, column=1, sticky="nswe")

        Button(self._frame, text="Import...", width=8, command=lambda: set_file_config("Import"),
               **TrackerConstants.DEFAULT_STYLES["button"]
               ).grid(row=row_index, column=2, sticky="nswe")

        Button(self._frame, text="Save As...", width=8, command=lambda: set_file_config("Save As"),
               **TrackerConstants.DEFAULT_STYLES["button"]
               ).grid(row=row_index, column=3, sticky="nswe")

    def _set_path_label_style(self):
        style = ({"fg": TrackerConstants.COLOURS["yellow"]} if self.parent.is_state_unsaved else
                 {"fg": TrackerConstants.DEFAULT_STYLE_ARGS["fg"]})

        self.children["file_path_label"].config(**style)

    def _add_alert(self, msg):
        self.active_alerts[msg] = datetime.now()
        self.render()

    def _expire_alerts(self):
        now = datetime.now()

        for alert_message, alert_start in tuple(self.active_alerts.items()):
            if (now - alert_start).total_seconds()*1000 > TrackerConstants.ALERT_DURATION:
                del self.active_alerts[alert_message]
