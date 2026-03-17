from pathlib import Path

SAVE_PATH = Path(__file__).parent.parent.joinpath("Saves")

def getSavePath():
    return SAVE_PATH

def getConsolesList():
    consoles = [folder.name for folder in SAVE_PATH.iterdir() if folder.is_dir()]
    return consoles
    
def getGamesByConsole(console):
    console_path = SAVE_PATH.joinpath(console)
    console_saves = [game.name for game in console_path.iterdir() if game.is_dir()]
    return console_saves

def writeSave(module, game, buffer):
    pass

def readSave(savename, path):
    pass