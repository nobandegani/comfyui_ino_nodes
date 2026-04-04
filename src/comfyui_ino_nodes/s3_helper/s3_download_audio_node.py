from pathlib import Path

from inopyutils import ino_is_err, InoUtilHelper

from comfy_api.latest import io

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING
from ..node_helper import PARENT_FOLDER_OPTIONS, resolve_comfy_path


class InoS3DownloadAudio(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoS3DownloadAudio",
            display_name="Ino S3 Download Audio",
            category="InoS3Helper",
            description="Downloads an audio file from S3 and returns it as an AUDIO tensor.",
            inputs=[
                io.Boolean.Input("enabled", default=True, label_off="OFF", label_on="ON"),
                io.String.Input("s3_key", default="input/example.wav"),
                io.Combo.Input("parent_folder", options=PARENT_FOLDER_OPTIONS, default="temp"),
                io.String.Input("folder", default=""),
                io.String.Input("s3_config", default=S3_EMPTY_CONFIG_STRING, optional=True, tooltip="you can leave it empty and pass it with env vars"),
            ],
            outputs=[
                io.Boolean.Output(display_name="success"),
                io.String.Output(display_name="message"),
                io.String.Output(display_name="rel_path"),
                io.String.Output(display_name="abs_path"),
                io.Audio.Output(display_name="audio"),
            ],
        )

    @classmethod
    async def execute(cls, enabled, s3_key, parent_folder, folder, s3_config=None) -> io.NodeOutput:
        if not enabled:
            return io.NodeOutput(False, "not enabled", "", "", None)

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return io.NodeOutput(False, validate_s3_key["msg"], "", "", None)

        random_str = InoUtilHelper.get_date_time_utc_base64()
        file_name = f'{random_str}{Path(s3_key).suffix}'
        rel_path, abs_path = resolve_comfy_path(parent_folder, folder, file_name)

        Path(abs_path).parent.mkdir(parents=True, exist_ok=True)

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return io.NodeOutput(False, s3_instance["msg"], "", "", None)
        s3_instance = s3_instance["instance"]

        downloaded = await s3_instance.download_file(s3_key=s3_key, local_file_path=abs_path)
        if not downloaded["success"]:
            return io.NodeOutput(downloaded["success"], downloaded["msg"], rel_path, abs_path, None)

        from comfy_extras.nodes_audio import LoadAudio

        folder_suffix = folder if folder else ""
        annotated_name = f"{folder_suffix}/{file_name} [{parent_folder}]" if folder_suffix else f"{file_name} [{parent_folder}]"
        load_audio = LoadAudio.execute(audio=annotated_name)

        if load_audio[0]:
            return io.NodeOutput(True, "Success", rel_path, abs_path, load_audio[0])

        return io.NodeOutput(False, "failed to load the audio", rel_path, abs_path, None)
