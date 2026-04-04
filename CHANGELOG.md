# Changelog — ComfyUI-InoNodes

---

## 0.19.0

**Full migration to ComfyUI V3 schema across all nodes.**

- Migrated every node to V3 pattern (`io.ComfyNode` + `define_schema` + `execute` classmethod + `io.NodeOutput`) — 48 files rewritten (~4,600 insertions, ~4,700 deletions)
- Added `video_helper.py` with preview video node
- Added S3 download string and download video nodes
- Added `publish.py` for PyPI package publishing
- Added `CLAUDE.md` project documentation
- Unified image load/save nodes with shared `load_image` and `load_images_from_folder` in `node_helper.py`
- Added mask output to image loading nodes
- Expanded `string_helper.py` with additional string manipulation nodes
- Removed `prompt_helper.py` (random character prompt generator)
- Removed `util_helper.py`
- Major rewrites to `sampler_helper`, `download_model_helper`, `load_model_helper`, `image_helper`

## 0.18.0

**New Runpod integration, S3 sync/verify nodes, and broad improvements across all modules.**

- Added `runpod_helper.py` — Runpod serverless vLLM inference node
- Added `s3_sync_folder_node.py` — bidirectional S3 folder sync
- Added `s3_verify_file_node.py` — S3 file verification
- Added int and float compare nodes to `bool_helper.py` and `float_helper.py`
- Removed `init_helper.py` (functionality consolidated elsewhere)
- Major `image_helper.py` improvements (resize, crop, batch operations expanded)
- Improved all class helpers (`file_helper`, `http_helper`, `json_helper`, `openai_helper`)
- Expanded `lora_helper.py` with enhanced multi-LoRA loading
- Refactored `extra_nodes.py` (relay, switches, delay, logging nodes improved)
- Removed legacy test files and frontend JS extension
- Updated `sync_assets.py`

## 0.17.2

- Improved `sync_assets.py` with better error handling and configuration

## 0.17.1

- Added `sync_assets.py` — asset synchronization utility for managing model/data files (127 lines)
- Updated requirements

## 0.17.0

**Re-added S3 video upload and new LoRA data files.**

- Added `s3_upload_video_node.py` — S3 video upload node
- Created `lora_files.csv` for LoRA model download configurations
- Refactored `download_model_helper.py` (simplified download logic)
- Updated video model data files

## 0.16.4

- Added Civitai Klein NSFW model configuration
- Fixed S3 upload audio node (multiple iteration fixes for encoding/upload)
- Updated image, video, and clip model data files

## 0.16.3

- Updated image model and clip model data files with new entries

## 0.16.2

- Added Klein model configurations to image, clip, and VAE data files

## 0.16.1

- Added `DateTimeDuration` node to `time_helper.py`
- Updated image model data files

## 0.16.0

**New initialization system and major image helper expansion.**

- Added `init_helper.py` — initialization utilities for startup model/config management (135 lines)
- Added `util_helper.py` for shared utility functions
- Major `image_helper.py` expansion with new image processing nodes (+228 lines)
- Added new file operations to `file_helper.py`
- Expanded `string_helper.py` with additional string nodes
- Updated basic auth middleware
- Overhauled all model data files (clip, controlnet, image, vae, video)

## 0.15.1

- Started ComfyUI V3 schema migration (initial conversion of `bool_helper.py`)
- Added Mistral 3 FP8 model to clip data files
- Expanded `path_helper.py` with new path utility nodes
- Expanded `string_helper.py` with additional string operations

## 0.15.0

**New model loader system — split download and load into separate modules.**

- Split `model_helper.py` into `download_model_helper.py` and `load_model_helper.py`
- Added `load_model_helper.py` — 9 nodes for loading VAE, CLIP, ControlNet, and Diffusion models (466 lines)
- Added `controlnet_files.csv` for ControlNet model configurations
- Added Qwen model entries to data files

## 0.14.0

**New media helper and expanded model catalog.**

- Added `media_helper.py` — FFmpeg-based video conversion node
- Added Flux 2, Wan 2.2, and additional video models to download configurations
- Updated clip, vae, and video model data files

