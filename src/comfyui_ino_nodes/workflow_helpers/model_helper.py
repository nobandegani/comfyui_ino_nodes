import os

from pathlib import Path
from huggingface_hub import hf_hub_download
from inopyutils import InoJsonHelper, InoHttpHelper, InoFileHelper

import folder_paths
import node_helpers


from ..s3_helper.s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import ino_print_log

MODEL_TYPES = (
    "checkpoints", "clip", "clip_vision", "controlnet", "diffusers", "diffusion_models",
    "loras", "sams", "text_encoders", "vae"
)

class InoS3DownloadModel:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model_type": (MODEL_TYPES, {}),
                "model_subfolder": ("STRING", {"default": "flux1dev"}),
                "s3_key": ("STRING", {"default": "uploads/lora/aly_v001.safetensors"}),
            },
            "optional": {
                "s3_config": ("STRING", {"default": S3_EMPTY_CONFIG_STRING, "tooltip": "you can leave it empty and pass it with env vars"}),
                "bucket_name": ("STRING", {"default": "default"}),
            }
        }

    CATEGORY = "InoModelHelper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("success", "msg", "model_type", "abs_path", "rel_path")
    FUNCTION = "function"

    async def function(self, enabled, model_type, model_subfolder, s3_key, s3_config, bucket_name):
        if not enabled:
            ino_print_log("InoS3DownloadModel", "Attempt to run but disabled")
            return (False, "", "", "", "",)

        parent_path = Path(folder_paths.get_input_directory()).parent
        model_path_base: Path = parent_path / "models" / model_type
        model_path:Path = model_path_base / model_subfolder / Path(s3_key).name

        need_download = not model_path.is_file()
        if not need_download:
            ino_print_log("InoS3DownloadModel", "model already downloaded", )
            return (True, "model validated", "", "", "",)

        validate_s3_config = S3Helper.validate_s3_config(s3_config)
        if not validate_s3_config["success"]:
            ino_print_log("InoS3DownloadModel", validate_s3_config["msg"], )
            return (False, validate_s3_config["msg"], "", "", "",)
        s3_config = validate_s3_config["config"]
        
        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            ino_print_log("InoS3DownloadModel", validate_s3_key["msg"], )
            return (False, validate_s3_key["msg"], "", "", "",)

        model_path.parent.mkdir(parents=True, exist_ok=True)

        s3_instance = S3Helper.get_instance(s3_config)
        s3_result = await s3_instance.download_file(
            s3_key=s3_key,
            local_file_path=model_path
        )

        rel_path = Path(model_path).relative_to(model_path_base)

        ino_print_log("InoS3DownloadModel", "file downloaded successfully", )
        return (s3_result["success"], s3_result["msg"], model_type, model_path, rel_path, )

class InoHuggingFaceDownloadModel:
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
        try:
            if not enabled:
                ino_print_log("InoHuggingFaceDownloadFile", "Attempt to run but disabled")
                return (False, "", "", "", "",)

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
            model_path_base: Path = parent_path / "models" / model_type
            model_path: Path = model_path_base / model_subfolder
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
        except Exception as e:
            ino_print_log("InoHuggingFaceDownloadFile", "", e)
            return (False, f"Error: {e}", "",)

        try:
            result = hf_hub_download(repo_id, filename, **args)
            rel_path = Path(result).relative_to(model_path_base)
            ino_print_log("InoHuggingFaceDownloadFile", "file downloaded successfully", )
            return (True, "Successfull", model_type, result, rel_path)
        except Exception as e:
            ino_print_log("InoHuggingFaceDownloadFile", "", e)
            return (False, f"Error: {e}", "", )

