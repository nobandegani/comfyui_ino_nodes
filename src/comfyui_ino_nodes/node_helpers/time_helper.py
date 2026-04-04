from datetime import datetime, timezone

from inopyutils import InoUtilHelper

from comfy_api.latest import io


class InoDateTimeAsStringSimple(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoDateTimeAsStringSimple",
            display_name="Ino DateTime Simple",
            category="InoTimeHelper",
            description="Returns the current UTC date and time as a string in ISO or simple format.",
            inputs=[
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff, control_after_generate=True),
                io.Combo.Input("input_timezone", options=["UTC"]),
                io.Boolean.Input("iso_format", default=True),
            ],
            outputs=[
                io.String.Output(display_name="datetime"),
            ],
        )

    @classmethod
    def execute(cls, seed, input_timezone, iso_format) -> io.NodeOutput:
        now = datetime.now(timezone.utc)
        if iso_format:
            return io.NodeOutput(now.isoformat())
        return io.NodeOutput(now.strftime("%Y-%m-%d %H:%M:%S"))


class InoGetDateTimeDuration(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoGetDateTimeDuration",
            display_name="Ino DateTime Duration",
            category="InoTimeHelper",
            description="Calculates the duration between two ISO datetime strings.",
            inputs=[
                io.String.Input("datetime_a"),
                io.String.Input("datetime_b"),
            ],
            outputs=[
                io.String.Output(display_name="iso_format"),
                io.Float.Output(display_name="total_seconds"),
                io.Float.Output(display_name="total_minutes"),
                io.Float.Output(display_name="total_hours"),
                io.Float.Output(display_name="total_days"),
            ],
        )

    @classmethod
    def execute(cls, datetime_a, datetime_b) -> io.NodeOutput:
        dt_a = datetime.fromisoformat(datetime_a)
        dt_b = datetime.fromisoformat(datetime_b)

        time_delta = dt_a - dt_b
        total_seconds = time_delta.total_seconds()

        return io.NodeOutput(
            str(time_delta),
            total_seconds,
            total_seconds / 60,
            total_seconds / 3600,
            float(time_delta.days),
        )


class InoDateTimeAsString(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoDateTimeAsString",
            display_name="Ino DateTime Custom",
            category="InoTimeHelper",
            description="Returns the current date and time as a customizable string with selectable components and separators.",
            inputs=[
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff, control_after_generate=True),
                io.Boolean.Input("include_year", default=True, label_off="Exclude", label_on="Include"),
                io.Boolean.Input("include_month", default=True, label_off="Exclude", label_on="Include"),
                io.Boolean.Input("include_day", default=True, label_off="Exclude", label_on="Include"),
                io.Boolean.Input("include_hour", default=True, label_off="Exclude", label_on="Include"),
                io.Boolean.Input("include_minute", default=True, label_off="Exclude", label_on="Include"),
                io.Boolean.Input("include_second", default=True, label_off="Exclude", label_on="Include"),
                io.String.Input("date_sep", default="-"),
                io.String.Input("datetime_sep", default="-"),
                io.String.Input("time_sep", default="-"),
            ],
            outputs=[
                io.String.Output(display_name="datetime"),
            ],
        )

    @classmethod
    def execute(cls, seed, include_year, include_month, include_day, include_hour, include_minute, include_second, date_sep="-", datetime_sep=" ", time_sep=":") -> io.NodeOutput:
        now = datetime.now()

        date_parts = []
        time_parts = []

        if include_year:
            date_parts.append(str(now.year))
        if include_month:
            date_parts.append(f"{now.month:02d}")
        if include_day:
            date_parts.append(f"{now.day:02d}")

        if include_hour:
            time_parts.append(f"{now.hour:02d}")
        if include_minute:
            time_parts.append(f"{now.minute:02d}")
        if include_second:
            time_parts.append(f"{now.second:02d}")

        date_str = date_sep.join(date_parts) if date_parts else ""
        time_str = time_sep.join(time_parts) if time_parts else ""

        if date_str and time_str:
            return io.NodeOutput(f"{date_str}{datetime_sep}{time_str}")
        elif date_str:
            return io.NodeOutput(date_str)
        elif time_str:
            return io.NodeOutput(time_str)
        return io.NodeOutput("")


class InoGetDateTimeAsBase64(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoGetDateTimeAsBase64",
            display_name="Ino DateTime Base64",
            category="InoTimeHelper",
            description="Returns the current UTC datetime encoded as a base64 string. Unique per execution.",
            inputs=[],
            outputs=[
                io.String.Output(display_name="base64"),
            ],
        )

    @classmethod
    def fingerprint_inputs(cls, **kwargs):
        return InoUtilHelper.get_date_time_utc_base64()

    @classmethod
    def execute(cls) -> io.NodeOutput:
        return io.NodeOutput(InoUtilHelper.get_date_time_utc_base64())


LOCAL_NODE_CLASS = {
    "InoDateTimeAsStringSimple": InoDateTimeAsStringSimple,
    "InoGetDateTimeDuration": InoGetDateTimeDuration,
    "InoDateTimeAsString": InoDateTimeAsString,
    "InoGetDateTimeAsBase64": InoGetDateTimeAsBase64,
}
LOCAL_NODE_NAME = {
    "InoDateTimeAsStringSimple": "Ino DateTime Simple",
    "InoGetDateTimeDuration": "Ino DateTime Duration",
    "InoDateTimeAsString": "Ino DateTime Custom",
    "InoGetDateTimeAsBase64": "Ino DateTime Base64",
}
