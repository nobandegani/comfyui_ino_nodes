import io
import base64
import requests

import torch
import numpy as np
from PIL import Image

def rc_get_captcha(api_url: str = "http://your-cloudreve-domain/api/v3/captcha"):
    try:
        response = requests.get(api_url + "/site/captcha")
        response.raise_for_status()
        data = response.json()

        if data["code"] != 0 or "data" not in data:
            raise ValueError("Invalid response format or failed to get captcha")

        image_base64 = data["data"]["image"].split(",")[1]
        ticket = data["data"]["ticket"]

        image_bytes = base64.b64decode(image_base64)

        return image_bytes, ticket

    except Exception as e:
        print(f"[Captcha Error] {e}")
        dummy = torch.zeros((1, 3, 64, 64), dtype=torch.float32)
        return dummy, ""
