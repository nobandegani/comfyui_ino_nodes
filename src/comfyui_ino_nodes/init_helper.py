import asyncio

from .workflow_helpers.download_model_helper import InoHuggingFaceDownloadModel, InoGetVideoModelDownloadConfig, InoGetClipDownloadConfig, InoGetVaeDownloadConfig, InoHandleDownloadModel

async def init_models():
    print("Init models started.")

    video_model_config_loader = InoGetVideoModelDownloadConfig()
    clip_model_config_loader = InoGetClipDownloadConfig()
    vae_model_config_loader = InoGetVaeDownloadConfig()

    handle_download_model = InoHandleDownloadModel()

    huggingface_downloader = InoHuggingFaceDownloadModel()

    """
    _, wan_animate_model_bf16, _ = await handle_download_model.function(
        enabled=True,
        config=video_model_config_loader.function(True, "comfy-wan-22-animate-14B-bf16"),
    )
    print(f"wan_animate_model_bf16: {wan_animate_model_bf16}")

    _, wan_22_clip_bf16, _ = await handle_download_model.function(
        enabled=True,
        config=clip_model_config_loader.function(True, "kj-umt5-bf16"),
    )
    print(f"wan_22_clip_bf16: {wan_22_clip_bf16}")

    _, wan_21_vae_bf16, _ = await handle_download_model.function(
        enabled=True,
        config=vae_model_config_loader.function(True, "kj-wan-21-bf16"),
    )
    print(f"wan_21_vae_bf16: {wan_21_vae_bf16}")

    _, wan_21_vae_bf16, _ = await handle_download_model.function(
        enabled=True,
        config=vae_model_config_loader.function(True, "kj-wan-21-bf16"),
    )
    print(f"wan_21_vae_bf16: {wan_21_vae_bf16}")
    """

    _, wan_animate_yolo, _ = await huggingface_downloader.function(
        enabled=True,
        model_config="{}",
        model_type="detection",
        model_subfolder="",
        repo_id="Wan-AI/Wan2.2-Animate-14B",
        filename="process_checkpoint/det/yolov10m.onnx",
    )
    print(f"wan_animate_yolo: {wan_animate_yolo}")

    _, wan_animate_vitpose_bin, _ = await huggingface_downloader.function(
        enabled=True,
        model_config="{}",
        model_type="detection",
        model_subfolder="",
        repo_id="Kijai/vitpose_comfy",
        filename="onnx/vitpose_h_wholebody_data.bin",
    )
    print(f"wan_animate_vitpose_bin: {wan_animate_vitpose_bin}")

    _, wan_animate_vitpose_onnx, _ = await huggingface_downloader.function(
        enabled=True,
        model_config="{}",
        model_type="detection",
        model_subfolder="",
        repo_id="Kijai/vitpose_comfy",
        filename="onnx/vitpose_h_wholebody_model.onnx",
    )
    print(f"wan_animate_vitpose_onnx: {wan_animate_vitpose_onnx}")

    print("Init models finished.")
