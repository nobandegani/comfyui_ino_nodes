import os
import requests
import mimetypes

def upload_file_to_bedrive(api_token, file_path, parent_id, relative_path=""):
    print("start uploading file to bedrive")

    api_url = "https://drive.sparkcreator.ai/api/v1/uploads"

    if not os.path.exists(file_path):
        return {"success": False, "error": "File does not exist."}

    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    # Build form data
    data = {
        "relativePath": relative_path or os.path.basename(file_path),
        "parentId": None if parent_id == -1 else str(parent_id)
    }

    mime_type, _ = mimetypes.guess_type(file_path)
    mime_type = mime_type or "application/octet-stream"

    with open(file_path, 'rb') as f:
        files = {
            "file": (os.path.basename(file_path), f, mime_type)
        }

        response = requests.post(api_url, headers=headers, files=files, data=data)

    try:
        response_data = response.json()
    except Exception as e:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": f"Failed to parse JSON: {str(e)}",
            "raw_response": response.text
        }

    if response.ok and response_data.get("status") == "success":
        return {
            "success": True
        }
    else:
        return {
            "success": False,
            "status_code": response.status_code,
            "error": response_data.get("message", "Unknown error")
        }
