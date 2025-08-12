from inspect import cleandoc

import os
import subprocess

#---------------------------------InoIntEqual
class InoVideoConvert:
    """
        check if its equal to the input Int
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "video_path": ("STRING", {
                    "multiline": False,
                    "default": "/stest/test.mov"
                }),
                "output_format": ("STRING", {
                    "multiline": False,
                    "default": ".mp4"
                }),
                "video_codec": ("STRING", {
                    "multiline": False,
                    "default": "libx264"
                }),
                "crf": ("INT", {
                    "default": 18,
                    "min": 0,
                    "max": 28,
                    "step": 1,
                    "display": "crf"
                }),
                "audio_codec": ("STRING", {
                    "multiline": False,
                    "default": "aac"
                }),
                "audio_bitrate": ("STRING", {
                    "multiline": False,
                    "default": "256k"
                }),
                "preset": ("STRING", {
                    "multiline": False,
                    "default": "slow"
                }),
            },

        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING")
    RETURN_NAMES = ("success", "result", "video_path", )
    DESCRIPTION = cleandoc(__doc__)
    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def __init__(self):
        pass


    def function(self, video_path, output_format, video_codec, crf, audio_codec, audio_bitrate, preset):
        if os.path.splitext(video_path)[1].lower() == output_format:
            return True, f"Already a {output_format} file. Skipping conversion.", video_path

        base, _ = os.path.splitext(video_path)
        output_path = base + output_format

        command = [
            "ffmpeg",
            "-i", video_path,
            "-c:v", video_codec,
            "-crf", str(crf),
            "-preset", preset,
            "-c:a", audio_codec,
            "-b:a", audio_bitrate,
            "-movflags", "+faststart",
            "-y",  # Overwrite if exists
            output_path
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return True, result.stdout.strip(), output_path
        except subprocess.CalledProcessError as e:
            error_message = e.stderr if e.stderr else str(e)
            return False, error_message.strip(), output_path
