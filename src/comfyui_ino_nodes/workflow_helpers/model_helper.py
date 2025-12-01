import os
import shutil

from pathlib import Path
from huggingface_hub import hf_hub_download, snapshot_download
from inopyutils import InoJsonHelper, InoHttpHelper, InoFileHelper, ino_ok, ino_err, ino_is_err

import folder_paths
import node_helpers

from ..s3_helper.s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import ino_print_log, MODEL_TYPES, any_type, UNET_WEIGHT_DTYPE, CLIP_TYPE
from ..node_helper import get_list_from_csv, get_model_from_csv

#todo add progress bar

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
            ino_print_log("InoCreateDownloadModelConfig", "Attempt to run but disabled")
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

        ino_print_log("InoCreateDownloadModelConfig", "config created")
        return (config_str,)

class InoGetImageModelDownloadConfig:
    """

    """
    MODELS_LIST = get_list_from_csv(False, "image_models_files", True)

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model": (s.MODELS_LIST, {}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("ModelConfig",)

    FUNCTION = "function"

    CATEGORY = "InoModelHelper"

    def function(self, enabled, model):
        if not enabled:
            return ("",)

        model_dict = get_model_from_csv(False, "image_models_files", model)

        data = InoJsonHelper.dict_to_string(model_dict)["data"]
        return (data,)

class InoGetVideoModelDownloadConfig:
    """

    """
    MODELS_LIST = get_list_from_csv(False, "video_models_files", True)

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model": (s.MODELS_LIST, {}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("ModelConfig",)

    FUNCTION = "function"

    CATEGORY = "InoModelHelper"

    def function(self, enabled, model):
        if not enabled:
            return ("",)

        model_dict = get_model_from_csv(False, "video_models_files", model)

        data = InoJsonHelper.dict_to_string(model_dict)["data"]
        return (data,)

class InoGetVaeDownloadConfig:
    """

    """
    MODELS_LIST = get_list_from_csv(False, "vae_files", True)

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model": (s.MODELS_LIST, {}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("ModelConfig",)

    FUNCTION = "function"

    CATEGORY = "InoModelHelper"

    def function(self, enabled, model):
        if not enabled:
            return ("",)

        model_dict = get_model_from_csv(False, "vae_files", model)

        data = InoJsonHelper.dict_to_string(model_dict)["data"]
        return (data,)

class InoGetClipDownloadConfig:
    """

    """
    MODELS_LIST = get_list_from_csv(False, "clip_files", True)

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model": (s.MODELS_LIST, {}),
            },
            "optional": {
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("ModelConfig",)

    FUNCTION = "function"

    CATEGORY = "InoModelHelper"

    def function(self, enabled, model):
        if not enabled:
            return ("",)

        model_dict = get_model_from_csv(False, "clip_files", model)

        data = InoJsonHelper.dict_to_string(model_dict)["data"]
        return (data,)

class InoHttpDownloadModel:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model_config": ("STRING", {"default": "{}"}),
                "model_type": (MODEL_TYPES, {}),
                "model_subfolder": ("STRING", {"default": "flux1dev"}),
                "url": ("STRING", {"default": "https://download.pl"}),
            },
            "optional": {
            }
        }

    CATEGORY = "InoModelHelper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("success", "msg", "model_type", "abs_path", "rel_path")
    FUNCTION = "function"

    async def function(self, enabled, model_config, model_type="", model_subfolder="", url=""):
        if not enabled:
            ino_print_log("InoHttpDownloadModel", "Attempt to run but disabled")
            return (False, "", "", "", "",)

        try:
            if isinstance(model_config, str):
                input_config = InoJsonHelper.string_to_dict(model_config)
                if input_config["success"]:
                    model_config = input_config["data"]

            if isinstance(model_config, dict):
                model_type = model_config.get("model_type", model_type)
                model_subfolder = model_config.get("model_subfolder", model_subfolder)
                url = model_config.get("filename", url)

            parent_path = Path(folder_paths.get_input_directory()).parent
            model_path_base: Path = parent_path / "models" / model_type
            model_path:Path = model_path_base / model_subfolder / Path(url).name
            rel_path = Path(model_path).relative_to(model_path_base)

            need_download = not model_path.is_file()
            if not need_download:
                ino_print_log("InoHttpDownloadModel", "model already downloaded", )
                return (True, "model validated", model_type, model_path, rel_path,)

            model_path.parent.mkdir(parents=True, exist_ok=True)

            http_instance = InoHttpHelper()

            http_result = await http_instance.download(
                url=url,
                dest_path=model_path,
            )
            if ino_is_err(http_result):
                return (False, "failed to download", model_type, model_path, rel_path,)

            ino_print_log("InoHttpDownloadModel", "file downloaded successfully", )
            return (http_result["success"], http_result["msg"], model_type, model_path, rel_path, )
        except Exception as e:
            ino_print_log("InoHttpDownloadModel", "", e)
            return (False, f"Error: {e}", "", "", "",)

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

            validate_s3_key = S3Helper.validate_s3_key(s3_key)
            if not validate_s3_key["success"]:
                ino_print_log("InoS3DownloadModel", validate_s3_key["msg"], )
                return (False, validate_s3_key["msg"], "", "", "",)

            model_path.parent.mkdir(parents=True, exist_ok=True)

            s3_instance = S3Helper.get_instance(s3_config)
            if ino_is_err(s3_instance):
                return (False, s3_instance["msg"], "", "", "",)
            s3_instance = s3_instance["instance"]

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
                "revision": ("STRING", {"default": ""}),
                "ignore_repo_dir": ("BOOLEAN", {"default": False}),
            }
        }

    CATEGORY = "InoModelHelper"
    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("success", "msg", "model_type", "abs_path", "rel_path")
    FUNCTION = "function"

    async def function(self, enabled, model_config, model_type="", model_subfolder="", repo_id="", filename="", subfolder="", token="", repo_type="", revision="", ignore_repo_dir=False):
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
            if ignore_repo_dir:
                shutil.move(result, model_path)
                result = f"{model_path}/{Path(result).name}"
            rel_path = Path(result).relative_to(model_path_base)
            ino_print_log("InoHuggingFaceDownloadFile", "file downloaded successfully", )
            return (True, "Successfull", model_type, result, rel_path)
        except Exception as e:
            ino_print_log("InoHuggingFaceDownloadFile", "", e)
            return (False, f"Error: {e}", "", )

