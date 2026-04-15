from pathlib import Path

from GUI_Screens import modules_menu
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap

class module_menu(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = modules_menu.Ui_modules_menu()
        self.ui.setupUi(self)
        
    def setModule(self, moduleName):
        self.ui.inserted_module.setText(moduleName)
        filepath = Path(__file__).parent.parent.joinpath("Images/Modules/" + moduleName + ".png")
        self.ui.mod_image.setPixmap(QPixmap(filepath))
        
    def setGame(self, gameName):
        self.ui.inserted_game.setText(gameName)