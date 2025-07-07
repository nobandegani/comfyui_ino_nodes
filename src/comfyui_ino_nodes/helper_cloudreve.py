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

        # 🛑 Make sure it's 3-channel RGB image
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")  # shape: [H, W, 3]

        # Convert to NumPy float32 in [0,1]
        np_image = np.array(image).astype(np.float32) / 255.0  # shape: [H, W, 3]

        # Convert to torch tensor: [1, 3, H, W]
        torch_image = torch.from_numpy(np_image).permute(2, 0, 1).unsqueeze(0)  # [1, 3, H, W]

        return torch_image, ticket

    except Exception as e:
        print(f"[Captcha Error] {e}")
        dummy = torch.zeros((1, 3, 64, 64), dtype=torch.float32)
        return dummy, ""
