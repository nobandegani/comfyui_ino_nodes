"""Top-level package for comfyui_ino_nodes."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

__author__ = """InoNodes"""
__email__ = "contact@inoland.net"
__version__ = "0.0.1"

from .src.comfyui_ino_nodes.node_utils import InoParseFilePath
from .src.comfyui_ino_nodes.node_utils import InoCountFiles
from .src.comfyui_ino_nodes.node_utils import InoBranchImage
from .src.comfyui_ino_nodes.node_utils import InoDateTimeAsString
from .src.comfyui_ino_nodes.node_utils import InoGetFolderBatchID

from .src.comfyui_ino_nodes.utils.lora_helper import InoCalculateLoraConfig

from .src.comfyui_ino_nodes.utils.prompt_helper import InoRandomCharacterPrompt

from .src.comfyui_ino_nodes.utils.extra_nodes import InoBoolToSwitch, InoIntEqual, InoNotBoolean, InoStringToggleCase, InoStringToCombo

from .src.comfyui_ino_nodes.utils.file_helper import Zip, Unzip, RemoveFile, RemoveFolder, IncrementBatchName

from .src.comfyui_ino_nodes.utils.sampler_helper import InoGetModelConfig, InoShowModelConfig, InoGetLoraConfig, InoShowLoraConfig
from .src.comfyui_ino_nodes.utils.sampler_helper import InoLoadSamplerModels, InoGetConditioning, InoGetSamplerConfig

from .src.comfyui_ino_nodes.node_cloudreve import CloudreveInit, CloudreveSignin, CloudreveUploadFile

from .src.comfyui_ino_nodes.utils.s3_helper import InoS3UploadFile, InoS3UploadImage

NODE_CLASS_MAPPINGS = {
    "InoParseFilePath": InoParseFilePath,
    "InoCountFiles": InoCountFiles,
    "InoBranchImage": InoBranchImage,
    "InoDateTimeAsString": InoDateTimeAsString,
    "InoGetFolderBatchID": InoGetFolderBatchID,

    "InoCalculateLoraConfig": InoCalculateLoraConfig,

    "InoRandomCharacterPrompt": InoRandomCharacterPrompt,

    "InoIntEqual": InoIntEqual,
    "InoNotBoolean": InoNotBoolean,
    "InoStringToggleCase": InoStringToggleCase,
    "InoBoolToSwitch": InoBoolToSwitch,
    "InoStringToCombo": InoStringToCombo,

    "Zip": Zip,
    "Unzip": Unzip,
    "RemoveFile": RemoveFile,
    "RemoveFolder": RemoveFolder,
    "IncrementBatchName": IncrementBatchName,

    "InoGetModelConfig": InoGetModelConfig,
    "InoShowModelConfig": InoShowModelConfig,
    "InoGetLoraConfig": InoGetLoraConfig,
    "InoShowLoraConfig": InoShowLoraConfig,
    "InoLoadSamplerModels": InoLoadSamplerModels,
    "InoGetConditioning": InoGetConditioning,
    "InoGetSamplerConfig": InoGetSamplerConfig,

    "CloudreveInit": CloudreveInit,
    "CloudreveSignin": CloudreveSignin,
    "CloudreveUploadFile": CloudreveUploadFile,

    "InoS3UploadFile": InoS3UploadFile,
    "InoS3UploadImage": InoS3UploadImage,
}


NODE_DISPLAY_NAME_MAPPINGS = {
    "InoParseFilePath": "Ino Parse File Path",
    "InoCountFiles": "Ino Count Files",
    "InoBranchImage": "Ino Branch Image",
    "InoDateTimeAsString": "Ino DateTime As String",
    "InoGetFolderBatchID": "Ino Get Folder Batch ID",

    "InoCalculateLoraConfig": "Ino Calculate Lora Config",

    "Ino_RandomCharacterPrompt": "Ino Random Character Prompt",

    "InoNotBoolean": "Ino Not Boolean",
    "InoIntEqual": "Ino Int Equal",
    "InoStringToggleCase": "Ino String Toggle Case",
    "InoBoolToSwitch": "Ino Bool To Switch",
    "InoStringToCombo": "Ino String To Combo",

    "Zip": "Zip",
    "Unzip": "Unzip",
    "RemoveFile": "Remove File",
    "RemoveFolder": "Remove Folder",
    "IncrementBatchName": "Increment Batch Name",

    "InoGetModelConfig": "Ino Get Model Config",
    "InoShowModelConfig": "Ino Show Model Config",
    "InoGetLoraConfig": "Ino Get Lora Config",
    "InoShowLoraConfig": "Ino Show Lora Config",
    "InoLoadSamplerModels": "Ino Load Sampler Models",
    "InoGetConditioning": "Ino Get Conditioning",
    "InoGetSamplerConfig": "Ino Get Sampler Config",

    "CloudreveInit": "Cloudreve Init",
    "CloudreveSignin": "Cloudreve Signin",
    "CloudreveUploadFile": "Cloudreve Upload File",

    "InoS3UploadFile": "Ino S3 Upload File",
    "InoS3UploadImage": "Ino S3 Upload Image",
}


WEB_DIRECTORY = "./web"
