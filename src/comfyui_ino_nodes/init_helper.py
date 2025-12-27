import asyncio

from .workflow_helpers.download_model_helper import InoHuggingFaceDownloadModel, InoGetVideoModelDownloadConfig, InoGetClipDownloadConfig, InoGetVaeDownloadConfig, InoHandleDownloadModel

async def init_models():
    print("Init models started.")

    video_model_config_loader = InoGetVideoModelDownloadConfig()
    clip_model_config_loader = InoGetClipDownloadConfig()
    vae_model_config_loader = InoGetVaeDownloadConfig()

    handle_download_model = InoHandleDownloadModel()

    huggingface_downloader = InoHuggingFaceDownloadModel()

    wan_animate_model_bf16 = await handle_download_model.function(
        enabled=True,
        config=video_model_config_loader.function(True, "comfy-Wan-22-Animate-14B-bf16"),
    )

    wan_22_clip_bf16 = await handle_download_model.function(
        enabled=True,
        config=clip_model_config_loader.function(True, "kj-umt5-bf16"),
    )

    wan_21_vae_bf16 = await handle_download_model.function(
        enabled=True,
        config=vae_model_config_loader.function(True, "kj-wan-21-bf16"),
    )

    wan_animate_yolo = await huggingface_downloader.function(
        enabled=True,
        model_config="{}",
        model_type="detection",
        model_subfolder="",
        repo_id="Wan-AI/Wan2.2-Animate-14B",
        filename="process_checkpoint/det/yolov10m.onnx",
    )
    wan_animate_vitpose_bin = await huggingface_downloader.function(
        enabled=True,
        model_config="{}",
        model_type="detection",
        model_subfolder="",
        repo_id="Kijai/vitpose_comfy",
        filename="onnx/vitpose_h_wholebody_data.bin",
    )
    wan_animate_vitpose_onnx = await huggingface_downloader.function(
        enabled=True,
        model_config="{}",
        model_type="detection",
        model_subfolder="",
        repo_id="Kijai/vitpose_comfy",
        filename="onnx/vitpose_h_wholebody_model.onnx",
    )

    print("Init models finished.")
