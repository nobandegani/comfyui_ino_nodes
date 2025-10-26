import os

from pathlib import Path
from huggingface_hub import hf_hub_download
from inopyutils import InoJsonHelper, InoHttpHelper

import folder_paths
import node_helpers


from ..s3_helper.s3_helper import S3Helper

MODEL_TYPES = (
    "checkpoints", "clip", "clip_vision", "controlnet", "diffusers", "diffusion_models",
    "loras", "sams", "text_encoders", "vae"
)

class InoValidateModel:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "s3_config": ("STRING", {}),
                "model_type": (MODEL_TYPES, {}),
                "model_name": ("STRING", {"default": "flux1dev/ae.safetensors"}),
            }
        }

    CATEGORY = "InoModelHelper"
    RETURN_TYPES = ("BOOLEAN", "STRING", )
    RETURN_NAMES = ("success", "msg", )
    FUNCTION = "function"

    async def function(self, enabled, s3_config, model_type, model_name):
        if not enabled:
            return (False, "", )

        parent_path = Path(folder_paths.get_input_directory()).parent
        model_path:Path = parent_path / "models" / model_type / model_name
        print(model_path)
        need_download = not model_path.is_file()
        if not need_download:
            return (True, "model validated", )

        s3_key = f"comfyui/models/{model_type}/{model_name}"

        validate_s3_config = S3Helper.validate_s3_config(s3_config)
        if not validate_s3_config["success"]:
            return (False, validate_s3_config["msg"],)

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return (False, validate_s3_key["msg"],)

        model_path.parent.mkdir(parents=True, exist_ok=True)

        s3_instance = S3Helper.get_instance(s3_config)
        s3_result = await s3_instance.download_file(
            s3_key=s3_key,
            local_file_path=model_path
        )

        return (s3_result["success"], s3_result["msg"], )

class InoHuggingFaceDownloadFile:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "dict_as_input": ("STRING", {"default": "{}"}),
                "model_type": (MODEL_TYPES, {}),
                "model_subfolder": ("STRING", {"default": "flux1dev"}),
                "repo_id": ("STRING", {"default": ""}),
                "filename": ("STRING", {"default": ""}),
                "subfolder": ("STRING", {"default": ""}),
            },
            "optional": {
                "token": ("STRING", {"default": ""}),
                "repo_type": ("STRING", {"default": ""}),
                "revision": ("STRING", {"default": ""})
            }
        }

    CATEGORY = "InoModelHelper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("success", "msg", "model_type", "abs_path", "rel_path")
    FUNCTION = "function"

    async def function(self, enabled, dict_as_input, model_type="", model_subfolder="", repo_id="", filename="", subfolder="", token="", repo_type="", revision=""):
        if not enabled:
            return (False, "", "", )

        if isinstance(dict_as_input, str):
            input_config = InoJsonHelper.string_to_dict(dict_as_input)
            if input_config["success"]:
                dict_as_input = input_config["data"]

        if isinstance(dict_as_input, dict):
            model_type = dict_as_input.get("model_type", model_type)
            model_subfolder = dict_as_input.get("model_subfolder", model_subfolder)
            repo_id = dict_as_input.get("repo_id", repo_id)
            filename = dict_as_input.get("filename", filename)
            subfolder = dict_as_input.get("subfolder", subfolder)
            repo_type = dict_as_input.get("repo_type", repo_type)
            revision = dict_as_input.get("revision", revision)


        parent_path = Path(folder_paths.get_input_directory()).parent
        model_path: Path = parent_path / "models" / model_type / model_subfolder
        if model_path.is_file():
            model_path = model_path.parent

        args = {}
        if subfolder:
            args["subfolder"] = subfolder
        if token:
            args["token"] = token
        if repo_type:
            args["repo_type"] = repo_type
        if revision:
            args["revision"] = revision

        args["local_dir"] = model_path

        try:
            result = hf_hub_download(repo_id, filename, **args)
            rel_path = Path(result).relative_to(model_path.parent)
            return (True, "Successfull", model_type, result, rel_path)
        except Exception as e:
            return (False, f"Error: {e}", "", )

class InoCivitaiDownloadFile:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "dict_as_input": ("STRING", {"default": "{}"}),
                "model_type": (MODEL_TYPES, {}),
                "model_subfolder": ("STRING", {"default": "flux1dev"}),
                "model_version": ("STRING", {"default": ""}),
            },
            "optional": {
                "token": ("STRING", {"default": ""}),
                "model_id": ("STRING", {"default": ""}),
            }
        }

    CATEGORY = "InoModelHelper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("success", "msg", "model_type", "abs_path", "rel_path")
    FUNCTION = "function"

    async def function(self, enabled, dict_as_input, model_type="", model_subfolder="", model_version="", token="", model_id=""):
        if not enabled:
            return (False, "", "", "", "", )

        if isinstance(dict_as_input, str):
            input_config = InoJsonHelper.string_to_dict(dict_as_input)
            if input_config["success"]:
                dict_as_input = input_config["data"]

        if isinstance(dict_as_input, dict):
            model_type = dict_as_input.get("model_type", model_type)
            model_subfolder = dict_as_input.get("model_subfolder", model_subfolder)
            model_version = dict_as_input.get("model_version", model_version)
            model_id = dict_as_input.get("model_id", model_id)

        parent_path = Path(folder_paths.get_input_directory()).parent
        model_path: Path = parent_path / "models" / model_type / model_subfolder
        if model_path.is_file():
            model_path = model_path.parent

        token = os.getenv("CIVITAI_TOKEN", token)

        headers = {
            "Authorization": f"Bearer {token}"
        }

        http_client = InoHttpHelper(
            timeout_total=None,
            timeout_sock_read=None,
            timeout_connect=30.0,
            timeout_sock_connect=30.0,
            retries=5,
            backoff_factor=1.0,
            default_headers=headers
        )

        if model_version:
            url = f"https://civitai.com/api/v1/model-versions/{model_version}"
        else:
            return (False, "model_version is required", "", "", "",)

        download_url = await http_client.get(
            url=url
        )
        if not download_url["success"]:
            return (False, download_url["msg"], "", "", "",)

        try:
            file_name = download_url["data"]["files"][0]["name"]
        except:
            return (False, "files is empty", "", "", "",)

        full_model_path = model_path / file_name

        if not download_url["data"]["downloadUrl"]:
            return (False, "downloadUrl is empty", "", "", "",)

        download_url = download_url["data"]["downloadUrl"]

        download_file = http_client.download(
            url=download_url,
            dest_path=model_path,
            chunk_size=8 * 1024 * 1024,
            resume=True,
            overwrite=False,
            allow_redirects=True,
            mkdirs=True,
            verify_size=True,
        )

        return (download_file["success"], download_file["msg"], model_type, download_url["data"], "", )


LOCAL_NODE_CLASS = {
    "InoValidateModel": InoValidateModel,
    "InoHuggingFaceDownloadFile": InoHuggingFaceDownloadFile,
    "InoCivitaiDownloadFile": InoCivitaiDownloadFile,
}
LOCAL_NODE_NAME = {
    "InoValidateModel": "Ino Validate Model",
    "InoHuggingFaceDownloadFile": "Ino Hugging Face Download File",
    "InoCivitaiDownloadFile": "Ino Civitai Download File",
}
