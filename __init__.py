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
from .src.comfyui_ino_nodes.node_utils import InoRandomCharacterPrompt
from .src.comfyui_ino_nodes.node_utils import InoCalculateLoraConfig
from .src.comfyui_ino_nodes.node_utils import InoGetFolderBatchID

from src.comfyui_ino_nodes.utils.extra_nodes import InoBoolToSwitch, InoIntEqual, InoNotBoolean, InoStringToggleCase

from .src.comfyui_ino_nodes.utils.file_helper import Zip, Unzip, RemoveFile, RemoveFolder, IncrementBatchName

from .src.comfyui_ino_nodes.utils.sampler_helper import InoGetModelConfig, InoShowModelConfig, InoGetLoraConfig, InoShowLoraConfig
from .src.comfyui_ino_nodes.utils.sampler_helper import InoLoadSamplerModels, InoGetConditioning, InoGetSamplerConfig

from .src.comfyui_ino_nodes import CloudreveInit, CloudreveSignin, CloudreveUploadFile

NODE_CLASS_MAPPINGS = {
    "Ino_ParseFilePath": InoParseFilePath,
    "Ino_CountFiles": InoCountFiles,
    "Ino_BranchImage": InoBranchImage,
    "Ino_DateTimeAsString": InoDateTimeAsString,
    "Ino_RandomCharacterPrompt": InoRandomCharacterPrompt,
    "Ino_CalculateLoraConfig": InoCalculateLoraConfig,
    "Ino_GetFolderBatchID": InoGetFolderBatchID,

    "Ino_IntEqual": InoIntEqual,
    "Ino_NotBoolean": InoNotBoolean,
    "Ino_StringToggleCase": InoStringToggleCase,
    "Ino_BoolToSwitch": InoBoolToSwitch,

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
}


NODE_DISPLAY_NAME_MAPPINGS = {
    "Ino_ParseFilePath": "Ino Parse File Path",
    "Ino_CountFiles": "Ino Count Files",
    "Ino_BranchImage": "Ino Branch Image",
    "Ino_DateTimeAsString": "Ino DateTime As String",
    "Ino_RandomCharacterPrompt": "Ino Random Character Prompt",
    "Ino_CalculateLoraConfig": "Ino Calculate Lora Config",
    "Ino_GetFolderBatchID": "Ino Get Folder Batch ID",

    "Ino_NotBoolean": "Ino Not Boolean",
    "Ino_IntEqual": "Ino Int Equal",
    "Ino_StringToggleCase": "Ino String Toggle Case",
    "Ino_BoolToSwitch": "Ino Bool To Switch",

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
}


WEB_DIRECTORY = "./web"
