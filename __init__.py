"""Top-level package for comfyui_ino_nodes."""


#--------------------------------- Class helpers ---------------------------------
from .src.comfyui_ino_nodes.class_helpers.file_helper import (
    LOCAL_NODE_CLASS as FILE_HELPER_CLASS,
    LOCAL_NODE_NAME as FILE_HELPER_NAME
)
from .src.comfyui_ino_nodes.class_helpers.http_helper import (
    LOCAL_NODE_CLASS as HTTP_HELPER_CLASS,
    LOCAL_NODE_NAME as HTTP_HELPER_NAME
)
from .src.comfyui_ino_nodes.class_helpers.json_helper import (
    LOCAL_NODE_CLASS as JSON_HELPER_CLASS,
    LOCAL_NODE_NAME as JSON_HELPER_NAME
)
from .src.comfyui_ino_nodes.class_helpers.openai_helper import (
    LOCAL_NODE_CLASS as OPENAPI_HELPER_CLASS,
    LOCAL_NODE_NAME as OPENAPI_HELPER_NAME
)

#--------------------------------- Node helpers ---------------------------------
from .src.comfyui_ino_nodes.node_helpers.bool_helper import (
    LOCAL_NODE_CLASS as BOOL_HELPER_CLASS,
    LOCAL_NODE_NAME as BOOL_HELPER_NAME
)
from .src.comfyui_ino_nodes.node_helpers.float_helper import (
    LOCAL_NODE_CLASS as FLOAT_HELPER_CLASS,
    LOCAL_NODE_NAME as FLOAT_HELPER_NAME
)
from .src.comfyui_ino_nodes.node_helpers.image_helper import (
    LOCAL_NODE_CLASS as IMAGE_HELPER_CLASS,
    LOCAL_NODE_NAME as IMAGE_HELPER_NAME
)
from .src.comfyui_ino_nodes.node_helpers.int_helper import (
    LOCAL_NODE_CLASS as INT_HELPER_CLASS,
    LOCAL_NODE_NAME as INT_HELPER_NAME
)
from .src.comfyui_ino_nodes.node_helpers.string_helper import (
    LOCAL_NODE_CLASS as STRING_HELPER_CLASS,
    LOCAL_NODE_NAME as STRING_HELPER_NAME
)
from .src.comfyui_ino_nodes.node_helpers.time_helper import (
    LOCAL_NODE_CLASS as TIME_HELPER_CLASS,
    LOCAL_NODE_NAME as TIME_HELPER_NAME
)
from .src.comfyui_ino_nodes.node_helpers.cast_helper import (
    LOCAL_NODE_CLASS as CAST_HELPER_CLASS,
    LOCAL_NODE_NAME as CAST_HELPER_NAME
)

#--------------------------------- S3 helper ---------------------------------
from .src.comfyui_ino_nodes.s3_helper import (
    LOCAL_NODE_CLASS as S3_HELPER_CLASS,
    LOCAL_NODE_NAME as S3_HELPER_NAME
)

#--------------------------------- Extra nodes ---------------------------------
from .src.comfyui_ino_nodes.utils.extra_nodes import (
    LOCAL_NODE_CLASS as EXTRA_CLASS,
    LOCAL_NODE_NAME as EXTRA_NAME
)

#--------------------------------- Workflow helpers ---------------------------------
from .src.comfyui_ino_nodes.workflow_helpers.lora_helper import (
    LOCAL_NODE_CLASS as LORA_HELPER_CLASS,
    LOCAL_NODE_NAME as LORA_HELPER_NAME
)
from .src.comfyui_ino_nodes.workflow_helpers.model_helper import (
    LOCAL_NODE_CLASS as MODEL_HELPER_CLASS,
    LOCAL_NODE_NAME as MODEL_HELPER_NAME
)
from .src.comfyui_ino_nodes.workflow_helpers.prompt_helper import (
    LOCAL_NODE_CLASS as PROMPT_HELPER_CLASS,
    LOCAL_NODE_NAME as PROMPT_HELPER_NAME
)
from .src.comfyui_ino_nodes.workflow_helpers.sampler_helper import (
    LOCAL_NODE_CLASS as SAMPLER_HELPER_CLASS,
    LOCAL_NODE_NAME as SAMPLER_HELPER_NAME
)

from .src.comfyui_ino_nodes.basic_auth import LOCAL_NODE_CLASS as BASIC_AUTH_CLASS, LOCAL_NODE_NAME as BASIC_AUTH_NAME

_node_classes ={}
_node_classes.update(FILE_HELPER_CLASS)
_node_classes.update(HTTP_HELPER_CLASS)
_node_classes.update(JSON_HELPER_CLASS)
_node_classes.update(OPENAPI_HELPER_CLASS)

_node_classes.update(BOOL_HELPER_CLASS)
_node_classes.update(FLOAT_HELPER_CLASS)
_node_classes.update(IMAGE_HELPER_CLASS)
_node_classes.update(INT_HELPER_CLASS)
_node_classes.update(STRING_HELPER_CLASS)
_node_classes.update(TIME_HELPER_CLASS)
_node_classes.update(CAST_HELPER_CLASS)

_node_classes.update(S3_HELPER_CLASS)

_node_classes.update(EXTRA_CLASS)

_node_classes.update(LORA_HELPER_CLASS)
_node_classes.update(MODEL_HELPER_CLASS)
_node_classes.update(PROMPT_HELPER_CLASS)
_node_classes.update(SAMPLER_HELPER_CLASS)



_node_names = {}
_node_names.update(FILE_HELPER_NAME)
_node_names.update(HTTP_HELPER_NAME)
_node_names.update(JSON_HELPER_NAME)
_node_names.update(OPENAPI_HELPER_NAME)

_node_names.update(BOOL_HELPER_NAME)
_node_names.update(FLOAT_HELPER_NAME)
_node_names.update(IMAGE_HELPER_NAME)
_node_names.update(INT_HELPER_NAME)
_node_names.update(STRING_HELPER_NAME)
_node_names.update(TIME_HELPER_NAME)
_node_names.update(CAST_HELPER_NAME)

_node_names.update(S3_HELPER_NAME)

_node_names.update(EXTRA_NAME)

_node_names.update(LORA_HELPER_NAME)
_node_names.update(MODEL_HELPER_NAME)
_node_names.update(PROMPT_HELPER_NAME)
_node_names.update(SAMPLER_HELPER_NAME)

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
