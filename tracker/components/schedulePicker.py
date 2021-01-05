from .basicComponents import ButtonListBox
from ..constants import Constants as TrackerConstants


class SchedulePicker(ButtonListBox):
    def __init__(self, board, container, new_schedule_button=False):
        def get_data__button_list_box(list_box):
            schedule_button_style = {"bg": TrackerConstants.COLOURS["cool_less_dark_grey"]}
            default_button_format = "({0})"

            result = [{"value": None, "text": default_button_format.format(None)}]

            schedules = board.state.registered_get("workout_schedules")
            for schedule_id in schedules:
                result.append({
                    "value": schedule_id,
                    "text": schedules[schedule_id]["name"] or default_button_format.format(schedule_id),
                    "style": schedule_button_style if schedules[schedule_id]["name"] else {}
                })

            if new_schedule_button:
                result.append({
                    "value": True,
                    "text": default_button_format.format("New")
                })

            return result

        def on_change__button_list_box(list_box, new_value):
            tracker = board.parent

            if new_value is None:
                board.state.registered_set(None, "active_schedule_id")

            elif new_value is True:
                tracker.state__add_schedule()

            else:
                schedules = board.state.registered_get("workout_schedules")
                if new_value not in schedules:
                    raise ValueError

                board.state.registered_set(new_value, "active_schedule_id")

            tracker.render()

        def get_height__button_list_box():
            return board.height_clearance

        super().__init__(
            container,
            board.state.registered_get("active_schedule_id"),
            get_height__button_list_box,
            get_data=get_data__button_list_box,
            on_change=on_change__button_list_box,
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
