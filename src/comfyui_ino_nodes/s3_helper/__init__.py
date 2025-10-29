from .s3_helper import InoS3Config
from .s3_upload_file_node import InoS3UploadFile
from .s3_upload_folder_node import InoS3UploadFolder
from .s3_upload_image_node import InoS3UploadImage
from .s3_download_file_node import InoS3DownloadFile
from .s3_download_folder_node import InoS3DownloadFolder
from .s3_download_image_node import InoS3DownloadImage
from .s3_upload_string_node import InoS3UploadString
from .s3_get_download_url import InoS3GetDownloadURL
from .s3_download_audio_node import InoS3DownloadAudio
from .s3_upload_audio_node import InoS3UploadAudio

LOCAL_NODE_CLASS = {
    "InoS3Config": InoS3Config,
    "InoS3UploadFile": InoS3UploadFile,
    "InoS3UploadFolder": InoS3UploadFolder,
    "InoS3UploadImage": InoS3UploadImage,
    "InoS3DownloadFile": InoS3DownloadFile,
    "InoS3DownloadFolder": InoS3DownloadFolder,
    "InoS3DownloadImage": InoS3DownloadImage,
    "InoS3UploadString": InoS3UploadString,
    "InoS3GetDownloadURL": InoS3GetDownloadURL,
    "InoS3DownloadAudio": InoS3DownloadAudio,
}
LOCAL_NODE_NAME = {
    "InoS3Config": "Ino S3 Config",
    "InoS3UploadFile": "Ino S3 Upload File",
    "InoS3UploadFolder": "Ino S3 Upload Folder",
    "InoS3UploadImage": "Ino S3 Upload Image",
    "InoS3DownloadFile": "Ino S3 Download File",
    "InoS3DownloadFolder": "Ino S3 Download Folder",
    "InoS3DownloadImage": "Ino S3 Download Image",
    "InoS3UploadString": "Ino S3 Upload String",
    "InoS3GetDownloadURL": "Ino S3 Get Download URL",
    "InoS3DownloadAudio": "Ino S3 Download Audio",
}
