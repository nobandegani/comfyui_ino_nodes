"""Top-level package for comfyui_ino_nodes."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

__author__ = """InoNodes"""
__email__ = "contact@inoland.net"
__version__ = "0.0.1"

from .src.comfyui_ino_nodes.node_utils import InoParseFilePath, InoCountFiles, InoBranchImage, InoGetFolderBatchID

from .src.comfyui_ino_nodes.utils.lora_helper import InoCalculateLoraConfig

from .src.comfyui_ino_nodes.utils.prompt_helper import InoRandomCharacterPrompt

from .src.comfyui_ino_nodes.utils.extra_nodes import InoBoolToSwitch, InoIntEqual, InoNotBoolean, InoStringToggleCase, InoStringToCombo, InoDateTimeAsString, InoRandomIntInRange, InoIntToString, InoJson

from .src.comfyui_ino_nodes.utils.file_helper import Zip, Unzip, RemoveFile, RemoveFolder, IncrementBatchName

from .src.comfyui_ino_nodes.utils.sampler_helper import InoRandomNoise, InoGetModelConfig, InoShowModelConfig, InoUpdateModelConfig, InoGetLoraConfig, InoShowLoraConfig, InoLoadSamplerModels, InoGetConditioning, InoGetSamplerConfig

from .src.comfyui_ino_nodes.node_cloudreve import CloudreveInit, CloudreveSignin, CloudreveUploadFile

from .src.comfyui_ino_nodes.s3_helper.s3_helper import InoS3Config
from .src.comfyui_ino_nodes.s3_helper.s3_upload_file_node import InoS3UploadFile
from .src.comfyui_ino_nodes.s3_helper.s3_upload_image_node import InoS3UploadImage
from .src.comfyui_ino_nodes.s3_helper.s3_download_file_node import InoS3DownloadFile
from .src.comfyui_ino_nodes.s3_helper.s3_download_image_node import InoS3DownloadImage

NODE_CLASS_MAPPINGS = {
    "InoParseFilePath": InoParseFilePath,
    "InoCountFiles": InoCountFiles,
    "InoBranchImage": InoBranchImage,

    "InoGetFolderBatchID": InoGetFolderBatchID,

    "InoCalculateLoraConfig": InoCalculateLoraConfig,

    "InoRandomCharacterPrompt": InoRandomCharacterPrompt,

    "InoIntEqual": InoIntEqual,
    "InoNotBoolean": InoNotBoolean,
    "InoStringToggleCase": InoStringToggleCase,
    "InoBoolToSwitch": InoBoolToSwitch,
    "InoStringToCombo": InoStringToCombo,
    "InoDateTimeAsString": InoDateTimeAsString,
    "InoRandomIntInRange": InoRandomIntInRange,
    "InoIntToString": InoIntToString,
    "InoJson": InoJson,

    "Zip": Zip,
    "Unzip": Unzip,
    "RemoveFile": RemoveFile,
    "RemoveFolder": RemoveFolder,
    "IncrementBatchName": IncrementBatchName,

    "InoRandomNoise": InoRandomNoise,
    "InoGetModelConfig": InoGetModelConfig,
    "InoShowModelConfig": InoShowModelConfig,
    "InoUpdateModelConfig": InoUpdateModelConfig,
    "InoGetLoraConfig": InoGetLoraConfig,
    "InoShowLoraConfig": InoShowLoraConfig,
    "InoLoadSamplerModels": InoLoadSamplerModels,
    "InoGetConditioning": InoGetConditioning,
    "InoGetSamplerConfig": InoGetSamplerConfig,

    "CloudreveInit": CloudreveInit,
    "CloudreveSignin": CloudreveSignin,
    "CloudreveUploadFile": CloudreveUploadFile,

    "InoS3Config": InoS3Config,
    "InoS3UploadFile": InoS3UploadFile,
    "InoS3UploadImage": InoS3UploadImage,
    "InoS3DownloadFile": InoS3DownloadFile,
    "InoS3DownloadImage": InoS3DownloadImage,
}


NODE_DISPLAY_NAME_MAPPINGS = {
    "InoParseFilePath": "Ino Parse File Path",
    "InoCountFiles": "Ino Count Files",
    "InoBranchImage": "Ino Branch Image",
    "InoGetFolderBatchID": "Ino Get Folder Batch ID",

    "InoCalculateLoraConfig": "Ino Calculate Lora Config",

    "InoRandomCharacterPrompt": "Ino Random Character Prompt",

    "InoNotBoolean": "Ino Not Boolean",
    "InoIntEqual": "Ino Int Equal",
    "InoStringToggleCase": "Ino String Toggle Case",
    "InoBoolToSwitch": "Ino Bool To Switch",
    "InoStringToCombo": "Ino String To Combo",
    "InoDateTimeAsString": "Ino DateTime As String",
    "InoRandomIntInRange": "Ino Random Int In Range",
    "InoIntToString": "Ino Int To String",
    "InoJson": "Ino Json",

    "Zip": "Zip",
    "Unzip": "Unzip",
    "RemoveFile": "Remove File",
    "RemoveFolder": "Remove Folder",
    "IncrementBatchName": "Increment Batch Name",

    "InoRandomNoise": "Ino Random Noise",
    "InoGetModelConfig": "Ino Get Model Config",
    "InoShowModelConfig": "Ino Show Model Config",
    "InoUpdateModelConfig": "Ino Update Model Config",
    "InoGetLoraConfig": "Ino Get Lora Config",
    "InoShowLoraConfig": "Ino Show Lora Config",
    "InoLoadSamplerModels": "Ino Load Sampler Models",
    "InoGetConditioning": "Ino Get Conditioning",
    "InoGetSamplerConfig": "Ino Get Sampler Config",

    "CloudreveInit": "Cloudreve Init",
    "CloudreveSignin": "Cloudreve Signin",
    "CloudreveUploadFile": "Cloudreve Upload File",

    "InoS3Config": "Ino S3 Config",
    "InoS3UploadFile": "Ino S3 Upload File",
    "InoS3UploadImage": "Ino S3 Upload Image",
    "InoS3DownloadFile": "Ino S3 Download File",
    "InoS3DownloadImage": "Ino S3 Download Image",
}


WEB_DIRECTORY = "./web"
