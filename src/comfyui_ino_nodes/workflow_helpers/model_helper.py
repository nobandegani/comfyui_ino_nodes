import os

from pathlib import Path
from huggingface_hub import hf_hub_download
from inopyutils import InoJsonHelper, InoHttpHelper, InoFileHelper

import folder_paths
import node_helpers


from ..s3_helper.s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import ino_print_log, MODEL_TYPES


class InoCreateDownloadModelConfig:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "host": (["s3", "hf", "civitai"], {}),
                "model_type": (MODEL_TYPES, {}),
                "model_subfolder": ("STRING", {"default": "flux1dev", "tooltip": ""}),
                "repo_id": ("STRING", {"default": "", "tooltip": "depends on the host."}),
                "filename": ("STRING", {"default": "", "tooltip": "depends on the host."}),
                "subfolder": ("STRING", {"default": "", "tooltip": "depends on the host."}),
                "repo_type": ("STRING", {"default": "", "tooltip": "depends on the host."}),
                "revision": ("STRING", {"default": "", "tooltip": "depends on the host."}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("ModelConfig",)

    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    def function(self, enabled, host: str, model_type: str, model_subfolder: str, repo_id: str, filename: str,
                 subfolder: str, repo_type: str, revision: str):
        if not enabled:
            return ("",)

        config = {}
        config["host"] = host
        config["model_type"] = model_type
        config["model_subfolder"] = model_subfolder
        config["repo_id"] = repo_id
        config["filename"] = filename
        config["subfolder"] = subfolder
        config["repo_type"] = repo_type
        config["revision"] = revision

        config_str = InoJsonHelper.dict_to_string(config)["data"]

        return (config_str,)

class InoS3DownloadModel:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model_config": ("STRING", {"default": "{}"}),
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

    async def function(self, enabled, model_config, model_type="", model_subfolder="", s3_key="", s3_config="{}", bucket_name="default"):
        if not enabled:
            ino_print_log("InoS3DownloadModel", "Attempt to run but disabled")
            return (False, "", "", "", "",)

        try:
            if isinstance(model_config, str):
                input_config = InoJsonHelper.string_to_dict(model_config)
                if input_config["success"]:
                    model_config = input_config["data"]

            if isinstance(model_config, dict):
                model_type = model_config.get("model_type", model_type)
                model_subfolder = model_config.get("model_subfolder", model_subfolder)
                s3_config = model_config.get("repo_id", s3_config)
                s3_key = model_config.get("filename", s3_key)
                bucket_name = model_config.get("subfolder", bucket_name)

            parent_path = Path(folder_paths.get_input_directory()).parent
            model_path_base: Path = parent_path / "models" / model_type
            model_path:Path = model_path_base / model_subfolder / Path(s3_key).name
            rel_path = Path(model_path).relative_to(model_path_base)

            need_download = not model_path.is_file()
            if not need_download:
                ino_print_log("InoS3DownloadModel", "model already downloaded", )
                return (True, "model validated", model_type, model_path, rel_path,)

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

            ino_print_log("InoS3DownloadModel", "file downloaded successfully", )
            return (s3_result["success"], s3_result["msg"], model_type, model_path, rel_path, )
        except Exception as e:
            ino_print_log("InoS3DownloadModel", "", e)
            return (False, f"Error: {e}", "", "", "",)

class InoHuggingFaceDownloadModel:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model_config": ("STRING", {"default": "{}"}),
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

    async def function(self, enabled, model_config, model_type="", model_subfolder="", repo_id="", filename="", subfolder="", token="", repo_type="", revision=""):
        if not enabled:
            ino_print_log("InoHuggingFaceDownloadFile", "Attempt to run but disabled")
            return (False, "", "", "", "",)

        try:
            if isinstance(model_config, str):
                input_config = InoJsonHelper.string_to_dict(model_config)
                if input_config["success"]:
                    model_config = input_config["data"]

            if isinstance(model_config, dict):
                model_type = model_config.get("model_type", model_type)
                model_subfolder = model_config.get("model_subfolder", model_subfolder)
                repo_id = model_config.get("repo_id", repo_id)
                filename = model_config.get("filename", filename)
                subfolder = model_config.get("subfolder", subfolder)
                repo_type = model_config.get("repo_type", repo_type)
                revision = model_config.get("revision", revision)


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
                "model_config": ("STRING", {"default": "{}"}),
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

    async def function(self, enabled, model_config, model_type="", model_subfolder="", model_version="", token="", model_id="", file_id=0, chunk_size=8):
        if not enabled:
            ino_print_log("InoCivitaiDownloadFile", "Attempt to run but disabled")
            return (False, "", "", "", "", )

        try:
            if isinstance(model_config, str):
                input_config = InoJsonHelper.string_to_dict(model_config)
                if input_config["success"]:
                    model_config = input_config["data"]

            if isinstance(model_config, dict):
                model_type = model_config.get("model_type", model_type)
                model_subfolder = model_config.get("model_subfolder", model_subfolder)
                model_version = model_config.get("revision", model_version)
                model_id = model_config.get("repo_id", model_id)
                file_id = int(model_config.get("filename", file_id))

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
                return (False, "failed to get file name or sha", "", "", "",)

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

class InoHandleDownloadModel:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "config": ("STRING", {"default": "{}"}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("success", "msg", "model_type", "abs_path", "rel_path")

    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    async def function(self, enabled, config: str):
        if not enabled:
            return (False, "not enabled", "", "", "")

        config_dict = InoJsonHelper.string_to_dict(config)
        if not config_dict["success"]:
            return (False, config_dict["msg"], "", "", "")

        config_dict = config_dict["data"]

        loader = None
        if config_dict["host"] == "s3":
            loader = InoS3DownloadModel()
        elif config_dict["host"] == "hf":
            loader = InoHuggingFaceDownloadModel()
        elif config_dict["host"] == "civitai":
            loader = InoCivitaiDownloadModel()
        else:
            return (False, "unknown host", "", "", "")

        return await loader.function(enabled=True, model_config=config)

LOCAL_NODE_CLASS = {
    "InoCreateModelFileConfig": InoCreateDownloadModelConfig,
    "InoS3DownloadModel": InoS3DownloadModel,
    "InoHuggingFaceDownloadModel": InoHuggingFaceDownloadModel,
    "InoCivitaiDownloadModel": InoCivitaiDownloadModel,
    "InoHandleDownloadModel": InoHandleDownloadModel,
}
LOCAL_NODE_NAME = {
    "InoCreateModelFileConfig": "Ino Create Model File Config",
    "InoS3DownloadModel": "Ino S3 Download Model",
    "InoHuggingFaceDownloadModel": "Ino Hugging Face Download Model",
    "InoCivitaiDownloadModel": "Ino Civitai Download Model",
    "InoHandleDownloadModel": "Ino Handle Download Model",
}
