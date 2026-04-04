import os
from pathlib import Path

from PIL import Image
from PIL.PngImagePlugin import PngInfo
import numpy as np
from inopyutils import ino_is_err, InoUtilHelper

import folder_paths
from comfy.cli_args import args
from comfy_api.latest import io

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING


class InoS3UploadImage(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoS3UploadImage",
            display_name="Ino S3 Upload Image",
            category="InoS3Helper",
            description="Saves images as PNG to temp then uploads them to S3.",
            is_output_node=True,
            inputs=[
                io.Boolean.Input("enabled", default=True, label_off="OFF", label_on="ON"),
                io.Image.Input("images"),
                io.String.Input("s3_key", default=""),
                io.String.Input("filename", default=""),
                io.String.Input("s3_config", default=S3_EMPTY_CONFIG_STRING, optional=True, tooltip="you can leave it empty and pass it with env vars"),
                io.Int.Input("compress_level", default=4, min=1, max=9, optional=True),
                io.Boolean.Input("date_time_as_name", default=False, optional=True),
            ],
            outputs=[
                io.Image.Output(display_name="images"),
                io.Boolean.Output(display_name="success"),
                io.String.Output(display_name="message"),
                io.String.Output(display_name="file_names"),
                io.String.Output(display_name="s3_image_paths"),
            ],
        )

    @classmethod
    async def execute(cls, enabled, images, s3_key, filename, s3_config=None, compress_level=4, date_time_as_name=False) -> io.NodeOutput:
        if not enabled:
            return io.NodeOutput(images, False, "", "", "")

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return io.NodeOutput(images, False, validate_s3_key["msg"], "", "")

        if date_time_as_name:
            filename = InoUtilHelper.get_date_time_utc_base64()

        temp_path = folder_paths.get_temp_directory()
        full_output_folder, file_prefix, counter, subfolder, _ = folder_paths.get_save_image_path(filename, temp_path, images[0].shape[1], images[0].shape[0])

        results = {}
        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()

            filename_with_batch_num = file_prefix.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}"
            file_w_ext = file + ".png"
            full_path = os.path.join(full_output_folder, file_w_ext)
            img.save(full_path, pnginfo=metadata, compress_level=compress_level)
            results[batch_number] = {"filename": file, "filename_w_ext": file_w_ext, "full_path": full_path}
            counter += 1
            img.close()

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return io.NodeOutput(images, False, s3_instance["msg"], "", "")
        s3_instance = s3_instance["instance"]

        for index in results:
            s3_full_key = s3_key + "/" + results[index]["filename_w_ext"]
            s3_result = await s3_instance.upload_file(s3_key=s3_full_key, local_file_path=results[index]["full_path"])
            results[index]["s3_success"] = s3_result["success"]
            results[index]["s3_msg"] = s3_result["msg"]
            results[index]["s3_key"] = s3_full_key

        final_success = True
        final_message = ""
        for index in results:
            if not results[index]["s3_success"]:
                final_success = False
                final_message = results[index]["s3_msg"]
                break

        if not final_success:
            return io.NodeOutput(images, final_success, final_message, "", "")

        s3_paths = [results[i]["s3_key"] for i in results]
        file_names = [results[i]["filename"] for i in results]

        return io.NodeOutput(images, True, "Success", str(file_names), str(s3_paths))