## 0.13.0

**CSV-based model configuration system.**

- Added CSV reader to `model_helper.py` for loading model download configs from CSV files
- Reorganized data files into `data/configs/` and `data/files/` subdirectories
- Updated model data files

## 0.12.3

- Split unified model data into per-type CSV files: `clip_files.csv`, `image_models_files.csv`, `video_models_files.csv`, `vae_files.csv`, plus config CSVs
- Removed old unified `models_config.csv` and `models_files.csv`
- Updated `node_helper.py` and `model_helper.py` to use new file structure

## 0.12.2

- Added `path_helper.py` — path utility nodes (file path manipulation)
- Expanded `file_helper.py` with additional file operations (+113 lines)
- Expanded `string_helper.py` with new string manipulation nodes
- Fixed S3 upload nodes (audio, image, string)
- Updated `model_helper.py` with improved download handling

## 0.12.1

- Fixed basic auth middleware edge cases
- Fixed S3 helper connection and debug logging
- Added debug logging to S3 download/upload nodes

## 0.12.0

**Massive feature expansion — cast nodes, time nodes, audio S3, model loader, and much more.**

- Added `cast_helper.py` — 6 type casting nodes (Any to String/Int/Model/Clip/Vae/ControlNet)
- Added `time_helper.py` — 4 DateTime formatting and duration nodes
- Added `s3_download_audio_node.py` and `s3_upload_audio_node.py` — S3 audio transfer
- Added `s3_get_download_url.py` — presigned URL generation for S3 objects
- Added HuggingFace repository download support to `model_helper.py`
- Added control net loader node
- Added model loader node from JSON/CSV config
- Added debug logging (`ino_print_log`) across all helper modules
- Added S3 environment variable support (`S3_ACCESS_KEY`, `S3_ACCESS_SECRET`, etc.)
- Added download config and LoRA config nodes
- Created `models_config.csv` and `models_files.csv` for CSV-based model management
- Added 32-bit support to random noise node
- Added multi-bool condition node
- Major expansion of `model_helper.py` (+681 lines) and `sampler_helper.py` refactor
- Improved `openai_helper.py` with OpenAI Responses API support

## 0.11.0

**Major project restructure — new directory layout, basic auth, and model/node helpers.**

- Restructured project into `class_helpers/`, `node_helpers/`, `workflow_helpers/` directories
- Moved `file_helper`, `http_helper`, `json_helper`, `openai_helper` to `class_helpers/`
- Moved `lora_helper`, `prompt_helper`, `sampler_helper` to `workflow_helpers/`
- Added `basic_auth.py` — HTTP Basic Auth middleware for ComfyUI endpoints
- Added `model_helper.py` — model download management from S3 and HuggingFace (265 lines)
- Added `bool_helper.py` — 4 boolean operation nodes
- Added `float_helper.py` — 2 float operation nodes
- Added `int_helper.py` — 4 integer operation nodes
- Added `image_helper.py` — image load, save, resize nodes (204 lines)
- Added `string_helper.py` — string manipulation nodes
- Added `web/js/inonodes.js` — frontend extension for dynamic input UI
- Created `data/models.json` for centralized model configuration (610 lines)
- Added environment variable support for all S3 nodes

## 0.10.0

**New OpenAI integration, S3 string upload, and image save node.**

- Added `openai_helper.py` — OpenAI API integration (responses + chat completions)
- Added `s3_upload_string_node.py` — upload text content to S3
- Added image save node to `extra_nodes.py`
- Removed `node_cloudreve.py` and `node_utils.py` permanently (code consolidated into helpers)
- Simplified `http_helper.py` to use shared helper utilities
- Updated S3 upload file/image nodes with better error handling

## 0.9.0

**New HTTP client, JSON nodes, and S3 folder operations.**

