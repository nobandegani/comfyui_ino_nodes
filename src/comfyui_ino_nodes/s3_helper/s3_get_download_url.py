from inopyutils import ino_is_err

from comfy_api.latest import io

from .s3_helper import S3Helper, S3_EMPTY_CONFIG_STRING


class InoS3GetDownloadURL(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="InoS3GetDownloadURL",
            display_name="Ino S3 Get Download URL",
            category="InoS3Helper",
            description="Generates a presigned download URL for an S3 object.",
            inputs=[
                io.Boolean.Input("enabled", default=True, label_off="OFF", label_on="ON"),
                io.String.Input("s3_key", default="input/example.png"),
                io.Int.Input("expires_in", default=3600, min=1, max=3600, step=1),
                io.Boolean.Input("as_attachment", default=False),
                io.String.Input("filename", default=""),
                io.String.Input("s3_config", default=S3_EMPTY_CONFIG_STRING, optional=True, tooltip="you can leave it empty and pass it with env vars"),
                io.String.Input("bucket_name", default="default", optional=True),
            ],
            outputs=[
                io.Boolean.Output(display_name="success"),
                io.String.Output(display_name="message"),
                io.String.Output(display_name="download_url"),
                io.String.Output(display_name="filename"),
            ],
        )

    @classmethod
    async def execute(cls, enabled, s3_key, expires_in=3600, as_attachment=False, filename=None, s3_config=None, bucket_name=None) -> io.NodeOutput:
        if not enabled:
            return io.NodeOutput(False, "not enabled", "", "")

        validate_s3_key = S3Helper.validate_s3_key(s3_key)
        if not validate_s3_key["success"]:
            return io.NodeOutput(False, validate_s3_key["msg"], "", "")

        s3_instance = S3Helper.get_instance(s3_config)
        if ino_is_err(s3_instance):
            return io.NodeOutput(False, s3_instance["msg"], "", "")
        s3_instance = s3_instance["instance"]

        s3_result = await s3_instance.get_download_link(s3_key=s3_key, expires_in=expires_in, as_attachment=as_attachment, filename=filename)
        return io.NodeOutput(s3_result["success"], s3_result["msg"], s3_result["url"], s3_result["filename"])
