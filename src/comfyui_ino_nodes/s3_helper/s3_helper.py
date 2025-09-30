from pathlib import Path
from inopyutils import InoS3Helper

def get_save_path(s3_key: str, save_path: str):
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

def get_s3_instance(s3_config):
    try:
        s3_instance = InoS3Helper(
            aws_access_key_id=s3_config["access_key_id"],
            aws_secret_access_key=s3_config["secret_access_key"],
            endpoint_url=s3_config["endpoint_url"],
            region_name = s3_config["region_name"],
            bucket_name=s3_config["bucket_name"],
        )
        return s3_instance
    except Exception as e:
        print(f"Failed to create S3 instance: {e} Please check your environment variables.")

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
