from datetime import datetime
from functools import partial
from tkinter import Label, Button, StringVar
from tkinter.filedialog import askopenfilename, asksaveasfilename

from ..constants import Constants as TrackerConstants
from ..components import Alert
from .board import Board


class File(Board):
    def __init__(self, parent, container):
        super().__init__(parent, container)

        self.active_alerts = {}

        self._filename__var = StringVar()
        self._filename__var.set(self.parent.state_filename)

    @property
    def display_name(self):
        return "File"

    def _render(self):
        def get_data__alert(message, alert):
            alert.started = self.active_alerts[message]
            return message

        def on_change__alert(alert):
            self.render()

        def import__button():
            import_filename = askopenfilename()

            #####

        self._expire_alerts()

        self.children["alerts"] = []

        self._apply_frame_stretch(
            rows=[0, 5+len(self.active_alerts)] + ([1+len(self.active_alerts)] if self.active_alerts else []),
            columns=[0, 4])

        row_index = 0

        for alert_message in self.active_alerts:
            row_index += 1
            alert_instance = Alert(
                self._frame,
                TrackerConstants.ALERT_DURATION,
                get_data=partial(get_data__alert, alert_message),
                on_change=on_change__alert,
                styles={
                    "progress_bar": {
                        "width": 20,
                        "filled_frame": {"bg": "blue", "pady": 15, "borderwidth": 3, "relief": "ridge"},
                        "empty_frame": {"bg": "red", "pady": 10}  #####
                    }
                }
            )
            self.children["alerts"].append(alert_instance)
            alert_instance.render().grid(row=row_index, column=1, columnspan=3, sticky="nswe")

        row_index += 2
        Label(self._frame, text="Save Location").grid(row=row_index, column=1, columnspan=3, sticky="nswe")

        row_index += 1
        Label(self._frame, textvariable=self._filename__var).grid(row=row_index, column=1, columnspan=3, sticky="nswe")

        row_index += 1
        def test():
            self.active_alerts["test"] = datetime.now()
            self.render()
        Button(self._frame, text="Test", command=test).grid(row=row_index, column=1, sticky="nswe")

    def _expire_alerts(self):
        now = datetime.now()

        for alert_message, alert_start in tuple(self.active_alerts.items()):
            if (now - alert_start).total_seconds()*1000 > TrackerConstants.ALERT_DURATION:
                del self.active_alerts[alert_message]
