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


NODE_CLASS_MAPPINGS = {
    "Ino_SaveImage": BeDriveSaveImage,
    "Ino_SaveFile": BeDriveSaveFile,
    "Ino_GetParentID": BeDriveGetParentID,

    "Ino_ParseFilePath": InoParseFilePath,
    "Ino_NotBoolean": InoNotBoolean,
    "Ino_CountFiles": InoCountFiles,
}


NODE_DISPLAY_NAME_MAPPINGS = {
    "Ino_SaveImage": "BeDrive Save Image",
    "Ino_SaveFile": "BeDrive Save File",
    "Ino_GetParentID": "BeDrive Get Parent ID",

    "Ino_ParseFilePath": "Ino Parse File Path",
    "Ino_NotBoolean": "Ino Not Boolean",
    "Ino_CountFiles": "Ino Count Files",
}


WEB_DIRECTORY = "./web"
