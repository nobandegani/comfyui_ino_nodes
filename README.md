# Ino Custom Nodes

A comprehensive collection of custom nodes for ComfyUI that provides advanced file handling, S3 cloud storage integration, LoRA configuration management, and various utility functions.

## Installation

### Option 1: Using ComfyUI-Manager (Recommended)
1. Install [ComfyUI](https://docs.comfy.org/get_started)
2. Install [ComfyUI-Manager](https://github.com/ltdrdata/ComfyUI-Manager)
3. Search for "ComfyUI Ino Nodes" in ComfyUI-Manager and install
4. Restart ComfyUI

### Option 2: Manual Installation
1. Clone this repository into your ComfyUI custom_nodes directory:
   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/nobandegani/comfyui_ino_nodes.git
   ```
2. Install dependencies:
   ```bash
   cd comfyui_ino_nodes
   pip install -r requirements.txt
   ```
3. Restart ComfyUI

### Dependencies
- `inocloudreve` - Cloudreve cloud storage integration
- `inopyutils` - Utility functions

## Features

### 🗂️ File & Path Utilities
- **Parse File Path**: Extract components from file paths
- **Count Files**: Count files in directories
- **Branch Image**: Conditional image routing
- **DateTime As String**: Generate datetime strings
- **Get Folder Batch ID**: Generate batch identifiers for folders

### ☁️ Cloud Storage Integration

#### S3 Helper Nodes
- **S3 Upload Image**: Upload images to S3 with metadata preservation
- **S3 Upload File**: Upload any file to S3 storage
- **S3 Upload Video**: Upload video files to S3
- **S3 Download Image**: Download images from S3
- **S3 Download File**: Download any file from S3

#### Cloudreve Integration
- **Cloudreve Init**: Initialize Cloudreve client
- **Cloudreve Signin**: Authenticate with Cloudreve
- **Cloudreve Upload File**: Upload files to Cloudreve storage

### 🎛️ LoRA & Model Management
- **Calculate LoRA Config**: Compute LoRA configurations
- **Get/Show/Update Model Config**: Manage model configurations
- **Get/Show LoRA Config**: Handle LoRA settings
- **Load Sampler Models**: Load and manage sampling models
- **Get Conditioning**: Extract conditioning data
- **Get Sampler Config**: Retrieve sampler configurations

### 🔧 Utility Nodes
- **Random Character Prompt**: Generate random character prompts
- **Bool To Switch**: Convert boolean to switch values
- **Int Equal**: Integer equality comparison
- **Not Boolean**: Boolean negation
- **String Toggle Case**: Toggle string case
- **String To Combo**: Convert string to combo selection

### 📁 File Operations
- **Zip/Unzip**: Archive and extract files
- **Remove File/Folder**: Delete files and directories
- **Increment Batch Name**: Auto-increment batch naming

## Usage

After installation, the nodes will appear in your ComfyUI node menu under the following categories:
- **InoNodes** - File utilities and basic operations
- **InoS3Helper** - S3 cloud storage operations
- **InoCloudreve** - Cloudreve cloud storage integration

Simply drag and drop the nodes into your ComfyUI workflow and configure them according to your needs.

## Requirements

- ComfyUI (latest version recommended)
- Python 3.8+
- Dependencies listed in `requirements.txt`

## License

This project is licensed under the terms specified in the LICENSE file.

## Support

For issues and questions, please visit the [GitHub repository](https://github.com/nobandegani/comfyui_ino_nodes).

---

**Version:** 1.1.5
**Publisher:** Inoland
**Contact:** contact@inoland.net
