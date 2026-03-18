from pathlib import Path
import re
from time import gmtime

SAVE_PATH = Path(__file__).parent.parent.joinpath("Saves")

def getBasePath() -> Path:
    return SAVE_PATH

def getNewSaveFilePath(current_module: str, cartridge_name: str) -> str:
    now = gmtime()
    game_name = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', cartridge_name.strip())
    filename = current_module + "/" + game_name + "/" + game_name + "_" + str(now.tm_mday) + "_" + str(now.tm_mon) + "_" + str(now.tm_year) + "_" + str(now.tm_hour) + "_" + str(now.tm_min) + "_" + str(now.tm_sec) + ".sav"
    return filename

def getExistingSaveFilePath(current_module: str, cartridge_name: str, save_name: str) -> str:
    filename = current_module + "/" + cartridge_name + "/" + save_name
    return filename

def getConsolesList() -> list:
    consoles = [folder.name for folder in SAVE_PATH.iterdir() if folder.is_dir()]
    return consoles
    
def getGamesByConsole(console: str) -> list:
    console_path = SAVE_PATH.joinpath(console)
    console_saves = [game.name for game in console_path.iterdir() if game.is_dir()]
    return console_saves

def writeSave(filepath: str, buffer: bytes):
    file = SAVE_PATH.joinpath(filepath)
    file.write_bytes(buffer)
    
def readSave(current_module: str, cartridge_name: str, save_name: str) -> bytes:
    save_path = SAVE_PATH.joinpath(getExistingSaveFilePath(current_module, cartridge_name, save_name))
    return save_path.read_bytes()