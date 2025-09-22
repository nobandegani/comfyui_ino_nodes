import os
import json
import tempfile
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from comfy.cli_args import args
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.config import Config

from dotenv import load_dotenv

load_dotenv()


class S3:
    def __init__(self, region, access_key, secret_key, bucket_name, endpoint_url):
        self.region = region
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.endpoint_url = endpoint_url
        self.s3_client = self.get_client()
        self.input_dir = os.getenv("S3_INPUT_DIR")
        self.output_dir = os.getenv("S3_OUTPUT_DIR")
        if not self.does_folder_exist(self.input_dir):
            self.create_folder(self.input_dir)
        if not self.does_folder_exist(self.output_dir):
            self.create_folder(self.output_dir)

    def get_client(self):
        if not all([self.region, self.access_key, self.secret_key, self.bucket_name]):
            err = "Missing required S3 environment variables."
            print(err)
            #logger.error(err)

        try:
            addressing_style = os.getenv("S3_ADDRESSING_STYLE", "auto")
            if addressing_style not in ["auto", "virtual", "path"]:
                #logger.warning(f"Invalid S3_ADDRESSING_STYLE value: {addressing_style}, using 'auto' instead")
                print(f"Invalid S3_ADDRESSING_STYLE value: {addressing_style}, using 'auto' instead")
                addressing_style = "auto"
            s3_config = Config(
                s3={
                    'addressing_style': addressing_style  # S3 addressing_style: auto/virtual/path
                }
            )

            s3 = boto3.resource(
                service_name='s3',
                region_name=self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                endpoint_url=self.endpoint_url,
                config=s3_config
            )
            return s3
        except Exception as e:
            err = f"Failed to create S3 client: {e}"
            print(err)
            #logger.error(err)

    def get_files(self, prefix):
        if self.does_folder_exist(prefix):
            try:
                bucket = self.s3_client.Bucket(self.bucket_name)
                files = [obj.key for obj in bucket.objects.filter(Prefix=prefix)]
                files = [f.replace(prefix, "") for f in files]
                return files
            except Exception as e:
                err = f"Failed to get files from S3: {e}"
                print(err)
                #logger.error(err)
        else:
            return []

    def does_folder_exist(self, folder_name):
        try:
            bucket = self.s3_client.Bucket(self.bucket_name)
            response = bucket.objects.filter(Prefix=folder_name)
            return any(obj.key.startswith(folder_name) for obj in response)
        except Exception as e:
            err = f"Failed to check if folder exists in S3: {e}"
            print(err)
            #logger.error(err)

    def create_folder(self, folder_name):
        try:
            bucket = self.s3_client.Bucket(self.bucket_name)
            bucket.put_object(Key=f"{folder_name}/")
        except Exception as e:
            err = f"Failed to create folder in S3: {e}"
            print(err)
            #logger.error(err)

    def download_file(self, s3_path, local_path):
        local_dir = os.path.dirname(local_path)
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        try:
            bucket = self.s3_client.Bucket(self.bucket_name)
            bucket.download_file(s3_path, local_path)
            return local_path
        except NoCredentialsError:
            err = "Credentials not available or not valid."
            print(err)
            #logger.error(err)
        except Exception as e:
            err = f"Failed to download file from S3: {e}"
            print(err)
            #logger.error(err)

    def upload_file(self, local_path, s3_path):
        try:
            bucket = self.s3_client.Bucket(self.bucket_name)
            bucket.upload_file(local_path, s3_path)
            return s3_path
        except NoCredentialsError:
            err = "Credentials not available or not valid."
            print(err)
            #logger.error(err)
        except Exception as e:
            err = f"Failed to upload file to S3: {e}"
            print(err)
            #logger.error(err)

    def get_save_path(self, filename_prefix, image_width=0, image_height=0):
        def map_filename(filename):
            prefix_len = len(os.path.basename(filename_prefix))
            prefix = filename[:prefix_len + 1]
            try:
                digits = int(filename[prefix_len + 1:].split('_')[0])
            except:
                digits = 0
            return (digits, prefix)

        def compute_vars(input, image_width, image_height):
            input = input.replace("%width%", str(image_width))
            input = input.replace("%height%", str(image_height))
            return input

        filename_prefix = compute_vars(filename_prefix, image_width, image_height)
        subfolder = os.path.dirname(os.path.normpath(filename_prefix))
        filename = os.path.basename(os.path.normpath(filename_prefix))

        full_output_folder_s3 = os.path.join(self.output_dir, subfolder)

        # Check if the output folder exists, create it if it doesn't
        if not self.does_folder_exist(full_output_folder_s3):
            self.create_folder(full_output_folder_s3)

        try:
            # Continue with the counter calculation
            files = self.get_files(full_output_folder_s3)
            counter = max(
                filter(
                    lambda a: a[1][:-1] == filename and a[1][-1] == "_",
                    map(map_filename, files)
                )
            )[0] + 1
        except (ValueError, KeyError):
            counter = 1

        return full_output_folder_s3, filename, counter, subfolder, filename_prefix


