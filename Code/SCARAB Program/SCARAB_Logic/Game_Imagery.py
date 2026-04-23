from pathlib import Path
import sys

class Game_Imagery():
    IMAGES_PATH = (Path(sys.executable).parent if hasattr(sys, '_MEIPASS') else Path(__file__).parent.parent) / "Images"
    
    def __init__(self):
        self.IMAGES_PATH.mkdir(parents=True, exist_ok=True)
        pass
    
    def getImageByName(self, name: str, platform: str):
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
    