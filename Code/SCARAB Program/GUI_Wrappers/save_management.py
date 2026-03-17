from GUI_Screens import save_management_menu
from PySide6.QtWidgets import QWidget

class save_management(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = save_management_menu.Ui_save_management()
        self.ui.setupUi(self)
        
