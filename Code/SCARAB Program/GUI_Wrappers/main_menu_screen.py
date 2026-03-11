from ..GUI_Screens import main_menu
from PySide6.QtWidgets import QWidget

class main_menu_screen(QWidget):
    def __init__(self):
        super.__init__()
        
        self.ui = main_menu.Ui_main_menu()
        self.ui.setupUi(self)

    def set_scarab_found(self, isFound):
        self.ui.scarab_status.setText("FOUND" if isFound else "NOT FOUND")

    def set_module(self, module):
        self.ui.inserted_module.setText(module)