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

class InoStringToEnum:
    """
        Convert string to enum value
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

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("ENUM", )

    FUNCTION = "function"
    CATEGORY = "InoNodes"

    def function(self, enabled, input_string):
        if not enabled or not input_string:
            return (input_string, )

        return (input_string, )
