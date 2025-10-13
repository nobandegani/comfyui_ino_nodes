from pathlib import Path
from inopyutils import InoS3Helper

class S3Helper:
    @staticmethod
    def get_instance(s3_config):
        try:
            s3_instance = InoS3Helper()
            s3_instance.init(
                aws_access_key_id=s3_config["access_key_id"],
                aws_secret_access_key=s3_config["secret_access_key"],
                endpoint_url=s3_config["endpoint_url"],
                region_name=s3_config["region_name"],
                bucket_name=s3_config["bucket_name"],
            )
            return s3_instance
        except Exception as e:
            print(f"Failed to create S3 instance: {e} Please check your environment variables.")

    @staticmethod
    def validate_s3_config(s3_config) -> dict:
        if not s3_config:
            return {
                "success": False,
                "msg": "S3 configuration is required and cannot be empty"
            }

        if not isinstance(s3_config, dict):
            return {
                "success": False,
                "msg": "S3 configuration must be a dictionary"
            }

        required_keys = ["access_key_id", "secret_access_key", "endpoint_url", "region_name", "bucket_name"]
        missing_keys = [key for key in required_keys if key not in s3_config or not s3_config[key]]
        if missing_keys:
            return {
                "success": False,
                "msg": f"S3 configuration missing required keys: {', '.join(missing_keys)}"
            }

        return {
            "success": True,
            "msg": "S3 configuration is valid"
        }

    @staticmethod
    def validate_s3_key(s3_key) -> dict:
        if not s3_key or not s3_key.strip():
            return {
                "success": False,
                "msg": "S3 key is required and cannot be empty"
            }
        return {
            "success": True,
            "msg": "S3 key is valid"
        }

    @staticmethod
    def validate_local_path(local_path) -> dict:
        if not local_path:
            return {
                "success": False,
                "msg": "Local path is required and cannot be empty"
            }

        if not Path(local_path).is_file() and not Path(local_path).is_dir():
            return {
                "success": False,
                "msg": "Local path does not exist"
            }
        return {
            "success": True,
            "msg": "Local path is valid"
        }

    @staticmethod
    def get_save_path(s3_key: str, save_path: str):
        """
            Generate a local file path for saving an S3 object, handling various path formats.

            This function intelligently determines the appropriate local file path based on the
            provided save_path format and the S3 key. It handles three scenarios:
            1. Directory path - saves file with original name from S3 key
            2. Full file path with extension - replaces extension with S3 object's extension
            3. File path without extension - appends S3 object's extension

            Args:
                s3_key (str): The S3 object key (path) from which to extract the filename and extension.
                             Example: "folder/subfolder/document.pdf"
                save_path (str): The desired local save path. Can be:
                                - Directory path ending with '/' or '\\': "/local/dir/"
                                - Full file path with extension: "/local/dir/myfile.txt"
                                - File path without extension: "/local/dir/myfile"

            Returns:
                Path: A pathlib.Path object representing the complete local file path where
                      the S3 object should be saved, including the appropriate file extension.

            Note:
                - The function preserves the file extension from the S3 key in all cases
                - Both forward slashes (/) and backslashes (\\) are recognized as directory indicators
                - If save_path has an extension, it will be replaced with the S3 object's extension
            """
        save_path_obj = Path(save_path)
        s3_key_obj = Path(s3_key)

        if save_path.endswith('/') or save_path.endswith('\\'):
            local_file_path = save_path_obj / s3_key_obj.name
        elif save_path_obj.suffix:
            filename_without_ext = save_path_obj.stem
            s3_extension = s3_key_obj.suffix
            local_file_path = save_path_obj.parent / (filename_without_ext + s3_extension)
        else:
            s3_extension = s3_key_obj.suffix
            local_file_path = Path(save_path + s3_extension)

        return local_file_path

class InoS3Config:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "access_key_id": ("STRING", {"default": ""}),
                "secret_access_key": ("STRING", {"default": ""}),
                "endpoint_url": ("STRING", {"default": ""}),
                "region_name": ("STRING", {"default": ""}),
                "bucket_name": ("STRING", {"default": ""}),
            }
        }

    CATEGORY = "InoS3Helper"
    RETURN_TYPES = ("BOOLEAN", "STRING", )
    RETURN_NAMES = ("success", "config", )
    FUNCTION = "function"

    async def function(self, access_key_id, secret_access_key, endpoint_url, region_name, bucket_name):
        s3_config ={
            "access_key_id": access_key_id,
            "secret_access_key": secret_access_key,
            "endpoint_url": endpoint_url,
            "region_name": region_name,
            "bucket_name": bucket_name,
        }
        return (True, s3_config, )
