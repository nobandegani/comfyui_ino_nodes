from pathlib import Path

from inopyutils import ino_is_err, InoUtilHelper

import folder_paths
from comfy_api.latest import IO

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import any_type, PARENT_FOLDER_OPTIONS, resolve_comfy_path

class InoS3UploadAudio:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "execute": (any_type,),
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "audio": ("AUDIO",),
                "s3_key": ("STRING", {"default": ""}),
                "parent_folder": (PARENT_FOLDER_OPTIONS, {"default": "output"}),
                "folder": ("STRING", {"default": ""}),
                "filename": ("STRING", {"default": ""})
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING, "tooltip": "you can leave it empty and pass it with env vars"}),
                "date_time_as_name": ("BOOLEAN", {"default": False}),
            },
        }

    RETURN_TYPES = ("AUDIO", "BOOLEAN", "STRING", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("audio", "success", "message", "rel_path", "abs_path", "file_name", "s3_audio_path",)
    FUNCTION = "function"
    OUTPUT_NODE = True
    CATEGORY = "InoS3Helper"

    async def function(self, execute, enabled, audio, s3_key, parent_folder, folder, filename, s3_config=None, date_time_as_name=False):
        if not enabled:
            return (audio, False, "", "", "", "", "",)

        if not execute:
            return (audio, False, "", "", "", "", "",)

        if isinstance(filename, list):
            if len(filename) == 1:
                filename = str(filename[0])
            else:
                return (audio, False, "file name is list", "", "", "", "",)
        elif isinstance(filename, str):
            pass
        else:
            return (audio, False, "file name not string", "", "", "", "",)

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (audio, False, validate_s3_key["msg"], "", "", "", "",)

        if date_time_as_name:
            filename = InoUtilHelper.get_date_time_utc_base64()

        rel_path, abs_path = resolve_comfy_path(parent_folder, folder)

        save_as = "mp3"
        file = f"{filename}.{save_as}"

        from comfy_extras.nodes_audio import SaveAudioMP3

        audio_saver = SaveAudioMP3()
        save_audio: IO.NodeOutput = audio_saver.execute(
            audio=audio,
            filename_prefix=filename,
            format="mp3",
            quality="128k"
        )

        try:
            saved_filename = save_audio.ui.as_dict()["audio"][0]["filename"]
        except:
            return (audio, False, "Audio saved, but failed to get filename", rel_path, abs_path, "", "",)

        parent_path = folder_paths.get_output_directory()
        full_path:Path = Path(parent_path) / saved_filename

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return (audio, False, s3_instance["msg"], rel_path, abs_path, "", "",)
        s3_instance = s3_instance["instance"]

        s3_full_key = f"{s3_key.rstrip('/')}/{saved_filename}"
        s3_result = await s3_instance.upload_file(
            s3_key=s3_full_key,
            local_file_path=str(full_path),
        )
        if not s3_result["success"]:
            return (audio, False, s3_result["msg"], rel_path, abs_path, "", "",)

        return (audio, True, "Success", rel_path, abs_path, file, s3_full_key, )
