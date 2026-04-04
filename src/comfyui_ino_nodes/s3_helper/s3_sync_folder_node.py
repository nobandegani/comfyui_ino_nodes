from pathlib import Path

from inopyutils import ino_is_err

import folder_paths

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import any_type, PARENT_FOLDER_OPTIONS, resolve_comfy_path

class InoS3SyncFolder:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "execute": (any_type,),
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "s3_key": ("STRING", {"default": ""}),
                "parent_folder": (PARENT_FOLDER_OPTIONS,),
                "folder": ("STRING", {"default": "sync/"}),
                "sync_local": ("BOOLEAN", {"default": True, "label_off": "Upload (local->S3)", "label_on": "Download (S3->local)"}),
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING, "tooltip": "you can leave it empty and pass it with env vars"}),
                "concurrency": ("INT", {"default": 5, "min": 1, "max": 10}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "INT", "INT", "INT", "INT",)
    RETURN_NAMES = ("success", "message", "rel_path", "abs_path", "downloaded", "uploaded", "skipped_unchanged", "failed",)
    FUNCTION = "function"
    OUTPUT_NODE = True

    async def function(self, execute, enabled, s3_key, parent_folder, folder, sync_local, s3_config=None, concurrency=5):
        if not enabled:
            return (False, "not enabled", "", "", 0, 0, 0, 0,)

        if not execute:
            return (False, "execute empty", "", "", 0, 0, 0, 0,)

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"], "", "", 0, 0, 0, 0,)

        rel_path, abs_path = resolve_comfy_path(parent_folder, folder)

        local_folder_path = Path(abs_path)
        if not local_folder_path.is_dir():
            local_folder_path.mkdir(parents=True, exist_ok=True)

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return (False, s3_instance["msg"], "", "", 0, 0, 0, 0,)
        s3_instance = s3_instance["instance"]

        s3_result = await s3_instance.sync_folder(
            s3_key=s3_key,
            local_folder_path=abs_path,
            sync_local=sync_local,
            concurrency=concurrency,
        )

        return (
            s3_result["success"],
            s3_result["msg"],
            rel_path,
            abs_path,
            s3_result.get("downloaded", 0),
            s3_result.get("uploaded", 0),
            s3_result.get("skipped_unchanged", 0),
            s3_result.get("failed", 0),
        )
