from inspect import cleandoc

import os
import fnmatch
import random
import time
import hashlib
from datetime import datetime

#---------------------------------InoParseFilePath
class InoParseFilePath:
    """
        return path, name, extension from full file path
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {
                    "multiline": False,
                    "default": "C:/Local/Programs/5774150451195922272.jpg"
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING", )
    RETURN_NAMES = ("path", "file name", "extension", )
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass


    def function(self, file_path):
        # Normalize the path
        file_path = os.path.normpath(file_path)

        # Split path and file name
        dir_path = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)

        # Split file name and extension
        name, ext = os.path.splitext(base_name)
        ext = ext.lstrip(".")  # Remove leading dot

        return (dir_path, name, ext, )



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
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass


    def function(self, boolean):
        return (not boolean, )





#---------------------------------InoCountFiles
class InoCountFiles:
    """
        count files in folder
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {
                    "multiline": False,
                    "default": "test"
                }),
                "file_pattern": ("STRING", {
                    "multiline": False,
                    "default": "*.*"
                }),
            }
        }

    RETURN_TYPES = ("INT", )
    RETURN_NAMES = ("file count", )
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass


    def function(self, file_path, file_pattern):
        # Normalize and verify
        file_path = os.path.normpath(file_path)
        if not os.path.isdir(file_path):
            return (-1,)

        all_files = os.listdir(file_path)
        pattern = file_pattern.lower()

        # Step 1: split the pattern
        if '.' in pattern:
            name_part, ext_part = pattern.split('.', 1)
            ext_part = ext_part.lower()
        else:
            name_part = pattern
            ext_part = None

        # Step 2: match filename by inclusion
        if name_part == "*":
            name_matches = all_files
        else:
            name_matches = [f for f in all_files if name_part in f.lower()]

        # Step 3: match extension (if any)
        if ext_part != "*":
            final_matches = [f for f in name_matches if f.lower().endswith(f".{ext_part}")]
        else:
            final_matches = name_matches

        return (len(final_matches),)






#---------------------------------InoIntEqual
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

    RETURN_TYPES = ("BOOLEAN", )
    RETURN_NAMES = ("is equal", )
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass


    def function(self, int_a, int_b):
        return (int_a == int_b, )





#---------------------------------InoImageBranch
class InoBranchImage:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "boolean": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "input_image": ("IMAGE", ),
            },
        }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("output_image", )
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass


    def function(self, boolean, input_image=None):
        if boolean:
            return (input_image, )
        else:
            return (input_image, )



#---------------------------------InoImageBranch
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
    DESCRIPTION = cleandoc(__doc__)
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



