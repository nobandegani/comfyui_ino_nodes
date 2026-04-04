from pathlib import Path

from inopyutils import ino_is_err, InoUtilHelper

import folder_paths

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import PARENT_FOLDER_OPTIONS, resolve_comfy_path

class InoS3DownloadAudio:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "s3_key": ("STRING", {"default": "input/example.wav"}),
                "parent_folder": (PARENT_FOLDER_OPTIONS, {"default": "temp"}),
                "folder": ("STRING", {"default": ""}),
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING, "tooltip": "you can leave it empty and pass it with env vars"}),
                "bucket_name": ("STRING", {"default": "default"}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "AUDIO", )
    RETURN_NAMES = ("success", "message", "rel_path", "abs_path", "audio", )
    FUNCTION = "function"

    async def function(self, enabled, s3_key, parent_folder, folder, s3_config=None, bucket_name=None):
        if not enabled:
            return (False, "not enabled", "", "", None, )

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"], "", "", None, )

        random_str = InoUtilHelper.get_date_time_utc_base64()
        file_name = f'{random_str}{Path(s3_key).suffix}'
        rel_path, abs_path = resolve_comfy_path(parent_folder, folder, file_name)

        Path(abs_path).parent.mkdir(parents=True, exist_ok=True)

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return (False, s3_instance["msg"], "", "", None, )
        s3_instance = s3_instance["instance"]

        downloaded = await s3_instance.download_file(
            s3_key=s3_key,
            local_file_path=abs_path
        )
        if not downloaded["success"]:
            return (downloaded["success"], downloaded["msg"], rel_path, abs_path, None, )

        from comfy_extras.nodes_audio import LoadAudio

        # Build annotated name for ComfyUI's audio loader
        folder_suffix = folder if folder else ""
        annotated_name = f"{folder_suffix}/{file_name} [{parent_folder}]" if folder_suffix else f"{file_name} [{parent_folder}]"
        load_audio = LoadAudio.execute(audio=annotated_name)

        if load_audio[0]:
            return (True, "Success", rel_path, abs_path, load_audio[0],)

        return (False, "failed to load the audio", rel_path, abs_path, None,)