- Added `http_helper.py` — REST client node supporting GET/POST/PUT/DELETE/PATCH
- Added `json_helper.py` — JSON field manipulation and save nodes
- Added `s3_download_folder_node.py` and `s3_upload_folder_node.py` — S3 folder transfer
- Added S3 __init__.py with node class aggregation
- Major `__init__.py` restructure (cleaner node registration)
- Refactored `sampler_helper.py`
- Expanded `extra_nodes.py` with new utility nodes
- Updated README with comprehensive documentation

## 0.8.0

**S3 config refactor and new utility nodes.**

- Refactored S3 from client-based to `s3_helper.py` (S3Helper class with shared connection)
- Added `node_helper.py` — shared utilities (`resolve_comfy_path`, etc.)
- Added random noise node, random int in range node, datetime random int node
- Added int to string node
- Added JSON helper nodes (create, parse, save)
- Changed S3 config from environment variables to ComfyUI input nodes
- Removed `s3_upload_video_node.py` (temporarily, re-added later)
- Fixed int max limit in random int node
- Updated pyproject.toml and README

## 0.7.0

**New S3 cloud storage integration.**

- Added S3 helper module with `s3_client.py` for AWS S3 / compatible storage
- Added S3 upload nodes: file, video, image
- Added S3 download nodes: file, image
- Updated sampler helper with model config management
- Updated model configurations

## 0.6.0

**New extra nodes, LoRA helper, and prompt helper.**

- Added `extra_nodes.py` — relay, switches, delay, and logging utility nodes (150 lines)
- Added `lora_helper.py` — load and apply multiple LoRAs (99 lines)
- Added `prompt_helper.py` — random character prompt generator (416 lines)
- Removed `node_utils.py` (code split into new modules)
- Added lora applied bool output to sampler helper
- Added sampler helper node

## 0.5.0

**Major cleanup — removed legacy modules, added LoRA support to sampler.**

- Removed bedrive module entirely (upload helper, save file/image, get parent ID)
- Removed deprecated module (old video convert, legacy nodes)
- Added `loras.json` configuration for LoRA models
- Major `sampler_helper.py` rewrite with LoRA support (+545 lines changed)
- Added trigger words support, show LoRA and model config nodes
- Updated model configurations and paths

## 0.4.1

- Updated sampler helper with additional model configurations

## 0.4.0

**New sampler helper with model config system.**

- Added `sampler_helper.py` — complete sampler configuration node (369 lines)
- Created `models.json` configuration file for model presets (136 entries)
- Added bool switch node to `node_utils.py`
- Renamed `node_file_helper.py` to `file_helper.py`

## 0.3.0

**Project reorganization and file helper.**

- Reorganized project into subdirectories: `bedrive/`, `depricated/`, `utils/`
- Moved bedrive nodes into `bedrive/` subfolder
- Moved legacy nodes into `depricated/` subfolder
- Added `node_file_helper.py` — InoFileHelper nodes for file operations (273 lines)
- Re-added Cloudreve support with expanded upload/download functionality
- Added pyproject.toml and updated requirements.txt

## 0.2.0

**Cloudreve cleanup and new utility nodes.**

- Created `requirements.txt`
- Removed `helper_cloudreve.py` (functionality inlined)
- Added seed to batch type node
- Added sample every N node
- Added toggle case node
- Fixed calculate LoRA configuration
- Cleaned up Cloudreve node

## 0.1.1

- Bug fix for batch folder node

## 0.1.0

**Cloudreve integration and batch utilities.**

- Added `helper_cloudreve.py` — Cloudreve cloud storage helper
- Added `node_cloudreve.py` — Cloudreve upload/download nodes
- Added calculate LoRA config utility
- Added batch folder ID and get batch utilities to `node_utils.py`

## 0.0.3

- Major rewrite of character prompt generator with expanded options and improved generation logic (+310 lines, -78 lines)

## 0.0.2

- Added `RandomCharacterPrompt` node for generating random character descriptions (190 lines)

## 0.0.1

**Initial release.**

- Project initialization with basic ComfyUI custom node structure
- Added Bedrive integration nodes (save file, save image, get parent ID)
- Added FFmpeg video convert node
- Added file count node
- Added upload helper utility
