import random
from datetime import datetime

#---------------------------------InoNotBoolean
class InoNotBoolean:
    """
        reverse boolean
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "boolean": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("BOOLEAN", )
    RETURN_NAMES = ("boolean", )

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, boolean):
        return (not boolean, )


# ---------------------------------InoIntEqual
class InoIntEqual:
    """
        check if its equal to the input Int
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "int_a": ("INT", {
                    "default": 0,
                    "step": 1,
                    "display": "number"
                }),
                "int_b": ("INT", {
                    "default": 0,
                    "step": 1,
                    "display": "number"
                }),
            },

        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("is equal",)

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, int_a, int_b):
        return (int_a == int_b,)


class InoStringToggleCase:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "input_string": ("STRING", {
                    "multiline": True,
                    "default": "Test String"
                }),
                "toggle_to": ("BOOLEAN", {"default": True, "label_off": "Lower", "label_on": "Upper"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("String",)

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, enabled, input_string, toggle_to):
        if not enabled:
            return input_string
        result = str(input_string).upper() if toggle_to else str(input_string).lower()
        return (result,)

class InoBoolToSwitch:
    """
        Convert bool to int, 2 for true, 1 for false
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "input_bool": ("BOOLEAN", {})
            }
        }

    RETURN_TYPES = ("INT", )
    RETURN_NAMES = ("INT", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, enabled, input_bool):
        if not enabled:
            return -1

        if input_bool:
            result = 2
        else:
            result = 1

        return (result, )

class InoStringToCombo:
    """
        Convert string to combo value
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "input_string": ("STRING", {
                    "multiline": False,
                    "default": "default"
                }),
            }
        }

    RETURN_TYPES = ("COMBO", )
    RETURN_NAMES = ("COMBO", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, enabled, input_string):
        if not enabled or not input_string:
            return (input_string, )

        return (input_string, )

class InoDateTimeAsString:
    """
        Date Time As String
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
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


    def function(self, include_year, include_month, include_day,
                      include_hour, include_minute, include_second,
                      date_sep="-", datetime_sep=" ", time_sep=":"):
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

class InoRandomIntInRange:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "int_min": ("INT", {"default": 0}),
                "int_max": ("INT", {"default": 100}),
                "length": ("INT", {"default": 1, "min": 0, "max": 10}),
            }
        }

    RETURN_TYPES = ("INT", "INT", )
    RETURN_NAMES = ("RandomInt", "FormattedInt", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, enabled, int_min, int_max, length):
        if not enabled:
            return (-1, )
        random_int = random.randint(int_min, int_max)
        formatted_int = str(random_int).zfill(length)
        return (random_int, formatted_int, )

class InoIntToString:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_int": ("INT", {"default": 0}),
            }
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("ReturnString", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, input_int):
        return (str(input_int), )
