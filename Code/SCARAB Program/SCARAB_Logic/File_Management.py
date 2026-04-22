from pathlib import Path
import random
import re
from time import gmtime
import configparser

SAVE_PATH = Path(__file__).parent.parent.joinpath("Saves")
SETTINGS_PATH = Path(__file__).parent.parent.joinpath("settings.ini")

def getBasePath() -> Path:
    return SAVE_PATH

def getNewSaveFilePath(current_module: str, cartridge_name: str) -> str:
    now = gmtime()
    game_name = sanitiseString(cartridge_name)
    filename = current_module + "/" + game_name + "/" + game_name + "_" + str(now.tm_mday) + "_" + str(now.tm_mon) + "_" + str(now.tm_year) + "_" + str(now.tm_hour) + "_" + str(now.tm_min) + "_" + str(now.tm_sec) + ".sav"
    return filename

def getExistingSaveFilePath(current_module: str, cartridge_name: str, save_name: str) -> str:
    cartridge_name = sanitiseString(cartridge_name)
    filename = current_module + "/" + cartridge_name + "/" + save_name
    return filename

def getConsolesList() -> list:
    consoles = [folder.name for folder in SAVE_PATH.iterdir() if folder.is_dir()]
    return consoles
    
def getGamesByConsole(module: str) -> list:
    console_path = SAVE_PATH.joinpath(module)
    console_games = [game.name for game in console_path.iterdir() if game.is_dir()]
    return console_games

def getSavesByGame(module: str, game: str):
    saves_path = SAVE_PATH.joinpath(module, sanitiseString(game))
    saves = [save.name for save in saves_path.iterdir() if save.suffix == '.sav']
    return saves

def writeSave(filepath: str, buffer: bytes):
    file = SAVE_PATH.joinpath(filepath)
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_bytes(buffer)    
    
def readSave(current_module: str, cartridge_name: str, save_name: str) -> bytes:
    save_path = SAVE_PATH.joinpath(getExistingSaveFilePath(current_module, cartridge_name, save_name))
    return save_path.read_bytes()

def renameSave(console: str, game: str, old_name: str, new_name: str):
    if not new_name.endswith('.sav'):
        new_name += '.sav'
    old_path = SAVE_PATH.joinpath(getExistingSaveFilePath(console, game, old_name))
    new_path = old_path.parent.joinpath(sanitiseString(new_name))
    old_path.rename(new_path)

def sanitiseString(string: str):
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', string.strip())

def retentionWriteTempSave(buffer: bytes, cartridge_name: str):
    cartridge_name = sanitiseString(cartridge_name)
    writeSave("TEMP/" + cartridge_name + ".sav", buffer)
    
def retentionReadTempSave(cartridge_name: str):
    cartridge_name = sanitiseString(cartridge_name)
    path = SAVE_PATH.joinpath("TEMP/" + cartridge_name + ".sav")
    return path.read_bytes()

def deleteSave(filename: str, console: str, game: str):
    save_path = SAVE_PATH.joinpath(getExistingSaveFilePath(console, game, filename))
    save_path.unlink(True)

def generateDummySave(size) -> bytes:
    random.seed()
    return bytes(random.getrandbits(8) for _ in range(size))

def generateSettings():
    if not Path(SETTINGS_PATH).exists():
        settings = configparser.ConfigParser()
        settings['API'] = {'gamesdbapikey': ''}
        settings['SCARAB'] = {'autoid': 'no'}
        with open(SETTINGS_PATH, "w") as ini:
            settings.write(ini)
            
def getSettings():
    generateSettings()
    settings = configparser.ConfigParser()
    settings.read(SETTINGS_PATH)
    return {s: dict(settings[s]) for s in settings.sections()}

def saveSettings(new_settings: dict):
    settings = configparser.ConfigParser()
    for section, sec_settings in new_settings.items():
        settings[section] = sec_settings
    with open(SETTINGS_PATH, "w") as ini:
        settings.write(ini)