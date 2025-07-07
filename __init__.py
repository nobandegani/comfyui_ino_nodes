"""Top-level package for comfyui_ino_nodes."""

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

__author__ = """InoNodes"""
__email__ = "contact@inoland.net"
__version__ = "0.0.1"


from .src.comfyui_ino_nodes.node_bedrive_saveimage import BeDriveSaveImage
from .src.comfyui_ino_nodes.node_bedrive_savefile import BeDriveSaveFile
from .src.comfyui_ino_nodes.node_bedrive_getparentid import BeDriveGetParentID

from .src.comfyui_ino_nodes.node_utils import InoParseFilePath
from .src.comfyui_ino_nodes.node_utils import InoNotBoolean
from .src.comfyui_ino_nodes.node_utils import InoCountFiles
from .src.comfyui_ino_nodes.node_utils import InoIntEqual
from .src.comfyui_ino_nodes.node_utils import InoBranchImage
from .src.comfyui_ino_nodes.node_utils import InoDateTimeAsString
from .src.comfyui_ino_nodes.node_utils import InoRandomCharacterPrompt
from .src.comfyui_ino_nodes.node_utils import InoCalculateLoraConfig

from .src.comfyui_ino_nodes.node_video_convert import InoVideoConvert

from .src.comfyui_ino_nodes.node_cloudreve import Cloudreve_Get_Captcha

NODE_CLASS_MAPPINGS = {
    "Ino_SaveImage": BeDriveSaveImage,
    "Ino_SaveFile": BeDriveSaveFile,
    "Ino_GetParentID": BeDriveGetParentID,

    "Ino_ParseFilePath": InoParseFilePath,
    "Ino_NotBoolean": InoNotBoolean,
    "Ino_CountFiles": InoCountFiles,
    "Ino_IntEqual": InoIntEqual,
    "Ino_BranchImage": InoBranchImage,
    "Ino_DateTimeAsString": InoDateTimeAsString,
    "Ino_RandomCharacterPrompt": InoRandomCharacterPrompt,
    "Ino_CalculateLoraConfig": InoCalculateLoraConfig,

    "Ino_VideoConvert": InoVideoConvert,

    "CR_GetCaptcha": Cloudreve_Get_Captcha,
}


NODE_DISPLAY_NAME_MAPPINGS = {
    "Ino_SaveImage": "BeDrive Save Image",
    "Ino_SaveFile": "BeDrive Save File",
    "Ino_GetParentID": "BeDrive Get Parent ID",

    "Ino_ParseFilePath": "Ino Parse File Path",
    "Ino_NotBoolean": "Ino Not Boolean",
    "Ino_CountFiles": "Ino Count Files",
    "Ino_IntEqual": "Ino Int Equal",
    "Ino_BranchImage": "Ino Branch Image",
    "Ino_DateTimeAsString": "Ino DateTime As String",
    "Ino_RandomCharacterPrompt": "Ino Random Character Prompt",
    "Ino_CalculateLoraConfig": "Ino Calculate Lora Config",

    "Ino_VideoConvert": "Ino Video Convert",
    "CR_GetCaptcha": "CR Get Captcha",
}


WEB_DIRECTORY = "./web"