class InoHuggingFaceDownloadRepo:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model_config": ("STRING", {"default": "{}"}),
                "model_type": (MODEL_TYPES, {}),
                "model_subfolder": ("STRING", {"default": "flux1dev"}),
                "repo_id": ("STRING", {"default": ""}),
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

    async def function(self, enabled, model_config, model_type="", model_subfolder="", repo_id="", token="", repo_type="", revision=""):
        if not enabled:
            ino_print_log("InoHuggingFaceDownloadRepo", "Attempt to run but disabled")
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
                repo_type = model_config.get("repo_type", repo_type)
                revision = model_config.get("revision", revision)


            parent_path = Path(folder_paths.get_input_directory()).parent
            model_path_base: Path = parent_path / "models" / model_type
            model_path: Path = model_path_base / model_subfolder
            if model_path.is_file():
                model_path = model_path.parent

            args = {}
            if token:
                args["token"] = token
            if repo_type:
                args["repo_type"] = repo_type
            if revision:
                args["revision"] = revision

            args["local_dir"] = model_path
        except Exception as e:
            ino_print_log("InoHuggingFaceDownloadRepo", "", e)
            return (False, f"Error: {e}", "",)

        try:
            result = snapshot_download(repo_id, **args)
            rel_path = Path(result).relative_to(model_path_base)
            ino_print_log("InoHuggingFaceDownloadRepo", "file downloaded successfully", )
            return (True, "Successfull", model_type, result, rel_path)
        except Exception as e:
            ino_print_log("InoHuggingFaceDownloadRepo", "", e)
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
                    rel_path = full_model_path.relative_to(model_path_base)
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
            ino_print_log("InoHandleDownloadModel", "Attempt to run but disabled")
            return (False, "not enabled", "", "", "")

        config_dict = InoJsonHelper.string_to_dict(config)
        if not config_dict["success"]:
            ino_print_log("InoHandleDownloadModel", "invalid config string")
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
            ino_print_log("InoHandleDownloadModel", "unknown host")
            return (False, "unknown host", "", "", "")

        result = await loader.function(enabled=True, model_config=config)
        ino_print_log("InoHandleDownloadModel", "delegated to loader completed")
        return result