def get_s3_instance():
    try:
        s3_instance = S3(
            region=os.getenv("S3_REGION"),
            access_key=os.getenv("S3_ACCESS_KEY"),
            secret_key=os.getenv("S3_SECRET_KEY"),
            bucket_name=os.getenv("S3_BUCKET_NAME"),
            endpoint_url=os.getenv("S3_ENDPOINT_URL")
        )
        print(f"se_region: {os.getenv("S3_REGION")}")
        print(f"se_region: {os.getenv("S3_ACCESS_KEY")}")
        return s3_instance
    except Exception as e:
        err = f"Failed to create S3 instance: {e} Please check your environment variables."
        print(err)
        #logger.error(err)

S3_INSTANCE = get_s3_instance()

class InoS3UploadFile:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required":{
                "s3_filename": ("STRING", {"default": ""}),
                "local_path": ("STRING", {"default": "input/example.png"}),
                "s3_folder": ("STRING", {"default": "output"}),
                "delete_local": (["false", "true"],),
            }
        }

    CATEGORY = "InoS3Helper"
    INPUT_NODE = True
    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("s3_paths",)
    FUNCTION = "function"

    def function(self, local_path, s3_folder, delete_local, s3_filename):
        if isinstance(local_path, str):
            local_path = [local_path]
        s3_paths = []
        for path in local_path:
            f_name = s3_filename if s3_filename else os.path.basename(path)
            s3_path = os.path.join(s3_folder, f_name)
            file_path = S3_INSTANCE.upload_file(path, s3_path)
            s3_paths.append(file_path)
            if delete_local == "true":
                os.remove(path)
                print(f"Deleted file at {path}")
        print(f"Uploaded file to S3 at {s3_path}")
        return { "ui": { "s3_paths": s3_paths },  "result": (s3_paths,) }


S3_INSTANCE = get_s3_instance()


class InoS3UploadImage:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        self.temp_dir = os.path.join(base_dir, "temp/")
        self.s3_output_dir = os.getenv("S3_OUTPUT_DIR")
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "images": ("IMAGE",),
            "filename_prefix": ("STRING", {"default": "Image"})},
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"
                       },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("s3_image_paths",)
    FUNCTION = "function"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)
    CATEGORY = "InoS3Helper"

    def function(self, images, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = S3_INSTANCE.get_save_path(filename_prefix,
                                                                                                      images[0].shape[
                                                                                                          1],
                                                                                                      images[0].shape[
                                                                                                          0])
        results = list()
        s3_image_paths = list()

        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            file = f"{filename}_{counter:05}_.png"
            temp_file = None
            try:
                # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                    temp_file_path = temp_file.name

                    # Save the image to the temporary file
                    img.save(temp_file_path, pnginfo=metadata, compress_level=self.compress_level)

                    # Upload the temporary file to S3
                    s3_path = os.path.join(full_output_folder, file)
                    file_path = S3_INSTANCE.upload_file(temp_file_path, s3_path)

                    # Add the s3 path to the s3_image_paths list
                    s3_image_paths.append(file_path)

                    # Add the result to the results list
                    results.append({
                        "filename": file,
                        "subfolder": subfolder,
                        "type": self.type
                    })
                    counter += 1

            finally:
                # Delete the temporary file
                if temp_file_path and os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

        return {"ui": {"images": results}, "result": (s3_image_paths,)}