class InoCivitaiDownloadModel:
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
                "file_id": ("INT", {"min": 0, "max": 100, "step": 1, "default": 0}),
                "chunk_size": ([8, 16, 32, 64], {"default": 8})
            }
        }

    CATEGORY = "InoModelHelper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("success", "msg", "model_type", "abs_path", "rel_path")
    FUNCTION = "function"

    async def function(self, enabled, dict_as_input, model_type="", model_subfolder="", model_version="", token="", model_id="", file_id=0, chunk_size=8):
        if not enabled:
            ino_print_log("InoCivitaiDownloadFile", "Attempt to run but disabled")
            return (False, "", "", "", "", )

        try:
            if isinstance(dict_as_input, str):
                input_config = InoJsonHelper.string_to_dict(dict_as_input)
                if input_config["success"]:
                    dict_as_input = input_config["data"]

            if isinstance(dict_as_input, dict):
                model_type = dict_as_input.get("model_type", model_type)
                model_subfolder = dict_as_input.get("model_subfolder", model_subfolder)
                model_version = dict_as_input.get("revision", model_version)
                model_id = dict_as_input.get("repo_id", model_id)
                file_id = dict_as_input.get("filename", file_id)

            parent_path = Path(folder_paths.get_input_directory()).parent
            model_path_base: Path = parent_path / "models" / model_type
            model_path = model_path_base / model_subfolder
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
                await http_client.close()
                ino_print_log("InoCivitaiDownloadFile", "model_version is required, using model_id not implemented yet")
                return (False, "model_version is required, using model_id not implemented yet", "", "", "",)

            download_url = await http_client.get(
                url=url
            )
            if not download_url["success"]:
                await http_client.close()
                ino_print_log("InoCivitaiDownloadFile", "failed to get download url", download_url["msg"])
                return (False, download_url["msg"], "", "", "",)

            try:
                file_name = download_url["data"]["files"][file_id]["name"]
                file_sha = download_url["data"]["files"][file_id]["hashes"]["SHA256"]
            except Exception as e:
                await http_client.close()
                ino_print_log("InoCivitaiDownloadFile", "failed to get file name or sha", e)
                return (False, "files is empty", "", "", "",)

            full_model_path = model_path / file_name

            if full_model_path.is_file():
                sha_res = await InoFileHelper.get_file_hash_sha_256(full_model_path)
                if sha_res["success"] and sha_res["sha"].lower() == file_sha.lower():
                    rel_path = full_model_path.relative_to(model_path.parent)
                    await http_client.close()
                    ino_print_log("InoCivitaiDownloadFile", "File already downloaded and valid", )
                    return (True, "File is valid", model_type, full_model_path, rel_path, )
                else:
                    full_model_path.unlink()

            if not download_url["data"]["downloadUrl"]:
                await http_client.close()
                ino_print_log("InoCivitaiDownloadFile", "downloadUrl is empty", )
                return (False, "downloadUrl is empty", "", "", "",)

            download_url = download_url["data"]["files"][file_id]["downloadUrl"]

            download_file = await http_client.download(
                url=download_url,
                dest_path=model_path,
                chunk_size=chunk_size * 1024 * 1024,
                resume=True,
                overwrite=False,
                allow_redirects=True,
                mkdirs=True,
                verify_size=True,
            )

            if not download_file["success"] and download_file["success"] != "OK":
                await http_client.close()
                ino_print_log("InoCivitaiDownloadFile", "failed to download file", download_file["msg"])
                return (download_file["success"], download_file["msg"], "", "", "",)

            rel_path = Path(download_file["path"]).relative_to(model_path_base)

            await http_client.close()
            ino_print_log("InoCivitaiDownloadFile", "File downloaded successfully", )
            return (download_file["success"], "File is downloaded", model_type, download_file["path"], rel_path, )
        except Exception as e:
            ino_print_log("InoCivitaiDownloadFile", "", e)
            return (False, e, "", "", "",)

LOCAL_NODE_CLASS = {
    "InoS3DownloadModel": InoS3DownloadModel,
    "InoHuggingFaceDownloadModel": InoHuggingFaceDownloadModel,
    "InoCivitaiDownloadModel": InoCivitaiDownloadModel,
}
LOCAL_NODE_NAME = {
    "InoS3DownloadModel": "Ino S3 Download Model",
    "InoHuggingFaceDownloadModel": "Ino Hugging Face Download Model",
    "InoCivitaiDownloadModel": "Ino Civitai Download Model",
}
