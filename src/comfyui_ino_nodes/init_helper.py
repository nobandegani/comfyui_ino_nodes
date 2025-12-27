import asyncio

from .workflow_helpers.download_model_helper import InoHuggingFaceDownloadModel

def init_models():
    huggingface_downloader = InoHuggingFaceDownloadModel()

    wan_animate_yolo = asyncio.run(huggingface_downloader.function(
        enabled=True,
        model_config="{}",
        model_type="detection",
        model_subfolder="",
        repo_id="Wan-AI/Wan2.2-Animate-14B",
        filename="process_checkpoint/det/yolov10m.onnx",
    ))
    wan_animate_vitpose_bin = asyncio.run(huggingface_downloader.function(
        enabled=True,
        model_config="{}",
        model_type="detection",
        model_subfolder="",
        repo_id="Kijai/vitpose_comfy",
        filename="onnx/vitpose_h_wholebody_data.bin",
    ))
    wan_animate_vitpose_onnx = asyncio.run(huggingface_downloader.function(
        enabled=True,
        model_config="{}",
        model_type="detection",
        model_subfolder="",
        repo_id="Kijai/vitpose_comfy",
        filename="onnx/vitpose_h_wholebody_model.onnx",
    ))