class InoHandleLoadModel:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "model_type": (MODEL_TYPES, {}),
                "model_path": ("STRING", {"default": ""}),
            },
            "optional": {
                "unet_weight_dtype": (UNET_WEIGHT_DTYPE, {}),
                "clip_type": (CLIP_TYPE, {})
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", any_type, )
    RETURN_NAMES = ("Success", "MSG", "Model",)

    FUNCTION = "function"
    CATEGORY = "InoSamplerHelper"

    async def function(self, enabled, model_type:str, model_path: str, unet_weight_dtype, clip_type):
        if not enabled:
            ino_print_log("InoHandleLoadModel", "Attempt to run but disabled")
            return (False, "not enabled", None,)

        try:
            loaded_model = None
            supported = True
            if model_type == "controlnet":
                from nodes import ControlNetLoader

                model_loader = ControlNetLoader()
                file_loader = model_loader.load_controlnet(
                    control_net_name=model_path
                )
                loaded_model = file_loader[0]
            elif model_type == "diffusion_models":
                from nodes import UNETLoader

                model_loader = UNETLoader()
                file_loader = model_loader.load_unet(
                    unet_name=model_path,
                    weight_dtype=unet_weight_dtype
                )
                loaded_model = file_loader[0]
            elif model_type == "text_encoders":
                from nodes import CLIPLoader
                model_loader = CLIPLoader()

                file_loader = model_loader.load_clip(
                    clip_name=model_path,
                    type=clip_type,
                    device="default"
                )
                loaded_model = file_loader[0]
            elif model_type == "vae":
                from nodes import VAELoader
                model_loader = VAELoader()

                file_loader = model_loader.load_vae(
                    vae_name=model_path,
                )
                loaded_model = file_loader[0]
            else:
                supported = False

            if not supported:
                ino_print_log("InoHandleLoadModel", f"loading {model_type} not supported")
                return (False, f"loading {model_type} models not supported yet", None, )

            if loaded_model is not None:
                ino_print_log("InoHandleLoadModel", f"{model_type} loaded")
                return (True, f"{model_type} loaded", loaded_model,  )
            else:
                ino_print_log("InoHandleLoadModel", f"{model_type} not loaded")
                return (False, f"{model_type} not loaded", None,  )
        except Exception as e:
            ino_print_log("InoHandleLoadModel", "exception", e)
            return (False, f"Error: {e}", None, )

class InoHandleDownloadAndLoadModel:
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

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING", "STRING", "STRING", any_type,)
    RETURN_NAMES = ("success", "msg", "model_type", "abs_path", "rel_path", "loaded_model",)

    FUNCTION = "function"

    CATEGORY = "InoSamplerHelper"

    async def function(self, enabled, config: str):
        if not enabled:
            ino_print_log("InoHandleDownloadAndLoadModel", "Attempt to run but disabled")
            return (False, "not enabled", "", "", "", None,)

        download_handler = InoHandleDownloadModel()
        download_result = await download_handler.function(enabled=True, config=config)

        if not download_result[0]:
            ino_print_log("InoHandleDownloadAndLoadModel", "download failed", download_result[1])
            return (False, download_result[1], "", "", "", None,)

        model_type = download_result[2]
        abs_path = download_result[3]
        rel_path = download_result[4]

        model_load_handler = InoHandleLoadModel()
        model_loader = await model_load_handler.function(enabled=True, model_type=model_type, model_path=rel_path)
        if not model_loader[0]:
            ino_print_log("InoHandleDownloadAndLoadModel", "load failed", model_loader[1])
            return (False, model_loader[1], model_type, abs_path, rel_path, None, )

        ino_print_log("InoHandleDownloadAndLoadModel", f"{model_type} downloaded and loaded")
        return (True, f"{model_type} loaded", model_type, abs_path, rel_path, model_loader[2])

class InoGetModelPathAsString:
    """

    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model_type": (MODEL_TYPES, {}),
            }
        }

    RETURN_TYPES = ("STRING", )
    RETURN_NAMES = ("string", )

    FUNCTION = "function"

    CATEGORY = "InoNodes"

    def function(self, model_type,):
        model_path = Path(folder_paths.get_input_directory()).parent / "models" / model_type
        return (str(model_path.resolve()), )

LOCAL_NODE_CLASS = {
    "InoCreateModelFileConfig": InoCreateDownloadModelConfig,
    "InoGetImageModelDownloadConfig": InoGetImageModelDownloadConfig,
    "InoGetVideoModelDownloadConfig": InoGetVideoModelDownloadConfig,
    "InoGetVaeDownloadConfig": InoGetVaeDownloadConfig,
    "InoGetClipDownloadConfig": InoGetClipDownloadConfig,

    "InoHttpDownloadModel": InoHttpDownloadModel,
    "InoS3DownloadModel": InoS3DownloadModel,
    "InoHuggingFaceDownloadModel": InoHuggingFaceDownloadModel,
    "InoHuggingFaceDownloadRepo": InoHuggingFaceDownloadRepo,
    "InoCivitaiDownloadModel": InoCivitaiDownloadModel,

    "InoHandleDownloadModel": InoHandleDownloadModel,
    "InoHandleLoadModel": InoHandleLoadModel,
    "InoHandleDownloadAndLoadModel": InoHandleDownloadAndLoadModel,
    "InoGetModelPathAsString": InoGetModelPathAsString
}
LOCAL_NODE_NAME = {
    "InoCreateModelFileConfig": "Ino Create Model File Config",
    "InoGetImageModelDownloadConfig": "Ino Get Image Model Download Config",
    "InoGetVideoModelDownloadConfig": "Ino Get Video Model Download Config",
    "InoGetVaeDownloadConfig": "Ino Get Vae Download Config",
    "InoGetClipDownloadConfig": "Ino Get Clip Download Config",

    "InoHttpDownloadModel": "Ino Http Download Model",
    "InoS3DownloadModel": "Ino S3 Download Model",
    "InoHuggingFaceDownloadModel": "Ino Hugging Face Download Model",
    "InoHuggingFaceDownloadRepo": "Ino Hugging Face Download Repo",
    "InoCivitaiDownloadModel": "Ino Civitai Download Model",

    "InoHandleDownloadModel": "Ino Handle Download Model",
    "InoHandleLoadModel": "Ino Handle Load Model",
    "InoHandleDownloadAndLoadModel": "Ino Handle Download And Load Model",

    "InoGetModelPathAsString": "Ino Get Model Path As String"
}
