import os
import asyncio

from botocore.config import Config

from inopyutils import InoS3Helper, InoHttpHelper, InoFileHelper, ino_err, ino_ok, ino_is_err

class FileSyncer:
    def __init__(self):
        self.global_comfy_models: dict[str, list[str]] = {
            "flux-2-dev": [
                "comfyui/models/diffusion_models/flux-2-dev",
                "comfyui/models/text_encoders/Flux2",
                "comfyui/models/vae/Flux2"
            ],
            "flux-2-klein-9b-base": [
                "comfyui/models/diffusion_models/flux-2-klein-9b-base",
                "comfyui/models/text_encoders/Flux2",
                "comfyui/models/vae/Flux2"
            ],
            "flux-2-loras": [
                "comfyui/models/loras/flux2",
            ],
            "wan-22-i2v": [
                "comfyui/models/diffusion_models/wan-22-i2v",
                "comfyui/models/text_encoders/Wan",
                "comfyui/models/vae/Wan"
            ],
            "yolo": [
                "comfyui/models/detection",
                "comfyui/models/ultralytics",
            ],
            "lightx2v": [
                "comfyui/models/loras/lightx2v"
            ],
            "vibe-voice": [
                "comfyui/models/vibevoice"
            ],
            "qwen-llm-1": [
                "comfyui/models/prompt_generator",
            ],
            "qwen-llm-2": [
                "comfyui/models/LLM/Qwen-VL",
            ]
        }

        self.s3_config = Config(
            retries={
                'max_attempts': 30,
                'mode': 'adaptive'
            },
            connect_timeout=600,
            read_timeout=600,
            max_pool_connections=50,
        )
        self.s3_url: str = os.getenv("SYNC_S3_URL", "")
        self.s3_region: str = os.getenv("SYNC_S3_REGION", "")
        self.s3_bucket: str = os.getenv("SYNC_S3_BUCKET", "")
        self.s3_id: str = os.getenv("SYNC_S3_ID", "")
        self.s3_secret: str = os.getenv("SYNC_S3_SECRET", "")

        self.s3_client = InoS3Helper()
        self.s3_client.init(
            aws_access_key_id=self.s3_id,
            aws_secret_access_key=self.s3_secret,
            endpoint_url=self.s3_url,
            region_name=self.s3_region,
            bucket_name=self.s3_bucket,
            retries=10,
            config=self.s3_config,
        )

        self.local_comfy_path = os.getenv("SYNC_COMFY_ROOT", "/app")

        self.comfy_models = self.get_list_from_env_var("SYNC_COMFY_MODELS", )
        self.sync_folders = []

    def get_list_from_env_var(self, var_name:str, ) -> list[str]:
        var_value = os.getenv(var_name, None)
        if var_value is None:
            return []
        items: list[str] = [s.strip() for s in var_value.split(",") if s.strip()]
        return items

    def prepare_comfy_models(self):
        valid_models: list[str] = []

        existing_folders = [folder.strip() for folder in self.sync_folders if folder.strip()]
        seen_folders: set[str] = set(existing_folders)
        folders_to_add: list[str] = []

        if "all" in self.comfy_models:
            self.comfy_models = list(self.global_comfy_models.keys())

        for model in self.comfy_models:
            model_folders = self.global_comfy_models.get(model)
            if model_folders is None:
                print(f"Model {model} not found in global list. Skipping...")
                continue

            valid_models.append(model)

            for folder in model_folders:
                folder = folder.strip()
                if folder and folder not in seen_folders:
                    seen_folders.add(folder)
                    folders_to_add.append(folder)

        self.comfy_models = valid_models
        self.sync_folders.extend(folders_to_add)
        print(f"Valid models: {self.comfy_models}")
        print(f"Folders to sync: {self.sync_folders}")

    async def sync_files(self):
        for folder in self.sync_folders:
            local_folder_path = folder.replace("comfyui", self.local_comfy_path, 1)
            print(f"Syncing folder started for {folder} to {local_folder_path}")

            syncfolder_res = await self.s3_client.sync_folder(
                s3_key=folder,
                local_folder_path=local_folder_path,
                concc=10
            )
            if ino_is_err(syncfolder_res):
                print(f"Syncing folder failed for {folder}: {syncfolder_res['msg']}")
            else:
                print(f"Syncing Folder finished for {folder}")

async def main():
    print("Sync assets starting...")
    file_syncer = FileSyncer()
    file_syncer.prepare_comfy_models()
    await file_syncer.sync_files()

if __name__ == "__main__":
    asyncio.run(main())
