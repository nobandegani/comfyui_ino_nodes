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

    _, yolo_face_8m, _ = await huggingface_downloader.function(
        enabled=True,
        model_config="{}",
        model_type="ultralytics",
        model_subfolder="bbox",
        repo_id="Bingsu/adetailer",
        filename="face_yolov8m.pt",
    )
    print(f"yolo_face_8m: {yolo_face_8m}")

    _, yolo_11x, _ = await huggingface_downloader.function(
        enabled=True,
        model_config="{}",
        model_type="ultralytics",
        model_subfolder="segm",
        repo_id="Ultralytics/YOLO11",
        filename="yolo11x-seg.pt",
    )
    print(f"yolo_11x: {yolo_11x}")

    _, yolo_person_12l, _ = await huggingface_downloader.function(
        enabled=True,
        model_config="{}",
        model_type="ultralytics",
        model_subfolder="segm",
        repo_id="RyanJames/yolo12l-person-seg",
        filename="yolo12l-person-seg.pt",
    )
    print(f"yolo_person_12l: {yolo_person_12l}")

    _, yolo_person_8m, _ = await huggingface_downloader.function(
        enabled=True,
        model_config="{}",
        model_type="ultralytics",
        model_subfolder="segm",
        repo_id="Bingsu/adetailer",
        filename="person_yolov8m-seg.pt",
    )
    print(f"yolo_person_8m: {yolo_person_8m}")

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

"""
import asyncio
from .src.comfyui_ino_nodes.init_helper import init_models

_init_task: asyncio.Task | None = None

def ensure_models_init() -> asyncio.Task:
    global _init_task
    if _init_task is not None:
        return _init_task

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        _init_task = asyncio.run(init_models())
        return _init_task

    _init_task = loop.create_task(init_models())
    return _init_task

ensure_models_init()
"""
