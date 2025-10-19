"""Top-level package for comfyui_ino_nodes."""
from .src.comfyui_ino_nodes.s3_helper import LOCAL_NODE_CLASS as S3_CLASS, LOCAL_NODE_NAME as S3_NAME

from .src.comfyui_ino_nodes.utils.extra_nodes import LOCAL_NODE_CLASS as EXTRA_CLASS, LOCAL_NODE_NAME as EXTRA_NAME
from .src.comfyui_ino_nodes.utils.json_helper import LOCAL_NODE_CLASS as JSON_CLASS, LOCAL_NODE_NAME as JSON_NAME
from .src.comfyui_ino_nodes.utils.http_helper import LOCAL_NODE_CLASS as HTTP_CLASS, LOCAL_NODE_NAME as HTTP_NAME
from .src.comfyui_ino_nodes.utils.lora_helper import LOCAL_NODE_CLASS as LORA_CLASS, LOCAL_NODE_NAME as LORA_NAME
from .src.comfyui_ino_nodes.utils.prompt_helper import LOCAL_NODE_CLASS as PROMPT_CLASS, LOCAL_NODE_NAME as PROMPT_NAME
from .src.comfyui_ino_nodes.utils.sampler_helper import LOCAL_NODE_CLASS as SAMPLER_CLASS, LOCAL_NODE_NAME as SAMPLER_NAME
from .src.comfyui_ino_nodes.utils.file_helper import LOCAL_NODE_CLASS as FILE_CLASS, LOCAL_NODE_NAME as FILE_NAME
from .src.comfyui_ino_nodes.utils.openai_helper import LOCAL_NODE_CLASS as OPENAPI_CLASS, LOCAL_NODE_NAME as OPENAPI_NAME

_node_classes ={}
_node_classes.update(S3_CLASS)
_node_classes.update(EXTRA_CLASS)
_node_classes.update(JSON_CLASS)
_node_classes.update(HTTP_CLASS)
_node_classes.update(LORA_CLASS)
_node_classes.update(PROMPT_CLASS)
_node_classes.update(SAMPLER_CLASS)
_node_classes.update(FILE_CLASS)
_node_classes.update(OPENAPI_CLASS)

_node_names = {}
_node_names.update(S3_NAME)
_node_names.update(EXTRA_NAME)
_node_names.update(JSON_NAME)
_node_names.update(HTTP_NAME)
_node_names.update(LORA_NAME)
_node_names.update(PROMPT_NAME)
_node_names.update(SAMPLER_NAME)
_node_names.update(FILE_NAME)
_node_names.update(OPENAPI_NAME)

NODE_CLASS_MAPPINGS = _node_classes
NODE_DISPLAY_NAME_MAPPINGS = _node_names

WEB_DIRECTORY = "./web"

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]

__author__ = """InoNodes"""
__email__ = "contact@inoland.net"
__version__ = "1.1.5"
