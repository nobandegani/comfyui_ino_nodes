from pathlib import Path

from inopyutils import InoMediaHelper

from comfy_api.latest import io

from ..node_helper import PARENT_FOLDER_OPTIONS, resolve_comfy_path


class InoConvertVideoToMP4(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoConvertVideoToMP4",
            display_name="Ino Convert Video To MP4",
            category="InoMediaHelper",
            description="Converts video files to MP4 format via FFmpeg with optional FPS and resolution changes.",
            is_output_node=True,
            inputs=[
                io.Boolean.Input("enabled", default=True, label_off="OFF", label_on="ON"),
                io.Combo.Input("input_parent_folder", options=PARENT_FOLDER_OPTIONS),
                io.String.Input("input_folder", default=""),
                io.Combo.Input("output_parent_folder", options=PARENT_FOLDER_OPTIONS),
                io.String.Input("output_folder", default=""),
                io.Boolean.Input("change_fps", default=True, optional=True),
                io.Int.Input("fps", default=30, min=1, max=1000, optional=True),
                io.Boolean.Input("change_resolution", default=True, optional=True),
                io.Int.Input("max_resolution", default=2560, optional=True),
            ],
            outputs=[
                io.Boolean.Output(display_name="success"),
                io.String.Output(display_name="message"),
                io.String.Output(display_name="rel_path"),
                io.String.Output(display_name="abs_path"),
            ],
        )

    @classmethod
    async def execute(cls, enabled, input_parent_folder, input_folder, output_parent_folder, output_folder,
                      change_fps=True, fps=30, change_resolution=True, max_resolution=2560) -> io.NodeOutput:
        if not enabled:
            return io.NodeOutput(False, "Node is disabled", "", "")

        _, input_abs = resolve_comfy_path(input_parent_folder, input_folder)
        rel_path, abs_path = resolve_comfy_path(output_parent_folder, output_folder)

        convert = await InoMediaHelper.video_convert_ffmpeg(
            input_path=Path(input_abs), output_path=Path(abs_path),
            change_res=change_resolution, change_fps=change_fps,
            max_res=max_resolution, max_fps=fps
        )

        return io.NodeOutput(convert["success"], convert["msg"], rel_path, abs_path)


LOCAL_NODE_CLASS = {
    "InoConvertVideoToMP4": InoConvertVideoToMP4,
}
LOCAL_NODE_NAME = {
    "InoConvertVideoToMP4": "Ino Convert Video To MP4",
}
