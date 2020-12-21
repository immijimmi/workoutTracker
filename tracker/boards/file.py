from datetime import datetime
from functools import partial
from json import decoder
from tkinter import Label, Button, StringVar
from tkinter.filedialog import askopenfilename, asksaveasfilename

from ..constants import Constants as TrackerConstants
from ..components import Alert
from .board import Board


class File(Board):
    def __init__(self, parent, container):
        super().__init__(parent, container)

        self.active_alerts = {}

        self._file_path__var = StringVar()
        self._file_path__var.set(self.parent.state_file_path)

    @property
    def display_name(self):
        return "File"

    def _render(self):
        def get_data__alert(message, alert):
            alert.started = self.active_alerts[message]
            return message

        def on_change__alert(alert):
            self.render()

        def open__button():
            selected_file_path = askopenfilename(filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))
            if selected_file_path == "":
                return

            try:
                self.parent.load_state(selected_file_path)
            except (FileNotFoundError, decoder.JSONDecodeError) as ex:
                self.active_alerts["Unable to open file."] = datetime.now()

                self.render()
                return

            self.parent.state_file_path = selected_file_path
            self._file_path__var.set(self.parent.state_file_path)

        self._expire_alerts()

        self.children["alerts"] = []

        self._apply_frame_stretch(
            rows=[4+len(self.active_alerts)] + ([len(self.active_alerts)] if self.active_alerts else []),
            columns=[1, 3])

        row_index = -1

        for alert_message in self.active_alerts:
            row_index += 1
            alert_component = Alert(
                self._frame,
                TrackerConstants.ALERT_DURATION,
                get_data=partial(get_data__alert, alert_message),
                on_change=on_change__alert,
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

        row_index += 2
        Label(self._frame, textvariable=self._file_path__var,
              **{
                  **TrackerConstants.DEFAULT_STYLES["label"],
                  "relief": "ridge",
                  "borderwidth": TrackerConstants.BORDERWIDTH__SMALL
              }).grid(row=row_index, column=0, columnspan=5, sticky="nswe")

        row_index += 2
        Button(self._frame, text="Open", command=open__button, **TrackerConstants.DEFAULT_STYLES["button"]
               ).grid(row=row_index, column=0, sticky="nswe")

        Button(self._frame, text="Import", **TrackerConstants.DEFAULT_STYLES["button"]
               ).grid(row=row_index, column=2, sticky="nswe")

        Button(self._frame, text="Move", **TrackerConstants.DEFAULT_STYLES["button"]
               ).grid(row=row_index, column=4, sticky="nswe")

    def _expire_alerts(self):
        now = datetime.now()

        for alert_message, alert_start in tuple(self.active_alerts.items()):
            if (now - alert_start).total_seconds()*1000 > TrackerConstants.ALERT_DURATION:
                del self.active_alerts[alert_message]
