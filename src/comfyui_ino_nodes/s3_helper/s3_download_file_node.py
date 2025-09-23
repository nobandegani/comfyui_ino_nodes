from .s3_client import get_s3_instance
S3_INSTANCE = get_s3_instance()

class InoS3DownloadFile:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "s3_key": ("STRING", {"default": "input/example.png"}),
                "local_path": ("STRING", {"default": "input/example.png"}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", )
    RETURN_NAMES = ("result", )
    FUNCTION = "function"

    async def function(self, s3_key, local_path):
        downloaded = await S3_INSTANCE.download_file(
            s3_key=s3_key,
            local_file_path=local_path
        )
        print(f"B2 download success: {downloaded}")
        return (downloaded, )
