import torch
import hashlib
from inspect import cleandoc

from inocloudreve import CloudreveClient
from inopyutils import SparkHelper

_cloudreve_client = CloudreveClient()

class CloudreveInit:
    """
        Cloudreve Init
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "step": 1,
                    "label": "Seed (0 = random)"
                }),
                "server_address": ("STRING", {
                    "multiline": False,
                    "default": "https://cloudreve.com"
                })
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING")
    RETURN_NAMES = ("success", "message", "other")

    DESCRIPTION = cleandoc(__doc__)

    FUNCTION = "function"

    CATEGORY = "InoCloudreve"

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        m = hashlib.sha256()
        m.update(seed)
        return m.digest().hex()

    def function(self, enabled, seed, server_address):
        if not enabled:
            return "Disabled", "Node is disabled", ""

        try:
            _cloudreve_client.init(server_address)
            return "Success", "Cloudreve init success", ""
        except Exception as e:
            return "Failed", "Cloudreve init failed", str(e)


class CloudreveSignin:
    """
        Cloudreve Signin
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "step": 1,
                    "label": "Seed (0 = random)"
                }),
                "email": ("STRING", {
                    "multiline": False,
                    "default": "user"
                }),
                "password": ("STRING", {
                    "multiline": False,
                    "default": "*******"
                })
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING")
    RETURN_NAMES = ("success", "message", "other")

    DESCRIPTION = cleandoc(__doc__)

    FUNCTION = "function"

    CATEGORY = "InoCloudreve"

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        m = hashlib.sha256()
        m.update(seed)
        return m.digest().hex()

    async def function(self, enabled, seed, email, password):
        if not enabled:
            return "Disabled", "Node is disabled", ""

        try:
            res = await _cloudreve_client.password_sign_in(
                email=email,
                password=password
            )
            return res['success'], res['msg'], res
        except Exception as e:
            return "Failed", "Cloudreve signin failed", str(e)


class CloudreveUploadFile:
    """
        Cloudreve upload file
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "enabled": ("BOOLEAN", {"default": True, "label_off": "OFF", "label_on": "ON"}),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "step": 1,
                    "label": "Seed (0 = random)"
                }),
                "local_path": ("STRING", {
                    "multiline": False,
                    "default": "C:\Inoland\Arduino\Arduino IDE"
                }),
                "cloud_path": ("STRING", {
                    "multiline": False,
                    "default": "Ino/test"
                })
            }
        }

    RETURN_TYPES = ("BOOLEAN", "STRING", "STRING")
    RETURN_NAMES = ("success", "message", "other")

    DESCRIPTION = cleandoc(__doc__)

    FUNCTION = "function"

    CATEGORY = "InoCloudreve"

    @classmethod
    def IS_CHANGED(cls, seed, **kwargs):
        m = hashlib.sha256()
        m.update(seed)
        return m.digest().hex()

    async def function(self, enabled, seed, local_path, cloud_path):
        if not enabled:
            return "Disabled", "Node is disabled", ""

        try:
            res = await _cloudreve_client.upload_file(
                local_path=local_path,
                remote_path=cloud_path,
                storage_policy=SparkHelper.get_default_storage_policy()["id"]
            )
            return res['success'], res['msg'], res
        except Exception as e:
            return "Failed", "Cloudreve signin failed", str(e)
