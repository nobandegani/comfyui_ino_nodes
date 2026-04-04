import os
from pathlib import Path

from inopyutils import ino_is_err, InoUtilHelper

import folder_paths
from comfy_api.latest import io

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING


class InoS3UploadAudio(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoS3UploadAudio",
            display_name="Ino S3 Upload Audio",
            category="InoS3Helper",
            description="Saves audio as MP3 to temp then uploads it to S3.",
            is_output_node=True,
            inputs=[
                io.Boolean.Input("enabled", default=True, label_off="OFF", label_on="ON"),
                io.Audio.Input("audio"),
                io.String.Input("s3_key", default=""),
                io.String.Input("filename", default=""),
                io.String.Input("s3_config", default=S3_EMPTY_CONFIG_STRING, optional=True, tooltip="you can leave it empty and pass it with env vars"),
                io.Boolean.Input("date_time_as_name", default=False, optional=True),
            ],
            outputs=[
                io.Audio.Output(display_name="audio"),
                io.Boolean.Output(display_name="success"),
                io.String.Output(display_name="message"),
                io.String.Output(display_name="file_name"),
                io.String.Output(display_name="s3_audio_path"),
            ],
        )

    @classmethod
    async def execute(cls, enabled, audio, s3_key, filename, s3_config=None, date_time_as_name=False) -> io.NodeOutput:
        if not enabled:
            return io.NodeOutput(audio, False, "", "", "")

        if isinstance(filename, list):
            if len(filename) == 1:
                filename = str(filename[0])
            else:
                return io.NodeOutput(audio, False, "file name is list", "", "")
        elif not isinstance(filename, str):
            return io.NodeOutput(audio, False, "file name not string", "", "")

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return io.NodeOutput(audio, False, validate_s3_key["msg"], "", "")

        if date_time_as_name:
            filename = InoUtilHelper.get_date_time_utc_base64()

        from comfy_extras.nodes_audio import SaveAudioMP3

        audio_saver = SaveAudioMP3()
        save_audio = audio_saver.execute(audio=audio, filename_prefix=filename, format="mp3", quality="128k")

        try:
            saved_filename = save_audio.ui.as_dict()["audio"][0]["filename"]
            parent_path = folder_paths.get_output_directory()
            full_path = str((Path(parent_path) / saved_filename).resolve())
        except:
            return io.NodeOutput(audio, False, "Audio saved, but failed to get filename", "", "")

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return io.NodeOutput(audio, False, s3_instance["msg"], "", "")
        s3_instance = s3_instance["instance"]

        s3_full_key = f"{s3_key.rstrip('/')}/{saved_filename}"
        s3_result = await s3_instance.upload_file(s3_key=s3_full_key, local_file_path=full_path)
        if not s3_result["success"]:
            return io.NodeOutput(audio, False, s3_result["msg"], "", "")

        return io.NodeOutput(audio, True, "Success", saved_filename, s3_full_key)
