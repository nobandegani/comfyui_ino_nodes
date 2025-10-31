from datetime import datetime, timezone, timedelta

class InoDateTimeAsStringSimple:
    """
        Date Time As String
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "step": 1,
                    "label": "Seed (0 = random)",
                    "control_after_generate": True,
                }),
                "input_timezone": (['UTC'], {}),
                "iso_format": ("BOOLEAN", {"default": True, }),
            },
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("output_date_time", )
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass

    def function(self, seed, input_timezone, iso_format):
        now = datetime.now(timezone.utc)
        if iso_format:
            return (now.isoformat(), )
        else:
            return (now.strftime("%Y-%m-%d %H:%M:%S"), )

class InoGetDateTimeDuration:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "datetime_a": ("STRING", {}),
                "datetime_b": ("STRING", {}),
            },
        }

    RETURN_TYPES = ("STRING", "FLOAT", "FLOAT", "FLOAT", "FLOAT",)
    RETURN_NAMES = ("iso_format", "total_seconds", "total_minutes", "total_hours", "total_days",)
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass

    def function(self, datetime_a, datetime_b, ):
        datetime_a: datetime = datetime.fromisoformat(datetime_a)
        datetime_b: datetime = datetime.fromisoformat(datetime_b)

        time_delta: timedelta = datetime_a - datetime_b
        total_seconds: float = time_delta.total_seconds()

        return (time_delta, total_seconds, float(total_seconds/60), float(total_seconds/3600), float(time_delta.days),)

class InoDateTimeAsString:
    """
        Date Time As String
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "step": 1,
                    "label": "Seed (0 = random)"
                }),
                "include_year": ("BOOLEAN", {"default": True, "label_off": "Exclude", "label_on": "Include"}),
                "include_month": ("BOOLEAN", {"default": True, "label_off": "Exclude", "label_on": "Include"}),
                "include_day": ("BOOLEAN", {"default": True, "label_off": "Exclude", "label_on": "Include"}),
                "include_hour": ("BOOLEAN", {"default": True, "label_off": "Exclude", "label_on": "Include"}),
                "include_minute": ("BOOLEAN", {"default": True, "label_off": "Exclude", "label_on": "Include"}),
                "include_second": ("BOOLEAN", {"default": True, "label_off": "Exclude", "label_on": "Include"}),
                "date_sep": ("STRING", {
                    "multiline": False,
                    "default": "-"
                }),
                "datetime_sep": ("STRING", {
                    "multiline": False,
                    "default": "-"
                }),
                "time_sep": ("STRING", {
                    "multiline": False,
                    "default": "-"
                }),
            },
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("output_date_time", )
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        m = hashlib.sha256()
        m.update(seed)
        return m.digest().hex()

    def function(
        self, seed,
        include_year, include_month, include_day,
        include_hour, include_minute, include_second,
        date_sep="-", datetime_sep=" ", time_sep=":"
    ):
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
            return (f"{date_str}{datetime_sep}{time_str}", )
        elif date_str:
            return (date_str, )
        elif time_str:
            return (time_str, )
        else:
            return ("", )

LOCAL_NODE_CLASS = {
    "InoDateTimeAsStringSimple": InoDateTimeAsStringSimple,
    "InoGetDateTimeDuration": InoGetDateTimeDuration,
    "InoDateTimeAsString": InoDateTimeAsString,
}
LOCAL_NODE_NAME = {
    "InoDateTimeAsStringSimple": "Ino Date Time As String Simple",
    "InoGetDateTimeDuration": "Ino Get Date Time Duration",
    "InoDateTimeAsString": "Ino Date Time As String",
}
