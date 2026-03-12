from GUI_Screens import options
from PySide6.QtWidgets import QWidget

class options_menu(QWidget):
    def __init__(self):
        super().__init__()
        
        self.ui = options.Ui_options()
        self.ui.setupUi(self)