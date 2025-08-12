import requests

def fetch_folder_map(api_url, api_token, parent_id):
    """
    Fetches folders from the BeDrive API and returns a dict mapping folder ID to name.
    """
    print("start fetching folder map")

    url = f"{api_url}?perPage=50&type=folder&workspaceId=0"
    if parent_id is not None:
        url += f"&parentIds={parent_id}"

    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.ok:
            json_data = response.json()
            folder_map = {entry["id"]: entry["name"] for entry in json_data.get("data", [])}
            return folder_map
        else:
            print("❌ Error:", response.status_code, response.text)
            return {}
    except Exception as e:
        print("❌ Exception occurred:", str(e))
        return {}

class BeDriveGetParentID:
    @classmethod
    def INPUT_TYPES(s):

        return {
            "required": {
                "api_url": ("STRING", {
                    "multiline": False,
                    "default": "https://drive.sparkcreator.ai/api/v1/drive/file-entries"
                }),
                "api_token": ("STRING", {
                    "multiline": False,
                    "default": "token"
                }),
                "folder": (None,),
            }
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("folder_name", "parent_id")
    FUNCTION = "resolve"
    CATEGORY = "InoNodes"

    def resolve(self, folder, api_url, api_token):
        folder = fetch_folder_map(api_url, api_token, None)

        #print(folders)
        return ("Hello1", 24)

    @classmethod
    def IS_CHANGED(s, directory: str, **kwargs):
        if directory is None:
            return fetch_folder_map(api_url, api_token, None)
