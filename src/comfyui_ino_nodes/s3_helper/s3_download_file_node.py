from pathlib import Path

from .s3_client import get_s3_instance
S3_INSTANCE = get_s3_instance()

class InoS3DownloadFile:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "s3_key": ("STRING", {"default": "input/example.png"}),
                "input_path": ("STRING", {"default": "input/example.png"}),
                "save_in": ("BOOLEAN", {"default": True, "label_off": "input", "label_on": "output"})
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING", )
    RETURN_NAMES = ("success", "msg", "result", "rel_path", "abs_path", )
    FUNCTION = "function"

    async def function(self, s3_key, input_path, save_in):
        rel_path: Path
        if save_in:
            rel_path = Path("output") / input_path
        else:
            rel_path = Path("input") / input_path

        abs_path = rel_path.resolve()
        downloaded = await S3_INSTANCE.download_file(
            s3_key=s3_key,
            local_file_path=rel_path
        )
        return (downloaded["success"], downloaded["msg"], downloaded, rel_path, abs_path, )
