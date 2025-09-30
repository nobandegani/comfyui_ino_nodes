import os
from pathlib import Path
from inopyutils import InoS3Helper

from dotenv import load_dotenv
load_dotenv()

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

def get_s3_instance():
    try:
        s3_instance = InoS3Helper(
            aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
            endpoint_url=os.getenv("S3_ENDPOINT_URL"),
            region_name = os.getenv("S3_REGION_NAME"),
            bucket_name=os.getenv("S3_BUCKET_NAME"),
        )
        return s3_instance
    except Exception as e:
        err = f"Failed to create S3 instance: {e} Please check your environment variables."
        print(err)
        #logger.error(err)
