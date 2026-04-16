from pathlib import Path
from rapidfuzz import process, utils

class Game_Imagery():
    IMAGES_PATH = Path(__file__).parent.parent.joinpath("Images")
    BASE_API_URL = "api.thegamesdb.net"
    
    def __init__(self):
        pass
    
    def getImageByName(self, name: str, platform: str, api_key: str, api_id: int):
        if self.IMAGES_PATH.joinpath(platform).exists():
            print(name)
            print('\"' + platform + '\"')
            image = next((p for p in self.IMAGES_PATH.joinpath(platform).iterdir() if p.is_file() and p.stem == name), None)
            if image:
                return image.read_bytes()
            else:
                image = self.IMAGES_PATH.joinpath("cart_image_not_found.png")
                return image.read_bytes()
        else:
            image = self.IMAGES_PATH.joinpath("cart_image_not_found.png")
            return image.read_bytes()
        #elif api_key != "":
        #    
        #    return
        #return None
    