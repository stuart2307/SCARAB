import sys

from GUI_Screens import main_menu
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap
from pathlib import Path

class main_menu_screen(QWidget):
    IMAGES_PATH = (Path(sys.executable).parent if hasattr(sys, '_MEIPASS') else Path(__file__).parent.parent) / "Images"
    def __init__(self):
        super().__init__()
        
        self.ui = main_menu.Ui_main_menu()
        self.ui.setupUi(self)

    def setScarabFound(self, isFound: bool):
        self.ui.scarab_status.setText("FOUND" if isFound else "NOT FOUND")
        filepath = self.IMAGES_PATH / "SCARAB" / ("found.png" if isFound else "not_found.png")
        self.ui.scarab_image.setPixmap(QPixmap(filepath))

    def setModule(self, module):
        self.ui.inserted_module.setText(module)