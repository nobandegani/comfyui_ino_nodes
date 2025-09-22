from .s3_client import get_s3_instance
S3_INSTANCE = get_s3_instance()

class InoS3DownloadFile:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "s3_path": ("STRING", {"default": "input/example.png"}),
                "local_path": ("STRING", {"default": "input/example.png"}),
            }
        }

    CATEGORY = "InoS3Helper"
    INPUT_NODE = True
    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("local_path",)
    FUNCTION = "function"

    def function(self, s3_path, local_path):
        local_path = S3_INSTANCE.download_file(s3_path=s3_path, local_path=local_path)
        print(f"Downloaded file from S3 to {local_path}")
        return local_path