#---------------------------------InoRandomCharacterPrompt
class InoRandomCharacterPrompt:
    """
        Random Character Prompt
    """

    def __init__(self):
        pass

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

                "main": ("STRING", {
                    "multiline": True,
                    "label": "Main prompt",
                    "default": "blonde hair, oval face, Caucasian, fair skin, 20-30 years old, female"
                }),

                "finetune": ("STRING", {
                    "multiline": True,
                    "label": "Finetune prompt",
                    "default": "pretty, naked, Hair Elegant braided top knot bun, consistent facial features across all 4 frames"
                }),

                "lighting": ("STRING", {
                    "multiline": True,
                    "default": "The lighting is soft and matte, with no gloss or facial shine. The light is evenly diffused and balanced to avoid specular highlights or reflective hotspots on the skin. The face appears naturally lit, with smooth shadows and a non-reflective finish."
                }),

                "camera": ("STRING", {
                    "multiline": True,
                    "default": "Captured with a high-quality DSLR camera using a wide aperture lens, producing a shallow depth of field and a sharp, detailed image. The result is a super realistic portrait with professional photography quality and natural skin tones."
                }),

                "background": ("STRING", {
                    "multiline": True,
                    "default": "The background is plain white, clean and seamless, without texture or distractions."
                }),

                "random_face_shape": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),

                "random_skin_tone": ("BOOLEAN", {"default": False, "label_off": "Disabled", "label_on": "Enabled"}),

                "random_eye_color": ("BOOLEAN", {"default": True, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_eye_shape": ("BOOLEAN", {"default": True, "label_off": "Disabled", "label_on": "Enabled"}),

                "random_eyelashes_style": ("BOOLEAN", {"default": True, "label_off": "Disabled", "label_on": "Enabled"}),

                "random_eyebrow_shape": ("BOOLEAN", {"default": True, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_eyebrow_thickness": ("BOOLEAN", {"default": True, "label_off": "Disabled", "label_on": "Enabled"}),

                "random_nose_shape": ("BOOLEAN", {"default": True, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_nose_size": ("BOOLEAN", {"default": True, "label_off": "Disabled", "label_on": "Enabled"}),

                "random_lip_shape": ("BOOLEAN", {"default": True, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_lip_thickness": ("BOOLEAN", {"default": True, "label_off": "Disabled", "label_on": "Enabled"}),

                "random_facial_marks": ("BOOLEAN", {"default": True, "label_off": "Disabled", "label_on": "Enabled"}),

                "random_makeup_style": ("BOOLEAN", {"default": True, "label_off": "Disabled", "label_on": "Enabled"}),
                "random_blush_or_highlight": ("BOOLEAN", {"default": True, "label_off": "Disabled", "label_on": "Enabled"}),
            },
        }

    RETURN_TYPES = ("STRING", "INT", )
    RETURN_NAMES = ("Prompt", "Seed", )
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass

    def get_index(self, seed, offset, length):
        return (seed + offset) % length

    def function(
        self,
        seed,
        main, finetune, lighting, camera, background,
        random_face_shape, random_skin_tone,
        random_eye_color, random_eye_shape,
        random_eyelashes_style,
        random_eyebrow_shape, random_eyebrow_thickness,
        random_nose_shape, random_nose_size,
        random_lip_shape, random_lip_thickness,
        random_facial_marks, random_makeup_style, random_blush_or_highlight):

        if seed == 0:
            seed_number = random.seed(seed)
            use_random = True
        else:
            use_random = False

        parts = [main, finetune]

        def pick(options, offset):
            if use_random:
                return random.choice(options)
            else:
                return options[self.get_index(seed, offset, len(options))]

        if random_face_shape:
            face_shapes = ["round face", "oval face", "square face", "heart-shaped face", "diamond face", "long face", "triangular face"]
            choice=pick(face_shapes, 10)
            parts.append(choice)

        if random_skin_tone:
            skin_tones = ["pale skin", "light skin", "olive skin", "tan skin", "brown skin", "dark skin", "freckled skin"]
            parts.append(pick(skin_tones, 20))

        if random_eye_color:
            eye_colors = ["blue eyes", "green eyes", "brown eyes", "hazel eyes", "amber eyes", "gray eyes", "violet eyes", "heterochromia eyes"]
            parts.append(pick(eye_colors, 30))

        if random_eye_shape:
            eye_shapes = ["almond shaped eyes", "round shaped eyes", "hooded shaped eyes", "monolid shaped eyes", "upturned shaped eyes", "downturned shaped eyes"]
            parts.append(pick(eye_shapes, 40))

        if random_eyelashes_style:
            eyelash_styles = ["long eyelashes", "short eyelashes", "curled eyelashes", "thick eyelashes", "natural eyelashes"]
            parts.append(pick(eyelash_styles, 50))

        if random_eyebrow_shape:
            eyebrow_shapes = ["arched eyebrows", "straight eyebrows", "curved eyebrows", "angled eyebrows", "soft round eyebrows"]
            parts.append(pick(eyebrow_shapes, 60))

        if random_eyebrow_thickness:
            eyebrow_thicknesses = ["thick eyebrows", "thin eyebrows", "medium eyebrows"]
            parts.append(pick(eyebrow_thicknesses, 70))

        if random_nose_shape:
            nose_shapes = ["button nose", "straight nose", "aquiline nose", "snub nose", "wide nose", "narrow nose"]
            parts.append(pick(nose_shapes, 80))

        if random_nose_size:
            nose_sizes = ["small nose", "medium nose", "large nose"]
            parts.append(pick(nose_sizes, 90))

        if random_lip_shape:
            lip_shapes = ["heart shaped lips", "round shaped lips", "bow shaped lips"]
            parts.append(pick(lip_shapes, 100))

        if random_lip_thickness:
            lip_thicknesses = ["thick lips", "thin lips", "balanced lips"]
            parts.append(pick(lip_thicknesses, 110))

        if random_facial_marks:
            facial_marks = ["light freckles", "beauty mark above lip", "tiny mole near eye", "faint cheek freckling", "subtle beauty spot", "cute nose freckle"]
            parts.append(pick(facial_marks, 120))

        if random_makeup_style:
            makeup_styles = ["natural makeup", "dramatic makeup", "smokey eyes", "glossy lips", "colorful eyeshadow"]
            parts.append(pick(makeup_styles, 130))

        if random_blush_or_highlight:
            blushes = ["rosy cheeks", "soft blush", "dewy highlight", "glowing skin", "matte finish"]
            parts.append(pick(blushes, 140))

        parts.append(lighting)
        parts.append(camera)
        parts.append(background)

        final_prompt = ", ".join(filter(None, parts))
        return (final_prompt, seed, )

        @classmethod
        def IS_CHANGED(cls, seed, **kwargs):
            m = hashlib.sha256()
            m.update(seed)
            return m.digest().hex()
