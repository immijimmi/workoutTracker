from ..components import ButtonListBox, NumberStepperTable
from ..constants import Constants as TrackerConstants
from .board import Board


class Schedule(Board):
    def __init__(self, parent, container):
        super().__init__(parent, container)

    @property
    def display_name(self):
        return "Schedule"

    def _render(self):
        def on_change__schedule_picker(_schedule_picker, new_value):
            if new_value is None:
                self.state.registered_set(None, "active_schedule_id")

            else:
                schedules = self.state.registered_get("workout_schedules")
                if new_value not in schedules:
                    raise ValueError

                self.state.registered_set(new_value, "active_schedule_id")

            self.parent.render()

        def get_data__schedule_picker(_schedule_picker):
            schedule_button_style = {"bg": TrackerConstants.COLOURS["cool_less_dark_grey"]}
            default_button_format = "({0})"

            result = [{"value": None, "text": default_button_format.format(None)}]

            schedules = self.state.registered_get("workout_schedules")
            for schedule_id in schedules:
                result.append({
                    "value": schedule_id,
                    "text": schedules[schedule_id]["name"] or default_button_format.format(schedule_id),
                    "style": schedule_button_style if schedules[schedule_id]["name"] else {}
                })

            return result

        def on_change__stepper_table(x_value, y_value, _stepper_table, increment_value):
            active_schedule_id = self.state.registered_get("active_schedule_id")

            if active_schedule_id is None:
                return

            self.state.registered_set(
                _stepper_table.value, "scheduled_sets_single_entry", [active_schedule_id, x_value, y_value])

        def get_data__stepper_table(x_value, y_value, _stepper_table):
            active_schedule_id = self.state.registered_get("active_schedule_id")

            if active_schedule_id is None:
                _stepper_table.min = 0
                _stepper_table.max = 0

                return 0

            else:
                return self.state.registered_get("scheduled_sets_single_entry", [active_schedule_id, x_value, y_value])

        self._apply_frame_stretch(rows=[0], columns=[1])

        schedule_picker = ButtonListBox(
            self._frame,
            self.state.registered_get("active_schedule_id"),
            lambda: self.height_clearance,
            get_data=get_data__schedule_picker,
            on_change=on_change__schedule_picker,
            styles={
                "canvas": {
                    "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"]
                },
                "button": {
                    **TrackerConstants.DEFAULT_STYLES["button"],
                    "relief": "raised"
                },
                "button_selected": {
                    "bg": TrackerConstants.COLOURS["default_grey"],
                    "relief": "sunken"
                },
                "scrollbar": {
                    "width": 14  # <14 Will not look symmetrical
                }
            }
        )
        schedule_picker.render().grid(row=0, column=0, sticky="nswe")

        workout_types = self.state.registered_get("workout_types")
        workout_y_values = workout_types.keys()
        workout_y_labels = [workout_types[workout_type_id]["name"] for workout_type_id in workout_y_values]

        stepper_table = NumberStepperTable(
            self._frame,
            [TrackerConstants.WEEKDAY_KEY_STRINGS, workout_y_labels],
            [TrackerConstants.WEEKDAY_KEY_STRINGS, workout_y_values],
            get_data=get_data__stepper_table,
            on_change=on_change__stepper_table,
            limits=(0, None),
            styles={
                "frame": {
                    "bg": TrackerConstants.DEFAULT_STYLE_ARGS["bg"]
                },
                "x_label": {
                    **TrackerConstants.DEFAULT_STYLES["label"],
                    **TrackerConstants.DEFAULT_STYLES["highlight"],
                    "width": 3
                },
                "y_label": {
                    **TrackerConstants.DEFAULT_STYLES["label"],
                    **({"width": max([len(label) for label in workout_y_labels])} if workout_y_labels else {})
                },
                "number_stepper": {
                    "label": {
                        **TrackerConstants.DEFAULT_STYLES["label"],
                        **TrackerConstants.DEFAULT_STYLES["highlight"],
                        "width": 3
                    },
                    "button": {
                        **TrackerConstants.DEFAULT_STYLES["symbol_button"]
                    }
                }
            }
        )
        stepper_table.render().grid(row=0, column=1, sticky="nswe")
