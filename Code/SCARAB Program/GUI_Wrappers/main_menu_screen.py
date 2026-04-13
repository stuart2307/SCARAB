from GUI_Screens import main_menu
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPixmap
from pathlib import Path

class main_menu_screen(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = main_menu.Ui_main_menu()
        self.ui.setupUi(self)

    def setScarabFound(self, isFound: bool):
        self.ui.scarab_status.setText("FOUND" if isFound else "NOT FOUND")
        filepath = Path(__file__).parent.parent.joinpath("Images/SCARAB/" + ("found.png" if isFound else "not_found.png"))
        self.ui.scarab_image.setPixmap(QPixmap(filepath))

    def setModule(self, module):
        self.ui.inserted_module.setText(module)