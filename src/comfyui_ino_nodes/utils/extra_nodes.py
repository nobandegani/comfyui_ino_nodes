
import json
import asyncio

import hashlib
from datetime import datetime, timezone

from ..node_helper import any_type, ino_print_log

#todo add show any

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

class InoRelay:
    """
        Date Time As String
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "execute": (any_type,),
                "relay": (any_type,),
            },
        }

    RETURN_TYPES = (any_type, any_type, )
    RETURN_NAMES = ("execute", "relay" )
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass

    def function(self, execute, relay):
        return (execute, relay, )

class InoAnyEqual:
    """
        reverse boolean
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input": (any_type, {}),
                "compare": (any_type, {}),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("equal",)

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, input, compare):
        return (input == compare,)

class InoAnyBoolSwitch:
    """
        reverse boolean
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_false": (any_type, {}),
                "input_true": (any_type, {}),
                "condition": ("BOOLEAN", {"default": True, "label_off": "False", "label_on": "True"}),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("output",)

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, input_false, input_true, condition):
        if condition:
            return (input_true,)
        else:
            return (input_false,)

class InoDelayAsync:
    """
        reverse boolean
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "relay": (any_type, {}),
                "delay": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 10000.0, "step": 0.1,}),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("output",)

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    async def function(self, enabled, relay, delay):
        if not enabled:
            return (relay,)

        await asyncio.sleep(delay)
        return (relay,)

class InoPrintLog:
    """
        reverse boolean
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "relay": (any_type, {}),
                "log_message": ("STRING", {"default": "Log message", "multiline": True}),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("output",)

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    async def function(self, enabled, relay, log_message):
        if not enabled:
            return (relay,)

        ino_print_log("", log_message)
        return (relay,)

LOCAL_NODE_CLASS = {
    "InoDateTimeAsString": InoDateTimeAsString,
    "InoRelay": InoRelay,
    "InoAnyEqual": InoAnyEqual,
    "InoAnyBoolSwitch": InoAnyBoolSwitch,
    "InoDelayAsync": InoDelayAsync,
    "InoPrintLog": InoPrintLog,
}
LOCAL_NODE_NAME = {
    "InoDateTimeAsString": "Ino Date Time As String",
    "InoRelay": "Ino Relay",
    "InoAnyEqual": "Ino Any Equal",
    "InoAnyBoolSwitch": "Ino Any Bool Switch",
    "InoDelayAsync": "Ino Delay Async",
    "InoPrintLog": "Ino Print Log",
}
