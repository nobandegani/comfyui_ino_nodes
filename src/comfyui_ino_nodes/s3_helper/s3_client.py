import os
from inopyutils import InoS3Helper

from dotenv import load_dotenv
load_dotenv()

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
