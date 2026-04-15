from pathlib import Path
from rapidfuzz import process, utils

import requests

class Game_Imagery():
    IMAGES_PATH = Path(__file__).parent.parent.joinpath("Images")
    BASE_API_URL = "api.thegamesdb.net"
    
    def __init__(self):
        pass
    
    def getImagePathByName(self, name: str, platform: str, api_key: str):
        if self.IMAGES_PATH.joinpath(platform).exists():
            image = next((p for p in self.IMAGES_PATH.joinpath(platform).iterdir() if p.is_file() and p.stem == name), None)
            if image:
                return image
        else:
            image_url = self.getUrlFromGame(name, platform)
            if image_url is None:
                return None
            print(image_url)
            response = requests.get(image_url)
            if response.status_code == 200:
                platform_path = self.IMAGES_PATH.joinpath(platform)
                platform_path.mkdir(parents=True, exist_ok=True)
                suffix = Path(image_url).suffix  # preserve .png/.jpg etc
                image_path = platform_path.joinpath(name + suffix)
                image_path.write_bytes(response.content)
                return image_path
            else:
                print(response.reason)
        return None