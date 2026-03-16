from GUI_Screens import modules_menu
from PySide6.QtWidgets import QWidget

class module_menu(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = modules_menu.Ui_modules_menu()
        self.ui.setupUi(self)
        
    def setModule(self, moduleName):
        self.ui.inserted_module = moduleName