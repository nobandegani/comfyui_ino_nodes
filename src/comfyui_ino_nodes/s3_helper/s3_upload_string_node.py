import os
from pathlib import Path

from inopyutils import InoJsonHelper, InoFileHelper, ino_is_err, InoUtilHelper

import folder_paths
from comfy_api.latest import io

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING


class InoS3UploadString(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoS3UploadString",
            display_name="Ino S3 Upload String",
            category="InoS3Helper",
            description="Saves a string as a file (txt/json/ini) to temp then uploads it to S3.",
            is_output_node=True,
            inputs=[
                io.Boolean.Input("enabled", default=True, label_off="OFF", label_on="ON"),
                io.String.Input("string"),
                io.Combo.Input("save_as", options=["txt", "json", "ini"]),
                io.String.Input("s3_key", default=""),
                io.String.Input("filename", default=""),
                io.String.Input("s3_config", default=S3_EMPTY_CONFIG_STRING, optional=True, tooltip="you can leave it empty and pass it with env vars"),
                io.Boolean.Input("date_time_as_name", default=False, optional=True),
            ],
            outputs=[
                io.String.Output(display_name="string"),
                io.Boolean.Output(display_name="success"),
                io.String.Output(display_name="message"),
                io.String.Output(display_name="file_name"),
                io.String.Output(display_name="s3_string_path"),
            ],
        )

    @classmethod
    async def execute(cls, enabled, string, save_as, s3_key, filename, s3_config=None, date_time_as_name=False) -> io.NodeOutput:
        if not enabled:
            return io.NodeOutput(string, False, "", "", "")

        if isinstance(filename, list):
            if len(filename) == 1:
                filename = str(filename[0])
            else:
                return io.NodeOutput(string, False, "file name is list", "", "")
        elif not isinstance(filename, str):
            return io.NodeOutput(string, False, "file name not string", "", "")

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return io.NodeOutput(string, False, validate_s3_key["msg"], "", "")

        if date_time_as_name:
            filename = InoUtilHelper.get_date_time_utc_base64()

        temp_path = folder_paths.get_temp_directory()
        full_output_folder, file_prefix, counter, subfolder, _ = folder_paths.get_save_image_path(filename, temp_path, 0, 0)

        filename_with_batch_num = file_prefix.replace("%batch_num%", "0")
        file = f"{filename_with_batch_num}_{counter:05}"
        file_w_ext = f"{file}.{save_as}"
        full_path = os.path.join(full_output_folder, file_w_ext)

        if save_as == "json":
            save_file = await InoJsonHelper.save_string_as_json_async(string, full_path)
        else:
            save_file = await InoFileHelper.save_string_as_file(string, full_path)

        if not save_file["success"]:
            return io.NodeOutput(string, False, save_file["msg"], "", "")

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return io.NodeOutput(string, False, s3_instance["msg"], "", "")
        s3_instance = s3_instance["instance"]

        s3_full_key = f"{s3_key.rstrip('/')}/{filename}.{save_as}"
        s3_result = await s3_instance.upload_file(s3_key=s3_full_key, local_file_path=full_path)
        if not s3_result["success"]:
            return io.NodeOutput(string, False, s3_result["msg"], "", "")

        return io.NodeOutput(string, True, "Success", file_w_ext, s3_full_key)
